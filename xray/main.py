import os
import torch
from torch.utils.data import DataLoader
import argparse
from data.dataset import XrayDataset
from models.autoencoder import Autoencoder
from models.cnn import CNN
from utils import load_config
from train_autoencoder import train_autoencoder
from train_cnn import train_cnn


def parse_args():
    parser = argparse.ArgumentParser(description="Run the machine learning case one.")

    parser.add_argument(
        "--config", type=str, default="config.yaml", help="config path"
    )

    parser.add_argument(
        "--data_dir",type=str,default="dataset",help="data path"
    )

    parser.add_argument(
        "--train_autoencoder", action="store_true",help="train autoencoder"
    )

    parser.add_argument(
        "--train_cnn", action="store_true", help="train CNN model"
    )

    parser.add_argument(
        "--autoencoder_dir", type=str, default="results/autoencoder",help="directory to save autoencoder model"
    )

    parser.add_argument(
        "--cnn_dir", type=str, default="results/cnn", help="directory to save CNN model"
    )

    parser.add_argument(
        "--ae_epochs", type=int , default=None,help="number of epochs for autoencoder training"
    )

    parser.add_argument(
        "--ae_batch_size", type=int , default=None,help="batch size for autoencoder training"
    )

    parser.add_argument(
        "--ae-lr", type=float, default=None, help="learning rate for autoencoder training"
    )

    parser.add_argument(
        "--cnn_epochs", type=int, default=None, help="number of epochs for CNN training"
    )

    parser.add_argument(
        "--cnn_batch_size", type=int, default=None, help="batch size for CNN training"
    )

    parser.add_argument(
        "--cnn_lr", type=float, default=None, help="learning rate for CNN training"
    )

    parser.add_argument(
        "--noise_factor", type=float, default=0.3, help="noise factor for data augmentation"
    )

    parser.add_argument(
        "--device", type=str,choices=["cpu", "cuda"], default="cuda",help="device to use for training (cpu or cuda)"
    )

    parser.add_argument(
        "--seed", type=int, default=42,help="random seed for reproducibility"
    )

    parser.add_argument(
        "--resume_autoencoder", type=str,default=None,help="path to resume autoencoder training from a checkpoint"
    )

    parser.add_argument(
        "--resume_cnn", type=str, default=None, help="path to resume CNN training from a checkpoint"
    )

    return parser.parse_args()

def train_phase_autoencoder(args,config,device,train_loader,test_loader):
    print("=== start training autoencoder ===")

    os.makedirs(args.autoencoder_dir, exist_ok=True)
    os.makedirs(os.path.join(args.autoencoder_dir, "checkpoints"), exist_ok=True)

    autoencoder = Autoencoder()

    if args.resume_autoencoder:
        print(f'Resuming autoencoder training from {args.resume_autoencoder}')
        autoencoder.load_state_dict(
            torch.load(args.resume_autoencoder, map_location=device)
        )

    autoencoder_history = train_autoencoder(
        model=autoencoder,
        lr=config["training"]["learning_rate"],
        train_loader=train_loader,
        test_loader=test_loader,
        num_epochs=config["training"]["num_epochs"],
        device=device,
        output_dir=args.autoencoder_dir
    )

    return autoencoder_history

def train_phase_cnn(args,config,device,train_loader,test_loader,autoencoder):
    print("=== cnn training phase ===")

    os.makedirs(args.cnn_dir, exist_ok=True)
    os.makedirs(os.path.join(args.cnn_dir, "checkpoints"), exist_ok=True)

    cnn_model = CNN()

    if args.resume_cnn:
        print(f'Resuming CNN training from {args.resume_cnn}')
        cnn_model.load_state_dict(
            torch.load(args.resume_cnn, map_location=device)
        )

    cnn_history = train_cnn(
        cnn_model=cnn_model,
        autoencoder=autoencoder,
        lr=config["training"]["learning_rate"],
        train_loader=train_loader,
        test_loader=test_loader,
        num_epochs=config["training"]["num_epochs"],
        device=device,
        output_path=args.cnn_dir,
        noise_factor=args.noise_factor
    )

    return cnn_history

def main():
    args = parse_args()

    torch.manual_seed(args.seed)

    config = load_config(args.config)

    ae_config = config.copy()
    cnn_config = config.copy()

    if args.ae_epochs is not None:
        ae_config["training"]["num_epochs"] = args.ae_epochs
    if args.ae_batch_size is not None:
        ae_config["training"]["batch_size"] = args.ae_batch_size
    if args.ae_lr is not None:
        ae_config["training"]["learning_rate"] = args.ae_lr

    if args.cnn_epochs is not None:
        cnn_config["training"]["num_epochs"] = args.cnn_epochs
    if args.cnn_batch_size is not None:
        cnn_config["training"]["batch_size"] = args.cnn_batch_size
    if args.cnn_lr is not None:
        cnn_config["training"]["learning_rate"] = args.cnn_lr

    if args.device == "cuda" and not torch.cuda.is_available():
        print("CUDA is not available. Using CPU instead.")
        device = torch.device("cpu")
    else:
        device = args.device
    print("Using device:", device)


    if args.train_autoencoder:
        train_dataset_ae = XrayDataset(root_dir=args.data_dir,is_train=True)
        test_dataset_ae = XrayDataset(root_dir=args.data_dir,is_train=False)

        train_loader_ae = DataLoader(
            train_dataset_ae,
            batch_size=ae_config["training"]["batch_size"],
            shuffle=True
        )

        test_loader_ae = DataLoader(
            test_dataset_ae,
            batch_size=ae_config["training"]["batch_size"],
            shuffle=False
        )

        print("\n === autoencoder training phase === \n")
        print(f"Epochs: {ae_config['training']['num_epochs']}")
        print(f"Batch Size: {ae_config['training']['batch_size']}")
        print(f"Learning Rate: {ae_config['training']['learning_rate']}\n")

        autoencoder = train_phase_autoencoder(
            args, ae_config, device, train_loader_ae, test_loader_ae
        )
    else:
        autoencoder = Autoencoder()
        autoencoder_path = args.autoencoder_dir
        if os.path.exists(autoencoder_path):
            print(f'Loading autoencoder from {autoencoder_path}')
            autoencoder.load_state_dict(
                torch.load(autoencoder_path, map_location=device)
            )
        else:
            raise FileNotFoundError(
                        f'no pretrained autoencoder found at {autoencoder_path}'
                    )

       
    if args.train_cnn:
        train_dataset_cnn = XrayDataset(root_dir=args.data_dir, is_train=True)
        test_dataset_cnn = XrayDataset(root_dir=args.data_dir, is_train=False)

        train_loader_cnn = DataLoader(
            train_dataset_cnn,
            batch_size=cnn_config["training"]["batch_size"],
            shuffle=True,
        )
        test_loader_cnn = DataLoader(
            test_dataset_cnn,
            batch_size=cnn_config["training"]["batch_size"],
            shuffle=False,
        )

        print("\n=== CNN Training Configuration ===")
        print(f"Epochs: {cnn_config['training']['num_epochs']}")
        print(f"Batch Size: {cnn_config['training']['batch_size']}")
        print(f"Learning Rate: {cnn_config['training']['learning_rate']}")
        print(f"Noise Factor: {args.noise_factor}\n")

        autoencoder.eval()
        train_phase_cnn(
            args, cnn_config, device, train_loader_cnn, test_loader_cnn, autoencoder
        )

if __name__ == "__main__":
    main()



