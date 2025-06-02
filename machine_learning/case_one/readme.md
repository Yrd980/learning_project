> [!IMPORTANT]
> PYTHONPATH=. python data/dataset.py

# Tenserboard

- tensorboard --logdir results/autoencoder/tentorboard
- tensorboard --logdir results/cnn/tentorboard

- tensorboard --logdir_spec autoencoder:results/autoencoder/tensorboard,cnn:results/cnn/tensorboard

