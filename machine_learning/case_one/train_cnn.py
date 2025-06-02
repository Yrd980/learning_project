import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
from torch.utils.tensorboard import SummaryWriter
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
from models.autoencoder import Autoencoder
from models.cnn import CNN
from data.dataset import XrayDataset
from constants.constants import Constants


def add_noise(image, noise_factor=0.3):
    noise = torch.randn_like(image) * noise_factor
    return torch.clamp(image + noise, 0., 1.)  

def plot_confusion_matrix(cm,classes,output_path):
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm,annot=True,fmt='d',cmap='Blues',xticklabels=classes,yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def save_plots(history,output_path,epoch=None):
    plt.figure(figsize=(12,5))

    for i, (metrics, title, ylabel) in enumerate([
        (('train_loss', 'test_loss'), 'Loss Curve', 'Loss'),
        (('train_acc', 'test_acc'), 'Accuracy Curve', 'Accuracy (%)')
    ]):
        plt.subplot(1, 2, i + 1)
        for key in metrics:
            plt.plot(history[key], label=key.replace('_', ' ').title())
        plt.xlabel('Epoch')
        plt.ylabel(ylabel)
        plt.legend()
        plt.title(title)

    plt.tight_layout()
    filename = f'loss_accuracy_epoch_{epoch+1}.png' if epoch is not None else 'final_metrics.png'
    plt.savefig(os.path.join(output_path,filename))
    plt.close()

def train_cnn(cnn_model,autoencoder,lr,train_loader,test_loader,device,num_epochs=100,output_path='results/cnn',noise_factor=0.3):
    checkpoint_dir, tensorboard_dir, plot_dir = [os.path.join(output_path, d) for d in ['checkpoints', 'tensorboard', 'plots']]
    for d in [checkpoint_dir, tensorboard_dir, plot_dir]:
        os.makedirs(d, exist_ok=True)

    writer = SummaryWriter(tensorboard_dir)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cnn_model, autoencoder = cnn_model.to(device), autoencoder.to(device)
    autoencoder.eval()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(cnn_model.parameters(), lr=lr)
    best_test_acc = 0.0

    history = {k: [] for k in ['train_loss', 'test_loss', 'train_acc', 'test_acc']}

    start_time = time.time()
    global_step = 0
    classes = Constants.CLASSES

    def _run_epoch(model,loader,autoencoder,criterion,device,noise_factor=0.3,train=False,global_step=0):
        model.train() if train else model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        all_preds, all_targets = [], []

        bar = tqdm(loader,desc='Training' if train else 'Testing')

        for data, targets in bar:
            data, targets = data.to(device), targets.to(device)
            noisy_data = add_noise(data,noise_factor)

            with torch.no_grad():
                denoised_data = autoencoder(noisy_data)

            outputs = model(denoised_data)
            loss = criterion(outputs,targets)

            if train:
                model.zero_grad()
                loss.backward()
                optimizer.step()

                writer.add_scalar('Loss/train', loss.item(), global_step)
                global_step += 1

            running_loss += loss.item()
            _,predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

            all_preds.extend(predicted.cpu().numpy())
            all_targets.extend(targets.cpu().numpy())

            bar.set_postfix({
                'loss': loss.item(),
                'acc': 100. * correct / total
            })

        avg_loss = running_loss / len(loader)
        acc = 100. * correct / total
        return avg_loss, acc, all_preds, all_targets, global_step

    for epoch in range(num_epochs):
        train_loss, train_acc, _, _, global_step = _run_epoch(cnn_model, train_loader, autoencoder, criterion, device, noise_factor, True, global_step)
        test_loss, test_acc, preds, targets, _ = _run_epoch(cnn_model, test_loader, autoencoder, criterion, device, noise_factor, False)

        history['train_loss'].append(train_loss)
        history['test_loss'].append(test_loss)
        history['train_acc'].append(train_acc)
        history['test_acc'].append(test_acc)

        writer.add_scalars('Loss/epoch', {'train': train_loss, 'test': test_loss}, epoch)
        writer.add_scalars('Accuracy/epoch', {'train': train_acc, 'test': test_acc}, epoch)

        cm = confusion_matrix(targets,preds)
        plot_confusion_matrix(cm,classes,os.path.join(plot_dir,f'confusion_matrix_epoch_{epoch+1}.png'))

        print(f"\nEpoch {epoch+1}:\n{classification_report(targets, preds, target_names=classes)}")
        print(f"Time: {time.time() - start_time:.2f}s | Train Acc: {train_acc:.2f}% | Test Acc: {test_acc:.2f}%")

        if test_acc > best_test_acc:
            best_test_acc = test_acc
            torch.save(cnn_model.state_dict(), os.path.join(checkpoint_dir, 'best_cnn_model.pth'))

        if (epoch + 1) % 10 == 0:
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': cnn_model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'train_loss': train_loss,
                'test_loss': test_loss,
                'train_acc': train_acc,
                'test_acc': test_acc
            }

            torch.save(checkpoint, os.path.join(checkpoint_dir, f'cnn_checkpoint_epoch_{epoch+1}.pth'))
            save_plots(history, plot_dir, epoch)

    torch.save(cnn_model.state_dict(), os.path.join(checkpoint_dir, 'final_cnn_model.pth'))
    save_plots(history,plot_dir)
    print(f'Training completed in {time.time() - start_time:.2f} seconds')
    writer.close()
    return history

if __name__ == "__main__":
    torch.manual_seed(42)
    device =torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')

    train_dataset = XrayDataset(Constants.ROOT_PATH,is_train=True)
    test_dataset = XrayDataset(Constants.ROOT_PATH, is_train=True)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=4)

    autoencoder = Autoencoder().to(device)
    autoencoder.load_state_dict(torch.load('results/autoencoder/checkpoints/best_autoencoder.pth', map_location=device))

    cnn_model = CNN()

    history = train_cnn(
        cnn_model=cnn_model,
        autoencoder=autoencoder,
        lr=1e-3,
        train_loader=train_loader,
        test_loader=test_loader,
        num_epochs=100,
        device=device,
        noise_factor=0.3
    )


