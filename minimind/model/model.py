import torch
import torch.nn.functional as F
from torch import nn
from typing import Optional, Tuple, List 
import math
from .LMConfig import LMConfig
from transformers import PreTrainedModel
from transformers.modeling_outputs import CausalLMOutputWithPast


class RMSNorm(torch.nn.Module):
    def __init__(self, dim: int, eps: float):
        super().__init__()
        self.eps = eps
        # treat model parameter backpropagation calculate gradient
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        # -1 usually mean calculate all
        return self.weight * (
            x.float() * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        ).type_as(x)


def precompute_pos_cis(dim: int, end: int = int(32 * 1024), theta: float = 1e6):
    # // 2 because 2i and 2i+1 in sin cos equal so save half
    freqs = 1.0 / (theta ** (torch.arange(0, dim, 2)[: (dim // 2)].float() / dim))
    t = torch.arange(end, device=freqs.device)
    freqs = torch.outer(t, freqs).float()
    pos_cis = torch.polar(torch.ones_like(freqs), freqs)
    return pos_cis


# xq xk (batch_size,seq_len,num_heads,head_dim)
# pos_cis (seq_len,head_dim//2)
def apply_rotary_emb(xq, xk, pos_cis):
    def unite_shape(pos_cis, x):
        ndim = x.ndim
        assert 0 <= 1 < ndim
        assert pos_cis.shape == (x.shape[1], x.shape[-1])
        shape = [d if i == 1 or i == ndim - 1 else 1 for i, d in enumerate(x.shape)]
        return pos_cis.view(*shape)

    xq_ = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1], -1, 2))
    xk_ = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1], -1, 2))
    pos_cis = unite_shape(pos_cis, xq_)
    xq_out = torch.view_as_complex(xq_ * pos_cis).flatten(3)
    xk_out = torch.view_as_complex(xk_ * pos_cis).flatten(3)
    return xq_out.type_as(xq), xk_out.type_as(xk)


def repeat_kv(x: torch.Tensor, n_rep: int) -> torch.Tensor:
    """torch.repeat_interleave(x,dim=2,repeats=n_rep)"""
    bs, slen, n_kv_heads, head_dim = x.shape
    if n_rep == 1:
        return x
    return (
        x[:, :, :, None, :]
        .expand(bs, slen, n_kv_heads, n_rep, head_dim)
        .reshape(bs, slen, n_kv_heads * n_rep, head_dim)
    )


class Attention(nn.Module):
    def __init__(self, args: LMConfig):
        super().__init__()
        # GQA
        self.n_kv_heads = args.n_heads if args.n_kv_heads is None else args.n_kv_heads
        assert args.n_heads % self.n_kv_heads == 0
        self.n_local_heads = args.n_heads
        self.n_local_kv_heads = args.n_kv_heads
        self.n_rep = self.n_local_heads // self.n_local_kv_heads
        self.head_dim = args.dim // args.n_heads
        self.wq = nn.Linear(args.dim, args.n_heads * self.head_dim, bias=False)
        self.wk = nn.Linear(args.dim, args.n_kv_heads * self.head_dim, bias=False)
        self.wv = nn.Linear(args.dim, args.n_kv_heads * self.head_dim, bias=False)
        self.wo = nn.Linear(args.n_heads * self.head_dim, args.dim, bias=False)
        self.attn_dropout = nn.Dropout(args.dropout)
        self.resid_dropout = nn.Dropout(args.dropout)
        self.flash = (
            hasattr(torch.nn.functional, "scaled_dot_product_attention")
            and args.flash_attn
        )

        mask = torch.full((1, 1, args.max_seq_len, args.max_seq_len), float("-inf"))
        mask = torch.triu(mask, diagonal=1)
        self.register_buffer("mask", mask, persistent=False)

    def forward(
        self,
        x: torch.Tensor,
        pos_cis: torch.Tensor,
        past_key_value: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
        use_cache=False,
    ):

        # x.shape still (batch_size,seq_len,num_heads,head_dim)
        bsz, seq_len, _ = x.shape
        xq, xk, xv = self.wq(x), self.wk(x), self.wv(x)
        xq = xq.view(bsz, seq_len, self.n_local_heads, self.head_dim)
        xk = xk.view(bsz, seq_len, self.n_local_kv_heads, self.head_dim)
        xv = xv.view(bsz, seq_len, self.n_local_kv_heads, self.head_dim)

        xq, xk = apply_rotary_emb(xq, xk, pos_cis)
        # kv implement
        if past_key_value is not None:
            xk = torch.cat([past_key_value[0], xk], dim=1)
            xv = torch.cat([past_key_value[1], xv], dim=1)
        past_kv = (xk, xv) if use_cache else None

        xq, xk, xv = (
            xq.transpose(1, 2),
            repeat_kv(xk, self.n_rep).transpose(1, 2),
            repeat_kv(xv, self.n_rep).transpose(1, 2),
        )

        if self.flash and seq_len != 1:
            dropout_p = self.dropout if self.training else 0.0
            output = F.scaled_dot_product_attention(
                xq, xk, xv, attn_mask=None, dropout_p=dropout_p, is_causal=True
            )
        else:
            scores = (xq @ xk.transpose(-2, -1)) / math.sqrt(self.head_dim)
            scores += self.mask[:, :, :seq_len, :seq_len]
            scores = F.softmax(scores.float(), dim=-1).type_as(xq)
            scores = self.attn_dropout(scores)
            output = scores @ xv

        # merge n_local_heads and head_dim
        # last linear transform
        output = output.transpose(1, 2).reshape(bsz, seq_len, -1)
        output = self.resid_dropout(self.wo(output))
        return output, past_kv


class FeedForward(nn.Module):
    def __init__(self, config: LMConfig):
        super().__init__()
        if config.hidden_dim is None:
            hidden_dim = 4 * config.dim
            hidden_dim = int(2 * hidden_dim / 3)
            config.hidden_dim = config.multiple_of * (
                (hidden_dim + config.multiple_of - 1) // config.multiple_of
            )
        self.w1 = nn.Linear(config.dim, config.hidden_dim, bias=False)
        self.w2 = nn.Linear(config.hidden_dim, config.dim, bias=False)
        self.w3 = nn.Linear(config.dim, config.hidden_dim, bias=False)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        return self.dropout(self.w2(F.silu(self.w1(x)) * self.w3(x)))


class MoEGate(nn.Module):
    def __init__(self, config: LMConfig):
        super().__init__()
        self.config = config
        self.top_k = config.num_experts_per_tok
        self.n_routed_experts = config.n_routed_experts

        self.scoring_func = config.scoring_func
        self.alpha = config.aux_loss_alpha
        self.seq_aux = config.seq_aux

        self.norm_topk_prob = config.norm_topk_prob
        self.gating_dim = config.dim
        self.weight = nn.Parameter(
            torch.empty((self.n_routed_experts, self.gating_dim))
        )
        self.reset_parameters()

    def reset_parameters(self) -> None:
        import torch.nn.init as init

        init.kaiming_uniform_(self.weight, a=math.sqrt(5))

    def forward(self, hidden_states):
        # hidden_states(batch_size,seq_len,hidden_dim)
        bsz, seq_len, h = hidden_states.shape
        # hidden_states(batch_size * seq_len,hidden_dim)
        hidden_states = hidden_states.view(-1, h)
        # weight(hidden_dim,n_routed_experts)
        # logits(batch_size * seq_len,n_routed_experts)
        logits = F.linear(hidden_states, self.weight, None)
        if self.scoring_func == "softmax":
            # same as logits n_routed_experts execute softmax
            scores = logits.softmax(dim=-1)
        else:
            raise NotImplementedError(
                f"insupportable scoring function for MoE gating: {self.scoring_func}"
            )

        # shape(batch_size * seq_len,top_k)
        topk_weight, topk_idx = torch.topk(scores, k=self.top_k, dim=-1, sorted=False)

        if self.top_k > 1 and self.norm_topk_prob:
            denominator = topk_weight.sum(dim=-1, keepdim=True) + 1e-20
            topk_weight = topk_weight / denominator

        if self.training and self.alpha > 0.0:
            scores_for_aux = scores
            aux_topk = self.top_k
            # shape(batch_size,seq_len * top_k)
            topk_idx_for_aux_loss = topk_idx.view(bsz, -1)
            if self.seq_aux:
                # shape(batch_size,seq_len,n_routed_experts)
                scores_for_seq_aux = scores_for_aux.view(bsz, seq_len, -1)
                # shape(batch_size,n_routed_experts)
                ce = torch.zeros(
                    bsz, self.n_routed_experts, device=hidden_states.device
                )
                # apply n_routed_experts cumulate and topk_idx_for_aux_loss as index aka merge experts occur numbers
                # topk_idx_for_aux_loss(batch_size * seq_len,top_k)
                ce.scatter_add_(
                    1,
                    topk_idx_for_aux_loss,
                    torch.ones(bsz, seq_len * aux_topk, device=hidden_states.device),
                ).div_(seq_len * aux_topk / self.n_routed_experts)
                # dim=1 mean seq_len (batch_size,seq_len,n_routed_experts) array mean(dim=1) column average aka experts scores average
                # # Batch 1
                #    [[0.1, 0.2, 0.3, 0.4],  # Sequence position 1
                #     [0.5, 0.6, 0.7, 0.8],  # Sequence position 2
                #     [0.9, 1.0, 1.1, 1.2]], # Sequence position 3
                #    # Batch 2
                #    [[1.3, 1.4, 1.5, 1.6],  # Sequence position 1
                #     [1.7, 1.8, 1.9, 2.0],  # Sequence position 2
                #     [2.1, 2.2, 2.3, 2.4]]  # Sequence position 3
                aux_loss = (ce * scores_for_seq_aux.mean(dim=1)).sum(
                    dim=1
                ).mean() * self.alpha
            else:
                # shape(batch_size * seq_len * top_k , n_routed_experts)
                mask_ce = F.one_hot(
                    topk_idx_for_aux_loss.view(-1), num_classes=self.n_routed_experts
                )
                # shape(n_routed_experts)
                ce = mask_ce.float().mean(0)
                # shape(n_routed_experts) just like 226 line
                Pi = scores_for_aux.mean(0)
                fi = ce * self.n_routed_experts
                aux_loss = (Pi * fi).sum() * self.alpha
        else:
            aux_loss = 0
        return topk_idx, topk_weight, aux_loss


class MoEFeedForward(nn.Module):
    def __init__(self, config: LMConfig):
        super().__init__()
        self.config = config
        self.experts = nn.ModuleList(
            [FeedForward(config) for _ in range(config.n_routed_experts)]
        )
        self.gate = MoEGate(config)
        if config.n_shared_experts is not None:
            self.shared_experts = FeedForward(config)

    def forward(self, x):
        identity = x
        orig_shape = x.shape
        topk_idx, topk_weight, aux_loss = self.gate(x)
        x = x.view(-1, x.shape[-1])
        flat_topk_idx = topk_idx.view(-1)
        if self.training:
            x = x.repeat_interleave(self.config.num_experts_per_tok, dim=0)
            y = torch.empty_like(x, dtype=torch.float16)
            for i, expert in enumerate(self.experts):
                y[flat_topk_idx == i] = expert[x[flat_topk_idx == i]].to(y.dtype)
            y = y.view(*topk_weight.shape, -1) * topk_weight.unsqueeze(-1).sum(dim=1)
            y = y.view(*orig_shape)
        else:
            y = self.moe_infer(x, flat_topk_idx, topk_weight.view(-1, 1)).view(
                *orig_shape
            )
        if self.config.n_shared_experts is not None:
            y += self.shared_experts(identity)
        self.aux_loss = aux_loss
        return y

    @torch.no_grad
    def moe_infer(self, x, flat_expert_indices, flat_expert_weights):
        expert_cache = torch.zeros_like(x)
        idxs = flat_expert_indices.argsort()
        # calculate end_idx
        tokens_per_expert = flat_expert_indices.bincount().cpu().numpy().cumsum(0)
        # expert index
        token_idxs = idxs // self.config.num_experts_per_tok
        for i, end_idx in enumerate(tokens_per_expert):
            start_idx = 0 if i == 0 else tokens_per_expert[i - 1]
            if start_idx == end_idx:
                continue
            expert = self.experts[i]
            exp_token_idx = token_idxs[start_idx:end_idx]
            expert_tokens = x[exp_token_idx]
            expert_out = expert(expert_tokens).to(expert_cache.dtype)
            expert_out.mul_(flat_expert_weights[idxs[start_idx:end_idx]])
            expert_cache.scatter_add_(
                0, exp_token_idx.view(-1, 1).repeat(1, x.shape[-1]), expert_out
            )

        return expert_cache


class MiniMindBlock(nn.Module):
    def __init__(self, layer_id: int, config: LMConfig):
        super().__init__()
        self.n_head = config.n_head
        self.dim = config.dim
        self.head_dim = config.dim // config.n_heads
        self.attention = Attention(config)

        self.layer_id = layer_id
        self.attention_norm = RMSNorm(config.dim, eps=config.norm_eps)
        self.ffn_norm = RMSNorm(config.dim, eps=config.eps)
        self.feed_forward = (
            FeedForward(config) if not config.use_moe else MoEFeedForward(config)
        )

    def forward(self, x, pos_cis, past_key_value, use_cache=False):
        h_attn, past_kv = self.attention(
            self.attention_norm(x),
            pos_cis,
            past_key_value=past_key_value,
            use_cache=use_cache,
        )
        # reside
        h = x + h_attn
        out = h + self.feed_forward(self.ffn_norm)
        return out, past_kv


class MiniMindLM(PreTrainedModel):
    config_class = LMConfig

    def __init__(self, params: LMConfig = None):
        self.params = params or LMConfig
        super().__init__(self.params)
        self.vocab_size, self.n_layers = params.vocab_size, params.n_layers
        self.tok_embeddings = nn.Embedding(params.vocab_size, params.dim)
        self.dropout = nn.Dropout(params.dropout)
        self.layers = nn.ModuleList(
            [MiniMindBlock(l, params) for l in range(self.n_layers)]
        )
        self.norm = RMSNorm(params.dim, eps=params.norm_eps)
        self.output = nn.Linear(params.dim, params.vocab_size, bias=False)
        self.tok_embeddings.weight = self.output.weight
        self.register_buffer(
            "pos_cis",
            precompute_pos_cis(
                dim=params.dim // params.n_heads, theta=params.rope_theta
            ),
            persistent=False,
        )
        self.OUT = CausalLMOutputWithPast()

    def forward(
        self,
        input_ids: Optional[torch.Tensor] = None,
        past_key_values: Optional[List[Tuple[torch.Tensor, torch.Tensor]]] = None,
        use_cache: bool = False,
        **args,
    ):
        past_key_values = past_key_values or [None] * len(self.layers)
        start_pos = args.get('start_pos',0)
        h = self.dropout(self.tok_embeddings(input_ids))
        pos_cis = self.pos_cis[start_pos:start_pos+input_ids.size(1)]
        past_kvs = []
        for l,layer in enumerate(self.layers):
            h,past_kv = layer(
                h,pos_cis,
                past_key_value=past_key_values[l],
                use_cache = use_cache
            )
            past_kvs.append(past_kv)
        logits = self.output(self.norm(h))
        aux_loss = sum(l.feed_forward.aux_loss for l in self.layers if isinstance(l.feed_forward,MoEFeedForward))
        self.OUT.__setitem__('logits',logits)
        self.OUT.__setitem__('aux_loss',aux_loss)
        self.OUT.__setitem__('past_key_values',past_key_values)
        return self.OUT

    @torch.inference_mode()
    def generate(self, input_ids, eos_token_id=2, max_new_tokens=1024, temperature=0.75, top_p=0.90,
                 stream=False, rp=1., use_cache=True, pad_token_id=0, **args):
        if stream:
            return self._stream(input_ids,eos_token_id,max_new_tokens,temperature,top_p,rp,use_cache,**args)
        generated = []
        for i in range(input_ids.size(0)):
            non_pad = input_ids[i][input_ids[i]!=pad_token_id].unsqueeze(0)
            out = self._stream(non_pad,eos_token_id,max_new_tokens,temperature,top_p,rp,use_cache,**args)
            tokens_list = [tokens[:,-1] for tokens in out]
            gen = torch.cat(tokens_list,dim=-1) if tokens_list else non_pad
            full_sequence = torch.cat([non_pad,gen],dim=-1)
            generated.append(full_sequence)
        max_length = max(seq.size(1) for seq in generated)
        generated = [
            torch.cat(
                [seq,torch.full((1,max_length-seq.size(1)),pad_token_id,dtype=seq.dtype,device=seq.device)],
                dim = -1
            )
            for seq in generated
        ]
        return torch.cat(generated,dim=0)
    
    def _stream(self,input_ids,eos_token_id,max_new_tokens,temperature,top_p,rp,use_cache,**args):
        start,first_seq,past_kvs = input_ids[1],True,None
        while input_ids.shape[1] < max_new_tokens - 1:
            if first_seq or not use_cache:
                out,first_seq = self(input_ids,past_key_values=past_kvs,use_cache = use_cache,**args),False
            else:
                out = self(input_ids[:-1],past_key_values=past_kvs,use_cache=use_cache,start_pos=input_ids.shape[1]-1,**args)
            logits,past_kvs = out.logits[:-1,:],out.past_key_values
            logits[:,list(set(input_ids.tolist()[0]))] /= rp
            logits /= (temperature+1e-9)
            if top_p is not None and top_p < 1.0:
                sorted_logits , sorted_indices = torch.sort(logits,descending=True,dim=-1)
                sorted_probs = F.softmax(sorted_logits,dim=-1)
                cumulative_probs = torch.cumsum(sorted_probs,dim=-1)
                sorted_indices_to_remove = cumulative_probs > top_p 
                sorted_indices_to_remove[:,1] = sorted_indices_to_remove[:,:-1].clone()
                sorted_indices_to_remove[:,0] = False
                indices_to_remove = sorted_indices_to_remove.scatter_add_(1,sorted_indices,sorted_indices_to_remove)
                logits[indices_to_remove] = -float('Inf')
            input_ids_next = torch.multinomial(F.softmax(logits,dim=-1),num_samples=1)
            input_ids = torch.cat((input_ids,input_ids_next),dim=1)
            yield input_ids[:start:]
            if input_ids_next.item() == eos_token_id:
                break
