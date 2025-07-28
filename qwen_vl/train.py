import os
import sys
from dataclasses import dataclass
from functools import partial
from PIL import Image

import torch
from transformers import (
    TrainingArguments,
    Trainer,
    HfArgumentParser,
)
from transformers.trainer_utils import get_last_checkpoint
import datasets
import swanlab

from utils import load_model, load_processor

device = "cuda:0"


def load_mm_data(select_data):
    all_data_names = [
        "chartqa",
        "finqa",
        "aokvqa",
        # "mimic_cgd",  # bad dataset
        "figureqa",
        "diagram_image_to_text",
        "geomverse",
        "ai2d",
        "iam",
        "infographic_vqa",
        # "localized_narratives",  # bad dataset
        "intergps",
        "hateful_memes",
        "clevr",
        "iconqa",
        "multihiertt",
        "mapqa",
        "datikz",
        # "okvqa", # bad dataset
        "hitab",
        "chart2text",
        # "ocrvqa",  # bad dataset
        # "clevr_math", # bad dataset
        # "nlvr2",  # bad dataset
        "cocoqa",
        "docvqa",
        "dvqa",
    ]

    if select_data == "all":
        select_data = all_data_names
    elif select_data in all_data_names:
        select_data = [select_data]
    else:
        raise f"cannot find {select_data}"

    data_list = []
    for data_name in select_data:
        try:
            data_list.append(
                datasets.load_dataset("data/the_cauldron", data_name)["train"]
            )
        except:
            print(f"bad dataset:{data_name}")
    raw_data = datasets.concatenate_datasets(data_list)
    raw_data = raw_data.train_test_split(64, shuffle=True, seed=training_args.data_seed)
    if select_data == "all":
        raw_data["train"] = raw_data["train"].select(range(60 * 1024))
    return raw_data


def freeze_model(qwen_smvl):
    for _, param in qwen_smvl.model.text_model.named_parameters():
        param.requires_grad = False
    for _, param in qwen_smvl.model.vision_model.named_parameters():
        param.requires_grad = False
    # for _, param in qwen_smvl.lm_head.named_parameters():
    #     param.requires_grad = False
    return qwen_smvl


def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params/(2**20):.2f}M || all params: {all_param/(2**20):.2f}M || trainable%: {100 * trainable_params / all_param}"
    )


def data_collate_fix2k(examples, processor, device, max_length=2048):
    batch_text = []
    batch_image = []
    for example in examples:
        images = example["images"][:1]
        batch_image.append(images)
        image_num = len(images)
        chat_texts = example["texts"][0]
        messages = [
            {
                "role": "user",
                "content": [{"type": "image"}] * image_num
                + [{"type": "text", "text": chat_texts["user"]}],
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": chat_texts["assistant"]}],
            },
        ]
        text = processor.apply_chat_template(
            messages, enable_thinking=False, add_generation_prompt=False
        )

        batch_text.append(text)

    batch = processor(
        text=batch_text,
        images=batch_image,
        max_length=max_length,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
    )
    labels = batch["input_ids"].clone()
    labels[labels == processor.tokenizer.pad_token_id] = -100
    labels[labels == processor.image_token_id] = -100
    batch["labels"] = labels
    return batch.to(device, dtype=torch.bfloat16)


@dataclass
class MyTrainArgs(TrainingArguments):
    train_data = "cocoqa"
    seed = 42
    data_seed = 42
    max_steps = 200
    per_device_train_batch_size = 1
    gradient_accumulation_steps = 4
    dataloader_pin_memory = False
    warmup_ratio = 0.1
    learning_rate = 1e-4
    lr_scheduler_type = "cosine"
    weight_decay = 0.01
    logging_steps = 5
    eval_strategy = "steps"
    eval_steps = 0.125
    save_strategy = "steps"
    save_steps = 0.125
    save_total_limit = 8
    optim = "adamw_torch"
    bf16 = True
    output_dir = f"./model/qwen-smovlm"
    overwrite_output_dir = True
    report_to = "swanlab"
    run_name = "freeze_except_connector_fulldata"
    remove_unused_columns = False
    gradient_checkpointing = False


def main(training_args):

    qwen_smvl_processor = load_processor()
    qwen_smvl = load_model(device)

    qwen_smvl = freeze_model(qwen_smvl)

    print_trainable_parameters(qwen_smvl)

    raw_data = load_mm_data(select_data=training_args.train_data)
    print(f"total data number：{raw_data}")

    collate_fn = partial(
        data_collate_fix2k, processor=qwen_smvl_processor, device=device
    )

    last_checkpoint = None
    if (
        os.path.isdir(training_args.output_dir)
        and not training_args.overwrite_output_dir
    ):
        last_checkpoint = get_last_checkpoint(training_args.output_dir)
        if last_checkpoint is None and len(os.listdir(training_args.output_dir)) > 0:
            raise ValueError(
                f"Output directory ({training_args.output_dir}) already exists and is not empty. "
                "Use --overwrite_output_dir to overcome."
            )
        print(
            f"Checkpoint detected, resuming training at {last_checkpoint}. To avoid this behavior, change "
            "the `--output_dir` or add `--overwrite_output_dir` to train from scratch."
        )

    trainer = Trainer(
        model=qwen_smvl,
        args=training_args,
        train_dataset=raw_data["train"],
        eval_dataset=raw_data["test"],
        data_collator=collate_fn,
    )
    trainer.train(resume_from_checkpoint=last_checkpoint)
    qwen_smvl.save_pretrained(training_args.output_dir)

    with torch.no_grad():
        if trainer.state.is_world_process_zero:
            question = "图中有什么动物？"
            messages = [
                {
                    "role": "system",
                    "content": "使用中文回答所有问题。",
                    # "content": "使用中文回答所有问题，在<think>和</think>中写出思考过程，如果没有思考则为<think> </think>",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {"type": "text", "text": question},
                    ],
                },
            ]
            texts = qwen_smvl_processor.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=False,
                enable_thinking=True,
            )
            print("################# 输入文本 #################")
            print(texts)
            images = [[Image.open("dog.png")]]
            batch = qwen_smvl_processor(
                text=[texts],
                images=images,
                max_length=1024,
                return_tensors="pt",
                paddding_side="left",
                padding=True,
            ).to(qwen_smvl.device, dtype=torch.bfloat16)
            generated_ids = qwen_smvl.generate(
                **batch, do_sample=False, max_new_tokens=256
            )
            model_context = qwen_smvl_processor.batch_decode(
                generated_ids, skip_special_tokens=False
            )
            input_ids_len = batch["input_ids"].shape[1]
            generated_texts = qwen_smvl_processor.batch_decode(
                generated_ids[:, input_ids_len:], skip_special_tokens=True
            )
            print("################# 生成文本 #################")
            print(generated_texts[0])

            table = swanlab.echarts.Table()
            headers = ["输入问题", "模型输出"]
            rows = [[question, generated_texts[0]]]
            table.add(headers, rows)
            swanlab.log(
                {
                    "sample/输入图像": swanlab.Image(images[0][0]),
                    "sample/问题&回复": table,
                    "sample/上下文": swanlab.Text(model_context[0]),
                }
            )


if __name__ == "__main__":
    parser = HfArgumentParser(TrainingArguments)
    if len(sys.argv) == 2 and sys.argv[1].endswith(".yaml"):
        training_args = parser.parse_yaml_file(json_file=os.path.abspath(sys.argv[1]))
    else:
        training_args = parser.parse_args_into_dataclasses()
    main(training_args)
