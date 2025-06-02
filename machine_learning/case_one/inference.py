import torch
import argparse
from models.autoencoder import Autoencoder
from models.cnn import CNN
from torchvision import transforms
from utils import load_config
from constants.constants import Constants
from PIL import Image

def parse_args():
    parser = argparse.ArgumentParser(description='Inference script for X-ray image classification')

    parser.add_argument(
        '--autoencoder_path', type=str, required=True,help='Path to the trained autoencoder model'
    )

    parser.add_argument(
        '--cnn_path', type=str, required=True, help='Path to the trained CNN model'
    )

    parser.add_argument(
        '--image_path', type=str, required=True, help='Path to the input X-ray image'
    )

    parser.add_argument(
        '--config', type=str, default='config.yaml', help='Path to the configuration file'
    )

    parser.add_argument(
        '--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu', help='Device to run the inference on (cpu or cuda)'
    )

def load_models(args):

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    autoencoder = Autoencoder().to(device)
    cnn_model = CNN().to(device)

    autoencoder.load_state_dict(torch.load(args.autoencoder_path, map_location=device))
    cnn_model.load_state_dict(torch.load(args.cnn_path, map_location=device))

    autoencoder.eval()
    cnn_model.eval()

    return autoencoder,cnn_model

def preprocess_image(image_path, config):
    img = Image.open(image_path).convert('L')

    preprocess_config = config['data']['preprocess']
    transform_list = [
        transforms.Resize(preprocess_config['resize_size']),
        transforms.ToTensor(),
    ]
    if preprocess_config.get('normalize',False):
        transform_list.append(
            transforms.Normalize(
                mean=preprocess_config['mean'],
                std=preprocess_config['std']
            )
        )
    transform = transforms.Compose(transform_list)

    img_tensor = transform(img).unsqueeze(0)
    return img_tensor

def main():
    args = parse_args()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    config = load_config(args.config)

    autoencoder, cnn_model = load_models(args)

    input_tensor = preprocess_image(args.image_path, config).to(device)

    with torch.no_grad():
        denoised_image = autoencoder(input_tensor)

        output = cnn_model(denoised_image)
        probabilities = torch.softmax(output, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1)

    class_names = Constants.CLASS_NAMES

    print(f"Probabilities: {probabilities.cpu().numpy()[0]}")
    print(f"Predicted class: {class_names[predicted_class]}")


if __name__ == "__main__":
    main()
