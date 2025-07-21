from torch.utils.data import Dataset
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import TomekLinks
import numpy as np
import pandas as pd
import torch


class KCDataset(Dataset):
    def __init__(
        self,
        datafile: str = "data/KC2.csv",
        isTrain: bool = True,
        test_size: float = 0.3,
    ):
        pd_data = pd.read_csv(datafile)
        pd_data = pd_data.sample(frac=1).reset_index(drop=True)
        count = pd_data.shape[0]

        train_len = int(count * (1 - test_size))

        train_data = pd_data[:train_len]
        test_data = pd_data[train_len:]

        pd_data = train_data if isTrain else test_data

        scaler = StandardScaler()
        scaled = scaler.fit_transform(pd_data.iloc[:, 0:21].to_numpy())
        y = pd_data.iloc[:, 21].to_numpy()

        smote = SMOTE(sampling_strategy="auto", random_state=42)
        X_resampled, y_resampled = smote.fit_resample(scaled, y)
        tl = TomekLinks(sampling_strategy="auto")
        X_resampled, y_resampled = tl.fit_resample(X_resampled, y_resampled)

        self.x = X_resampled
        self.y = (
            np.expand_dims(y_resampled, axis=1)
            if y_resampled.ndim == 1
            else y_resampled
        )

    def __len__(self):
        return self.y.shape[0]

    def __getitem__(self, item):
        data = torch.from_numpy(self.x[item]).float()
        target = torch.from_numpy(self.y[item]).float()

        return data, target


if __name__ == "__main__":

    file_path = "data/KC2.csv"
    train_dataset = KCDataset(datafile=file_path, isTrain=True)
    test_dataset = KCDataset(datafile=file_path, isTrain=False)
    print(len(train_dataset) + len(test_dataset))
