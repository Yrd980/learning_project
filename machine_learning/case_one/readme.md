ref https://github.com/guangzhaoli/covid19-xray-classification

> [!IMPORTANT]
> PYTHONPATH=. python data/dataset.py

# Tenserboard

- tensorboard --logdir results/autoencoder/tentorboard
- tensorboard --logdir results/cnn/tentorboard

- tensorboard --logdir_spec autoencoder:results/autoencoder/tensorboard,cnn:results/cnn/tensorboard

# gradio

- python app.py --autoencoder_path results/autoencoder/checkpoints/best_autoencoder.pth  --cnn_path results/cnn/checkpoints/best_cnn.pth --port 7860

