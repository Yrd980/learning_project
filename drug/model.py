import torch
import torch.nn as nn


class SentimentModel(nn.Module):
    def __init__(self, config):
        super(SentimentModel, self).__init__()
        self.config = config
        self.embedding = nn.Embedding(
            num_embeddings=config.vocab_size,
            embedding_dim=config.embedding_dim,
            padding_idx=0,
        )

        self.lstm = nn.LSTM(
            input_size=config.embedding_dim,
            hidden_size=config.lstm_units,
            batch_first=True,
        )

        self.dropout = nn.Dropout(config.dropout_rate)

        self.fc = nn.Linear(
            in_features=config.lstm_units, out_features=config.num_classes
        )

        self.softmax = nn.Softmax(dim=1)

    def forward(self, x, attention_mask=None):
        embedded = self.embedding(x)

        if attention_mask is not None:
            attention_mask = attention_mask.unsqueeze(-1)
            embedded *= attention_mask

        lstm_out, (hidden, cell) = self.lstm(embedded)

        dropped = self.dropout(hidden[-1])

        logits = self.fc(dropped)
        output = self.softmax(logits)

        return output


def create_model(config):
    model = SentimentModel(config)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)

    return model, criterion, optimizer


class ModelConfig:
    def __init__(self):
        self.vocab_size = 10000
        self.embedding_dim = 100
        self.lstm_units = 64
        self.dropout_rate = 0.2
        self.num_classes = 3
        self.learning_rate = 1e-3
        self.max_len = 128
