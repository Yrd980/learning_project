import torch
from torch.utils.data import DataLoader
from torch import nn, optim
from dataset import KCDataset
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from util.plot import plot_model

import warnings

warnings.filterwarnings("ignore")


class LMConfig(nn.Module):
    def __init__(self):
        super(LMConfig, self).__init__()

        self.layer = nn.Sequential(
            nn.Linear(21, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        x = self.layer(x)
        return x


def nural_networks(file_path):

    accuracy_list, precision_list, recall_list, f1_list = [], [], [], []
    decive = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = LMConfig().to(decive)

    opt = optim.Adam(model.parameters())

    bceloss = nn.BCELoss(reduction="mean")

    train_datasets = KCDataset(datafile=file_path, isTrain=True)
    test_datasets = KCDataset(datafile=file_path, isTrain=False)

    train_dataloader = DataLoader(train_datasets, batch_size=50, shuffle=True)
    test_dataloader = DataLoader(test_datasets, batch_size=50, shuffle=True)

    for epoch in range(1001):
        model.train()
        train_losses = []
        for i, (data, target) in enumerate(train_dataloader):
            data, target = data.to(decive), target.to(decive)

            pred = model(data)

            loss = bceloss(pred, target)

            opt.zero_grad()
            loss.requires_grad_(True)
            loss.backward()
            opt.step()

            train_losses.append(loss)

        epoch_losses = torch.mean(torch.tensor(train_losses))
        print("epoch {} train_losses = {}".format(epoch, epoch_losses))

        if epoch % 100 == 0:
            model.eval()

            accuracy_s, precision_s, recall_s, f1_s = [], [], [], []
            for i, (data, target) in enumerate(test_dataloader):
                data, target = data.to(decive), target.to(decive)

                pred = model(data)

                threshold = 0.5

                pred = (pred >= threshold).float()

                target, pred = target.detach().cpu(), pred.detach().cpu()

                accuracy, precision, recall, f1 = ret_calculate(target, pred)
                accuracy_s.append(accuracy)
                precision_s.append(precision)
                recall_s.append(recall)
                f1_s.append(f1)

            accuracy_p = torch.mean(torch.tensor(accuracy_s))
            precision_p = torch.mean(torch.tensor(precision_s))
            recall_p = torch.mean(torch.tensor(recall_s))
            f1_p = torch.mean(torch.tensor(f1_s))

            if epoch != 0:
                accuracy_list.append(accuracy_p)
                precision_list.append(precision_p)
                recall_list.append(recall_p)
                f1_list.append(f1_p)
            print(
                "----accuracy = {}, ----precision = {}, ----recall = {}, ----f1 = {}".format(
                    accuracy_p, precision_p, recall_p, f1_p
                )
            )
    return accuracy_list, precision_list, recall_list, f1_list


def ret_calculate(target, prediction):

    accuracy = accuracy_score(target, prediction)
    precision = precision_score(target, prediction)
    recall = recall_score(target, prediction)
    f1 = f1_score(target, prediction)

    return accuracy, precision, recall, f1


if __name__ == "__main__":
    filePath = "data/KC2.csv"
    accuracy_list, precision_list, recall_list, f1_list = nural_networks(filePath)
    plot_model(
        "Neural Networks", accuracy_list, precision_list, recall_list, f1_list
    )
    print("Accuracy:", accuracy_list)
    print("Precision:", precision_list)
    print("Recall:", recall_list)
    print("F1 Score:", f1_list)
