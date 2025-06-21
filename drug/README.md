ref <https://github.com/guangzhaoli/drug-review-sentiment>

# train

python train.py \
    --train_file review/drugsComTrain_raw.csv \
    --val_file review/drugsComTest_raw.csv \
    --model_dir checkpoints \
    --batch_size 32 \
    --epochs 10 \
    --learning_rate 0.001 \
    --max_length 128 \
    --embedding_dim 100 \
    --lstm_units 64 \
    --dropout_rate 0.2 \
    --device cpu

# text inference

python inference.py text \
        --model_path checkpoints/best_model.pth \
        --text "This medicine helped me a lot with minimal side effects." \
        --max_length 128

# file inference

python inference.py file \
  --model_path checkpoints/best_model.pth \
  --file ./review/drugsComTest_raw.csv

# tensorboard

tensorboard --logdir=checkpoints/tensorboard_logs
