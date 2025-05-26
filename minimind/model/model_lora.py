import torch
from torch import nn

class LoRA(nn.Module):
    def __init__(self,in_features,out_features,rank):
        super().__init__()
        self.rank = rank
        self.A = nn.Linear(in_features,rank,bias=False)
        self.B = nn.Linear(rank,out_features,bias=False)
        self.A.weight.data.normal_(mean=0.0,std=0.02)
        self.B.weight.data.zero_()

    def forward(self,x):
        return self.B(self.A(x))

def apply_lora(model, rank=16, target_modules=None):
    lora_modules = {}
    for name, module in model.named_modules():
        if isinstance(module, nn.Linear):
            if target_modules and name not in target_modules:
                continue
            lora = LoRA(module.in_features, module.out_features, rank).to(next(model.parameters()).device)
            module.lora = lora  # attach to each module
            original_forward = module.forward

            def forward_with_lora(x, orig=original_forward, lora_mod=lora):
                return orig(x) + lora_mod(x)

            module.forward = forward_with_lora
            lora_modules[name] = lora
    model._lora_modules = lora_modules  # store for later access

def save_lora(model, path):
    state_dict = {}
    for name, lora in getattr(model, "_lora_modules", {}).items():
        for key, val in lora.state_dict().items():
            state_dict[f"{name}.lora.{key}"] = val
    torch.save(state_dict, path)

def load_lora(model, path):
    state_dict = torch.load(path, map_location=next(model.parameters()).device)
    for name, lora in getattr(model, "_lora_modules", {}).items():
        lora_state = {k.replace(f"{name}.lora.", ""): v for k, v in state_dict.items() if k.startswith(f"{name}.lora.")}
        lora.load_state_dict(lora_state)


