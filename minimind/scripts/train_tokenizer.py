from tokenizers import (
    models,
    pre_tokenizers,
    decoders,
    trainers,
    Tokenizer,
)

import os
import random
import json

random.seed(42)


def train_tokenizer():

    def read_texts_from_jsonl(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                yield data["text"]

    data_path = "../dataset/pretrain_hq.jsonl"
    tokenizer = Tokenizer(models.BPE())
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)

    special_tokens = ["<|endoftext|>", "<|im_start|>", "<|im_end|>"]

    trainer = trainers.BpeTrainer(
        vocab_size=6400,
        special_tokens=special_tokens,
        show_progress=True,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
    )

    texts = read_texts_from_jsonl(data_path)

    tokenizer.train_from_iterator(texts, trainer=trainer)

    tokenizer.decoder = decoders.ByteLevel()

    assert tokenizer.token_to_id("<|endoftext|>") == 0
    assert tokenizer.token_to_id("<|im_start|>") == 1
    assert tokenizer.token_to_id("<|im_end|>") == 2

    tokenizer_dir = "../model/"
    os.makedirs(tokenizer_dir, exist_ok=True)
    tokenizer.save(os.path.join(tokenizer_dir, "tokenizer.json"))
    tokenizer.model.save("../model/")

    config = {
        "add_bos_token": False,
        "add_eos_token": False,
        "add_prefix_space": False,
        "added_tokens_decoder": {
            "0": {
                "content": "<|endoftext|>",
                "lstrip": False,
                "normalized": False,
                "rstrip": False,
                "single_word": False,
                "special": True,
            },
            "1": {
                "content": "<|im_start|>",
                "lstrip": False,
                "normalized": False,
                "rstrip": False,
                "single_word": False,
                "special": True,
            },
            "2": {
                "content": "<|im_end|>",
                "lstrip": False,
                "normalized": False,
                "rstrip": False,
                "single_word": False,
                "special": True,
            },
        },
        "additional_special_tokens": [],
        "bos_token": "<|im_start|>",
        "clean_up_tokenization_spaces": False,
        "eos_token": "<|im_end|>",
        "legacy": True,
        "model_max_length": 32768,
        "pad_token": "<|endoftext|>",
        "sp_model_kwargs": {},
        "spaces_between_special_tokens": False,
        "tokenizer_class": "PreTrainedTokenizerFast",
        "unk_token": "<|endoftext|>",
        "chat_template": "{% if messages[0]['role'] == 'system' %}{% set system_message = messages[0]['content'] %}{{ '<|im_start|>system\\n' + system_message + '<|im_end|>\\n' }}{% else %}{{ '<|im_start|>system\\nYou are a helpful assistant<|im_end|>\\n' }}{% endif %}{% for message in messages %}{% set content = message['content'] %}{% if message['role'] == 'user' %}{{ '<|im_start|>user\\n' + content + '<|im_end|>\\n<|im_start|>assistant\\n' }}{% elif message['role'] == 'assistant' %}{{ content + '<|im_end|>' + '\\n' }}{% endif %}{% endfor %}",
    }

    with open(
        os.path.join(tokenizer_dir, "tokenizer_config.json"), "w", encoding="utf-8"
    ) as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)

    print("Tokenizer training completed and saved")


def eval_tokenizer():
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained("../model/")

    messages = [
        {
            "role": "system",
            "content": "you are excellent chat bot please answer my question",
        },
        {"role": "user", "content": "where are you from"},
        {"role": "assistant", "content": "I'm from earth"},
    ]

    new_prompt = tokenizer.apply_chat_template(messages, tokenize=False)
    print(new_prompt)

    actual_vocab_size = len(tokenizer)
    print("tokenizer actual_vocab_size：", actual_vocab_size)

    model_inputs = tokenizer(new_prompt)
    print("encoder length：", len(model_inputs["input_ids"]))

    input_ids = model_inputs["input_ids"]
    response = tokenizer.decode(input_ids, skip_special_tokens=False)
    print("decoder == origin text：", response == new_prompt)


def main():
    train_tokenizer()
    eval_tokenizer()


if __name__ == "__main__":
    main()
