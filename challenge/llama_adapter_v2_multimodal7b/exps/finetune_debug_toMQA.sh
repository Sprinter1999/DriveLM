#!/usr/bin/bash

LLAMA_PATH="$1"
PRETRAINED_PATH="$2" # path to pre-trained checkpoint
CONFIG="$3"
OUTPUT_DIR="$4"
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6
mkdir -p $OUTPUT_DIR

python -u -m torch.distributed.launch --master_port=1112 --nproc_per_node=7 --use_env \
 main_finetune_debug_fromQAtoMQA.py --data_config "$CONFIG" --batch_size 3 \
 --epochs 3 --warmup_epochs 1 --blr 10e-4 --weight_decay 0.02 \
 --llama_path "$LLAMA_PATH" \
 --output_dir "$OUTPUT_DIR" \
 --pretrained_path "$PRETRAINED_PATH" \
 2>&1 | tee "$OUTPUT_DIR"/output_lora.log
