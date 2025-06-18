import yaml
import torch
from torchvision.utils import save_image
import matplotlib.pyplot as plt

def load_config(config_path) :
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def save_reconstructed_images(original,reconstructed,path,nrow=8):
    comparison = torch.cat([original[:nrow],reconstructed[:nrow]])
    save_image(comparison.cpu(), path, nrow=nrow)

def plot_loss(train_loss,test_loss, path):
    plt.figure(figsize=(10, 5))
    plt.plot(train_loss, label='Train Loss')
    plt.plot(test_loss, label='Test Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(path)
    plt.close()  # Close the figure to free memory

