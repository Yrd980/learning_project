import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils import tensorboard
from torch.utils.data import DataLoader
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
from torch.utils.tensorboard import SummaryWriter, writer
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import numpy as np
from models.autoencoder import Autoencoder
from models.cnn import CNN
from data.dataset import XrayDataset
from constants.constants import Constants


def add_noise(image, noise_factor=0.3):
    noise = torch.randn_like(image) * noise_factor
    noisy_image = image + noise
    return torch.clamp(noisy_image, 0., 1.)  # Ensure pixel values are in [0, 1]

def plot_confusion_matrix(cm,classes,output_path):
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm,annot=True,fmt='d',cmap='Blues',xticklabels=classes,yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def train_cnn(cnn_model,autoencoder,lr,train_loader,test_loader,device,num_epochs=100,output_path='results_cnn',noise_factor=0.3):
    checkpoint_dir = os.path.join(output_path, 'checkpoints')
    tensorboard_dir = os.path.join(output_path, 'tensorboard')
    plot_dir = os.path.join(output_path, 'plots')
    os.makedirs(checkpoint_dir, exist_ok=True)
    os.makedirs(tensorboard_dir, exist_ok=True)
    os.makedirs(plot_dir, exist_ok=True)

    writer = SummaryWriter(tensorboard_dir)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cnn_model = cnn_model.to(device)
    autoencoder = autoencoder.to(device)
    autoencoder.eval()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(cnn_model.parameters(), lr=lr)

    best_test_acc = 0.0

    history = {
        'train_loss': [],
        'test_loss': [],
        'train_acc': [],
        'test_acc': [],
    }

    start_time = time.time()
    global_step = 0

    classes = Constants.CLASSES

    for epoch in range(num_epochs):
        cnn_model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        train_bar = tqdm(train_loader, desc=f'Epoch [{epoch+1}/{num_epochs} Training]')

        for batch_idx , (data,targets) in enumerate(train_bar):
            data, targets = data.to(device), targets.to(device)
            noisy_data = add_noise(data, noise_factor=noise_factor)
            
            with torch.no_grad():
                denoised_data = autoencoder(noisy_data)

            outputs = cnn_model(denoised_data)
            loss = criterion(outputs,targets)

            _, predicted = outputs.max(1)
            train_total += targets.size(0)
            train_correct += predicted.eq(targets).sum().item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

            writer.add_scalar('Loss/train', loss.item(), global_step)

            train_bar.set_postfix({

            })
