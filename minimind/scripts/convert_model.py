import os
import sys

__package__ = "scripts"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import torch
import warnings
from transformers import AutoTokenizer,AutoModelForCausalLM, LlamaConfig, LlamaForCausalLM, ,LlamaForCausalLM

from model.model_minimind import MiniMindConfig,MiniMindForCausalLM

warnings.filterwarnings('ignore',category=UserWarning)

def convert_torch2transformers_minimind(torch_path,transformers_path,dtype=torch.bfloat16):
    MiniMindConfig.register_for_auto_class()
    MiniMindForCausalLM.register_for_auto_class("AutoModelForCausalLM")
    lm_model = MiniMindForCausalLM(lm_config)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    state_dict = torch.load(torch_path,map_location=device)
    lm_model.load_state_dict(state_dict,strict=False)
    lm_model = lm_model.to(dtype)
    model_params = sum(p.numel for p in lm_model.parameters() if p.requires_grad)
    print(f'model parameters: {model_params / 1e6} million = {model_params / 1e9} B (Billion)')
    lm_model.save_pretrained(transformers_path,safe_serialization=False)
    tokenizer = AutoTokenizer.from_pretrained('../model/')
    tokenizer.save_pretrained(transformers_path)
    print(f"model save with Transformers-MiniMind format: {transformers_path}")

def covert_torch2transformers_llama(torch_path,transformers_path,dtype=torch.bfloat16):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    state_dict = torch.load(torch_path,map_location=device)
    llama_config = LlamaConfig(
        vocab_size=lm_config.vocab_size,
        hidden_size=lm_config.hidden_size,
        intermediate_size=64*((int(lm_config.hidden_size * 8 / 3) + 64 -1) // 64),
        num_hidden_layers=lm_config.num_hidden_layers,
        num_attention_heads=lm_config.num_attention_heads,
        num_key_value_heads=lm_config.num_key_value_heads,
        max_position_embeddings=lm_config.max_seq_len,
        rms_norm_eps=lm_config.rms_norm_eps,
        rope_theta=lm_config.rope_theta
    )
    llama_model = LlamaForCausalLM(llama_config)
    llama_model.load_state_dict(state_dict,strict=False)
    llama_model = llama_model.to(dtype)
    llama_model.save_pretrained(transformers_path)
    model_params = sum(p.numel() for p in llama_model.parameters() if p.requires_grad)
    print(f'model parameters: {model_params / 1e6} million = {model_params / 1e9} B (Billion)')
    llama_model.save_pretrained(transformers_path,safe_serialization=False)
    tokenizer = AutoTokenizer.from_pretrained('../model/')
    tokenizer.save_pretrained(transformers_path)
    print(f"model save with Transformers-LLama format: {transformers_path}")


def convert_transformers2torch(transformers_path, torch_path):
    model = AutoModelForCausalLM.from_pretrained(transformers_path, trust_remote_code=True)
    torch.save(model.state_dict(), torch_path)
    print(f"model save to PyTorch 格式: {torch_path}")



if __name__ == '__main__':
    lm_config = MiniMindConfig(hidden_size=768,num_hidden_layers=16,max_seq_len=8192,use_moe=False)
    
    torch_path = f"../out/full_sft_{lm_config.hidden_size}{'_moe' if lm_config.use_moe else ''}.pth"

    transformers_path = '../MiniMind2'

    convert_torch2transformers_minimind(torch_path, transformers_path)

 
