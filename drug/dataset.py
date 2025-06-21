import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
from transformers import BertTokenizer


class DrugReviewDataset(Dataset):
    def __init__(self, file_path, max_length=128, is_test=False):

        self.data = pd.read_csv(file_path)
        self.reviews = self.data["review"].values

        if not is_test:
            self.ratings = self.data["rating"].values
            self.labels = self._convert_ratings_to_sentiment(self.ratings)

        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.max_length = max_length
        self.is_test = is_test

    def _convert_ratings_to_sentiment(self, ratings):
        sentiments = []
        for rating in ratings:
            if rating <= 4:
                sentiments.append(0)
            elif rating <= 6:
                sentiments.append(1)
            else:
                sentiments.append(2)
        return np.array(sentiments)

    def __len__(self):
        return len(self.reviews)

    def __getitem__(self, idx):
        review = str(self.reviews[idx])

        encoding = self.tokenizer(
            review,
            add_special_tokens=True,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        item = {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
        }

        if not self.is_test:
            item["label"] = torch.tensor(self.labels[idx], dtype=torch.long)

        return item


def create_data_loader(dataset, batch_size, shuffle=True):
    from torch.utils.data import DataLoader

    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

