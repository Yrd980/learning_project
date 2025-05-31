import torch
from torch._prims_common import dtype_to_type
import torch.nn.functional as F
from torch import device, export, nn
from transformers.trainer_utils import is_main_process
from .LMConfig import LMConfig

import math

class RMSNorm(torch.nn.Module):
    def __init__(self, dim, eps):
        super(RMSNorm, self).__init__()
        self.weight = torch.nn.Parameter(torch.ones(dim))
        self.eps = eps

    def forward(self, x):
        norm = torch.sqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return x * (self.weight / norm)

def precompute_pos_cis(dim,end,theta):
    freqs = 1.0 / (theta ** (torch.arange(0,dim,2)[: (dim // 2)].float() / dim ))
    t = torch.arange(end,device=freqs.device)
    freqs = torch.outer(t,freqs).float()
    pos_cis = torch.polar(torch.ones_like(freqs),freqs) return pos_cis
def apply_rotary_emb(xq, xk, pos_cis):
    def unite_shape(pos_cis,x):
        ndim = x.ndim
        assert 0 <=1 <= ndim
        assert pos_cis.shape == (x.shape[1],x.shape[2])
        shape = [d if i == 1 or i == ndim -1 else 1 for i,d in enumerate(x.shape)]
        return pos_cis.view(*shape)
    xq_ = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1],-1,2))
    xk_ = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1],-1,2))
    pos_cis = unite_shape(pos_cis,xq_)
    xq_out = torch.view_as_real(xq_ * pos_cis).flatten(3)
    xk_out = torch.view_as_real(xk_ * pos_cis).flatten(3)
    return xq_out.type_as(xq) , xk_out.type_as(xk)

def repeat_kv(x,n_rep):
    bs, slen, n_kv_heads, head_dim = x.shape
    if n_rep == 1 :
        return x
    return (
        x[:,:,:,:None,:]
        .expand(bs,slen,n_kv_heads,n_rep,head_dim)
        .reshape(bs,slen,n_kv_heads*n_rep,head_dim)
    )


class Attention(nn.Module):
    def __init__(self, args:LMConfig):
        super().__init__()
        self.n_kv_heads = args.n_heads if args.n_kv_heads is None else args.n_kv_heads
        assert args.n_heads % self.n_kv_heads == 0
        self.n_local_heads = args.n_heads
        self.n_local_kv_heads = self.n_kv_heads
        self.n_rep = args.n_local_heads // self.n_local_kv_heads
        self.head_dim = args.dim // args.n_heads
        self.wq = nn.Linear(args.dim,args.n_heads * self.head_dim,bias=False)
        self.wk = nn.Linear(args.dim,args.n_kv_heads * self.head_dim,bias=False)
        self.wv = nn.Linear(args.dim,args.n_kv_heads * self.head_dim,bias=False)
        self.wo = nn.Linear(args.n_heads * self.head_dim,args.dim,bias=False)
        self.attn_dropout = nn.Dropout(args.dropout)
        self.resid_dropout = nn.Dropout(args.dropout)
        self.dropout = args.dropout
        self.flash = hasattr(torch.nn.functional,'scaled_dot_product_attention') and args.flash_attn
        mask = torch.full((1,1,args.max_seq_len,args.max_seq_len),float("-inf"))
        mask = torch.triu(mask,diagonal=1)
        self.register_buffer("mask",mask,persistent=False)

def forward(self,
            x,
            pos_cis, 
            past_key_value,
            use_cache=False,
            ):
    bsz,seq_len,_ = x.shape
    xq,xk,xv = self.wq(x),self.wk(x),self.wv(x)
    xq = xq.view(bsz,seq_len,self.n_local_heads,self.head_dim)
    xk = xk.view(bsz,seq_len,self.n_local_kv_heads,self.head_dim)
    xv = xv.view(bsz,seq_len,self.n_local_kv_heads,self.head_dim)

    xq,xk = apply_rotary_emb(xq,xk,pos_cis)
    if past_key_value is not None:
        xk = torch.cat([past_key_value[0],xk],dim=1)
        xv = torch.cat([past_key_value[1],xv],dim=1)
    past_kv = (xk,xv) if use_cache else None

    xq,xk,xv = (
        xq.transpose(1,2),
        repeat_kv(xk,self.n_rep).transpose(1,2),
        repeat_kv(xv,self.n_rep).transpose(1,2),
    )

    if self.flash and seq_len != 1 :
       dropout_p = self.dropout if self.training else 0.0
       output = F.scaled_dot_product_attention(
            xq,xk,xv,
            attn_mask = None,
            dropout_p=dropout_p,
            is_causal = True
        )
    else:
        scores = (xq@x.transpose(-2,-1)) / math.sqrt(self.head_dim)
        scores += self.mask[:,:,:seq_len,:seq_len]
        scores = F.softmax(scores.float(),dim=-1).type_as(xq)
        scores = self.attn_dropout(scores)
        output = scores @ xv

    output = output.transpose(1,2).reshape(bsz,seq_len,-1)
    output = self.resid_dropout(self.wo(output))
    return output,past_kv

class FeedForward(nn.Module):
    def __init__(self, args:LMConfig):
        super().__init__()
        if args.hidden_dim is None:
            hidden_dim = args.dim * 4
            hidden_dim = int(2*hidden_dim/3)
            args.hidden_dim = args.multiple_of * ((hidden_dim+args.multiple_of -1) // args.multiple_of)
        self.w1 = nn.Linear(args.dim,args.hidden_dim,bias=False)
        self.w2 = nn.Linear(args.hidden_dim,args.dim,bias=False)
        self.w3 = nn.Linear(args.dim,args.hidden_dim,bias=False)
        self.dropout = nn.Dropout(args.dropout)

    def forward(self,x):
        return self.dropout(self.w2(F.silu(self.w1(x))*self.w3(x)))

class MoEGate(nn.Module):
    def __init__(self, args:LMConfig):
        super().__init__()
        self.args = args
        self.top_k = args.num_experts_per_tok
        self.n_routed_experts = args.n_routed_experts

        self.scoring_func = args.scoring_func
        self.alpha = args.aux_loss_alpha
        self.seq_aux = args.seq_aux

        self.norm_topk_prob = args.norm_topk_prob
        self.gating_dim = args.dim
        self.weight = nn.Parameter(torch.empty((self.n_routed_experts, self.gating_dim)))
        self.reset_parameters()

    def reset_parameters(self):
        import torch.nn.init as init
        init.kaiming_uniform_(self.weight,a=math.sqrt(5))

    def forward(self,hidden_states):
        bsz, seq_len, h = hidden_states.shape
        hidden_states = hidden_states.view(-1,h)
        logits = F.linear(hidden_states,self.weight,None)

        if self.scoring_func == 'softmax':
            scores = F.softmax(logits,dim=-1)
        else:
            raise NotImplementedError(f'MoE gating scoring function {self.scoring_func} not implemented')

        topk_weight, topk_idx = torch.topk(scores,k=self.top_k,dim=-1,sorted=False)

        if self.top_k > 1 and self.norm_topk_prob:
                denominator = topk_weight.sum(dim=-1,keepdim=True)+1e-20
                topk_weight = topk_weight / denominator

        if self.training and self.alpha > 0.0
            scores_for_aux = scores
            aux_topk = self.top_k
            topk_idx_for_aux_loss = topk_idx.view(bsz,-1)
            if self.seq_aux:
                scores_for_seq_aux = scores_for_aux.view(bsz,seq_len,-1)
                ce = torch.zeros(bsz,self.n_routed_experts,device=hidden_states.device)
                ce.scatter_add_(1,topk_idx_for_aux_loss,torch.ones(bsz,seq_len*aux_topk,device=hidden_states.device)).div_(seq_len*aux_topk/self.n_routed_experts)
                aux_loss = (ce*scores_for_seq_aux.mean(dim=1)).sum(dim=1).mean()*self.alpha
            else:
                mask_ce = F.one_hot(topk_idx_for_aux_loss.view(-1),num_classes=self.n_routed_experts)
                ce = mask_ce.float().mean(0)
                Pi = scores_for_aux.mean(0)
                fi = ce * self.n_routed_experts
                aux_loss = (fi * Pi).sum() * self.alpha
        else:
            aux_loss = 0
        return topk_idx,topk_weight, aux_loss

    class MOEFeedForward(nn.Module):
        def __init__(self, args:LMConfig):
            super().__init__()
            self.args = args
            self.experts = nn.ModuleList([
                FeedForward(args) for _ in range(args.n_routed_experts)
            ])
            self.gate = MoEGate(args)
            if args.n_shared_experts is not None:
                self.n_shared_experts = FeedForward(args)

        def forward(self,x):
            identity = x
            orig_shape = x.shape
            topk_idx, topk_weight, aux_loss = self.gate(x)
            x = x.view(-1,x.shape[-1])
            flat_topk_idx = topk_idx.view(-1)
            if self.training:
                x = x.repeat_interleave(self.args.num_experts_per_tok,dim=0)
                y = torch.empty_like(x,dtype=torch.float16)
                for i, expert in enumerate(self.experts):
                    y[flat_topk_idx==i] = expert(x[flat_topk_idx == i]).to(y.dtype)
                    y = (y.view(*topk_weight.shape, -1) * topk_weight.unsqueeze(-1)).sum(dim=1)
                    y = y.view(*orig_shape)
            else:
                y = self.moe_infer(x,flat_topk_idx,topk_weight.view(-1,1)).view(*orig_shape)
            if self.args.n_shared_experts is not None:
                y += self.n_shared_experts(identity)
            self.aux_loss = aux_loss
            return y

        @torch.no_grad
        def moe_infer(self,x,flat_expert_indices,flat_expert_weights):
            expert_cache = torch.zeros_like(x)
            idxs = flat_expert_indices.argsort()
            tokens_per_expert = flat_expert_indices.bincount().cpu().numpy().cumsum(0)
            token_idxs = idxs // self.args.num_experts_per_tok
            for i,end_idx in enumerate(tokens_per_expert):
                start_idx = 0 if i == 0 else tokens_per_expert[i-1]
                if start_idx == end_idx:
                    continue
                expert = self.experts[i]
                exp_token_idx = token_idxs[start_idx:end_idx]
                expert_tokens = x[exp_token_idx]
                expert_out = expert(expert_tokens).to(expert_cache.dtype)
                expert_out.mul_(flat_expert_weights[idxs[start_idx:end_idx]])
                expert_cache.scatter_add_(0,exp_token_idx.view(-1,1).repeat(1,x.shape[-1]),expert_out)

            return expert_cache
