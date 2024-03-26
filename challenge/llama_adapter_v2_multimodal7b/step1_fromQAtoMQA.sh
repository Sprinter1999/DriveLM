LLAMA_WEIGHT=../llama_model_weights

OUTPUT_PATH=debug_nuscenesMQA
# step1: finetuning
ADAPTER_WEIGHT=pre-trained/1bcbffc43484332672092e0024a8699a6eb5f558161aebf98a7c6b1db67224d1_LORA-BIAS-7B.pth
CONFIG=finetune_data_config_nuscenesMQA.yaml #to place the llama-style train data
./exps/finetune_debug_toMQA.sh $LLAMA_WEIGHT $ADAPTER_WEIGHT $CONFIG $OUTPUT_PATH

# step2: inference
#EPOCH=59
#ADAPTER_WEIGHT_FT=$OUTPUT_PATH/checkpoint-${EPOCH}.pth
#ADAPTER_WEIGHT_FT_CFG=$OUTPUT_PATH/checkpoint-${EPOCH}_config.pth
#RAW_PRED_JSON=${PWD}/../llama-adapter-DriveLM-${EPOCH}-backup.json
#python add_config.py --input1 $ADAPTER_WEIGHT --input2 $ADAPTER_WEIGHT_FT --output $ADAPTER_WEIGHT_FT_CFG
#python demo.py --llama_dir $LLAMA_WEIGHT --checkpoint $ADAPTER_WEIGHT_FT_CFG --data ../test_v2.json  --output ${RAW_PRED_JSON}

# fix prediction
#FIX_PRED_JSON=${PWD}/../llama-adapter-DriveLM-${EPOCH}-fix.json
#python fix_prediction.py --input ${RAW_PRED_JSON} --output ${FIX_PRED_JSON}

# step3: eval
#cd ..
#python evaluation.py --root_path1 ${FIX_PRED_JSON} --root_path2 ./test_v1.json