import os
import sys

__package__ = "trainer"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import argparse
import time
import math
import warnings
import torch
from torch import optim, nn
import torch.distributed as dist
from contextlib import nullcontext
from torch.utils.data import DataLoader, DistributedSampler
from transformers import AutoTokenizer, AutoModelForCausalLM
from model.model_minimind import MiniMindConfig, MiniMindForCausalLM
from dataset.lm_dataset import SFTDataset
from model.model_lora import load_lora, save_lora, apply_lora

def Logger(content):
    if not ddp or dist.get_rank() == 0:
        print(content)

