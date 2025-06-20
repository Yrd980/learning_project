import gradio as gr
import torch
import pandas as pd
from model import SentimentModel, ModelConfig
from transformers import BertTokenizer
import logging
import os


class SentimentAnalyzer:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        config = ModelConfig()
        config.vocab_size = self.tokenizer.vocab_size
        self.model = SentimentModel(config).to(self.device)
        checkpoint = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()

    def predict_text(self, text, max_length=128):
        if not text.strip():
            return "please input content"

        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        input_ids = encoding["input_ids"].to(self.device)
        attention_mask = encoding["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)

        probs = probabilities[0].cpu().numpy()
        sentiment_map = {0: "negative", 1: "normal", 2: "positive"}
        prediction = sentiment_map[probs.argmax()]

        result = f"✨ sentiment analysis result：{prediction}\n\n"
        result += "📊 probabilities distribution：\n"
        result += f"negative: {probs[0]:.2%}\n"
        result += f"normal: {probs[1]:.2%}\n"
        result += f"positive: {probs[2]:.2%}"  # 添加情感标签的颜色提示
        color_map = {"negative": "🔴", "normal": "⚪", "positive": "🟢"}
        result = f"{color_map[prediction]} {result}"

        return result

    def predict_file(self, file):
        if file is None:
            return "please upload csv file"

        try:
            df = pd.read_csv(file.name)
            if "review" not in df.columns:
                return "error: csv file must contain 'review' column"

            results = []
            for text in df["review"]:
                encoding = self.tokenizer(
                    str(text),
                    add_special_tokens=True,
                    max_length=128,
                    padding="max_length",
                    truncation=True,
                    return_tensors="pt",
                )
                input_ids = encoding["input_ids"].to(self.device)
                attention_mask = encoding["attention_mask"].to(self.device)

                with torch.no_grad():
                    outputs = self.model(input_ids, attention_mask)
                    _, predicted = torch.max(outputs, 1)
                    results.append(predicted.item())

            # 添加预测结果到DataFrame
            sentiment_map = {0: "negative", 1: "normal", 2: "positive"}
            df["predict_sentiment"] = [sentiment_map[pred] for pred in results]

            # 保存结果
            output_path = "result.csv"
            df.to_csv(output_path, index=False)
            return (
                f"✅ predict finish！result save to {output_path}\n\n📊 sentiment distribution ：\n"
                + f"positive：{(df['predict_sentiment']=='positive').sum()} 条\n"
                + f"normal：{(df['predict_sentiment']=='normal').sum()} \n"
                + f"negative：{(df['predict_sentiment']=='negative').sum()} "
            )
        except Exception as e:
            return f"❌ fail to process file：{str(e)}"



