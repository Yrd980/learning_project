import torch
from torch.utils.data import Dataset
from torchvision import transforms

import os

from PIL import Image
from constants.constants import Constants

class XrayDataset(Dataset):
    def __init__(self,root_dir,is_train=True,transform=None) :
        self.root_dir = root_dir
        self.is_train = is_train
        self.classes = Constants.CLASSES

        self.transform = transform or transforms.Compose([
            transforms.Resize((225, 225)),
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5],std=[0.5])
        ])

        self.data_info = self._gather_data()

    def _gather_data(self):

        data = []
        phase = 'train' if self.is_train else 'test'

        for class_idx, class_name in enumerate(self.classes):
            class_path = os.path.join(self.root_dir, phase, class_name)
            for img_name in os.listdir(class_path):
                if img_name.lower().endswith(('.png','.jpg','.jpeg')):
                    data.append({
                        'path': os.path.join(class_path,img_name),
                        'label': class_idx
                    })

        return data

    def __len__(self):
        return len(self.data_info)

    def __getitem__(self, idx) :
        img_path = self.data_info[idx]['path']
        label = self.data_info[idx]['label']

        image = Image.open(img_path).convert('L')
        image = self.transform(image)

        if self.is_train:
            image = self.add_gaussian_noise(image)
        return image,label

    @staticmethod
    def add_gaussian_noise(image,noise_level=0.1):
        noise = torch.rand_like(image) * noise_level
        return torch.clamp(image + noise,0,1)


if __name__ == "__main__":
    dataset = XrayDataset(root_dir='data/xray', is_train=True)
    print(f"Number of training samples: {len(dataset)}")




                    
