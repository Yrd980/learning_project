import os

import torch
import warnings
from .model_minimind import *
from typing import Optional, Tuple, List
from torch import nn
from transformers import CLIPProcessor, CLIPModel
from typing import List

warnings.filterwarnings("ignore")

class VLMConfig(MiniMindConfig):
    model_type = "minimind-v"

    def __init__(
        self,
        image_special_token: str = '@' * 196,
        image_ids : List = [34] * 196,
        **kwargs,
    ):
        self.image_special_token = image_special_token
        self.image_ids = image_ids
        super().__init__(**kwargs)

class VisionProj(nn.Module):
    def __init__(self,ve_hidden_size=768,hidden_size = 512):
        super().__init__()
        self.ve_hidden_size = ve_hidden_size
        self.hidden_size = hidden_size
        self.vision_proj = nn.Sequential(
            nn.Linear(self.ve_hidden_size,self.hidden_size)
        )

    def forward(self,image_encoders):
        vision_proj = self.vision_proj(image_encoders)
        return vision_proj

class MiniMindVLM(MiniMindForCasualLM):
    config_class = VLMConfig
 

