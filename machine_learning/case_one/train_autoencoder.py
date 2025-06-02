import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision.utils import make_grid
import os
from data.dataset import XrayDataset
from constants.constants import Constants
from models.autoencoder import Autoencoder
from tqdm import tqdm
import time
from torch.utils.tensorboard import SummaryWriter

def train_autoencoder(model,lr,train_loader,test_loader,device,num_epochs=100,output_dir='results/autoencoder'):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    checkpoint_dir, tensorboard_dir = [os.path.join(output_dir,d) for d in ['checkpoints', 'tensorboard']]
    for d in [checkpoint_dir,tensorboard_dir]:
        os.makedirs(d,exist_ok=True)

    writer = SummaryWriter(tensorboard_dir)
    model.to(device)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    best_test_loss = float('inf')

    fixed_test_data, _ = next(iter(test_loader))
    fixed_test_data = fixed_test_data.to(device)

    writer.add_graph(model,fixed_test_data)

    start_time = time.time()
    global_step = 0

    def _run_epoch(loader,is_train=True):
        nonlocal global_step
        model.train() if is_train else model.eval()
        total_loss = 0

        bar = tqdm(loader, desc=f"{'Train' if is_train else 'Test'} Epoch {epoch+1}/{num_epochs}")

        for data,_ in bar:
            data = data.to(device)
            output = model(data)
            loss =criterion(output,data)

            if is_train:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                global_step += 1
                if writer is not None:
                    writer.add_scalar('Loss/train_step', loss.item(), global_step)

            total_loss += loss.item()
            bar.set_postfix(loss=loss.item())

        return total_loss / len(loader)

    train_losses, test_losses = [], []

    for epoch in range(num_epochs):

        train_loss = _run_epoch(train_loader, is_train=True)
        test_loss = _run_epoch(test_loader, is_train=False)

        train_losses.append(train_loss)
        test_losses.append(test_loss)

        if writer is not None:
            writer.add_scalar('Loss/train_epoch', train_loss, epoch)
            writer.add_scalar('Loss/test_epoch', test_loss, epoch)

            with torch.no_grad():
                reconstructed = model(fixed_test_data)
                comparison = torch.cat([fixed_test_data[:8],reconstructed[:8]])
                grid = make_grid(comparison, nrow=8, normalize=True)
                writer.add_image('Reconstruction', grid, epoch)

            for name,param in model.named_parameters():
                writer.add_histogram(f'Parameters/{name}', param, epoch)
                if param.grad is not None:
                    writer.add_histogram(f'Gradient{name}', param.grad, epoch)

        elapsed_time = time.time() - start_time

        print(f'Epoch [{epoch+1}/{num_epochs}], '
              f'Train Loss: {train_loss:.6f}, '
              f'Test Loss: {test_loss:.6f}, '
              f'Time: {elapsed_time:.2f}s')

        if test_loss < best_test_loss:
            best_test_loss = test_loss
            torch.save(model.state_dict(), os.path.join(checkpoint_dir, 'best_autoencoder.pth'))

        if (epoch + 1) % 10 == 0:
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'train_loss': train_loss,
                'test_loss': test_loss
            }
            torch.save(checkpoint, os.path.join(checkpoint_dir, f'autoencoder_checkpoint_epoch_{epoch+1}.pth'))

        torch.save(model.state_dict(), os.path.join(checkpoint_dir, 'final_autoencoder.pth'))

        if writer is not None:
           writer.close()

    print(f'Training completed in {time.time() - start_time:.2f} seconds.')
    return train_losses, test_losses
 
if __name__ == "__main__":
    torch.manual_seed(42)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Using device: {device}')

    train_dataset = XrayDataset(Constants.ROOT_PATH,is_train=True)
    test_dataset = XrayDataset(Constants.ROOT_PATH,is_train=False)

    train_loader = DataLoader(train_dataset,batch_size=32,shuffle=True,num_workers=4)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=4)

    model = Autoencoder()
    train_losses, test_losses = train_autoencoder(
        model = model,
        lr = 1e-3,
        train_loader = train_loader,
        test_loader = test_loader,
        num_epochs = 100,
        device = device
    )
