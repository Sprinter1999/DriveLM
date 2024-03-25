import torch
import argparse

parser = argparse.ArgumentParser(description='Add config to checkpoint')
parser.add_argument('--input1', type=str, default="/path/to/pre-trained/checkpoint.pth", help='path to pre-trained checkpoint')
parser.add_argument('--input2', type=str, default="/path/to/output/checkpoint.pth", help='path to finetuned checkpoint')
parser.add_argument('--output', type=str, default="checkpoint_config.pth", help='path to output file')
args = parser.parse_args()

ckpt1 = torch.load(args.input1)
ckpt2 = torch.load(args.input2)
ckpt2['config'] = ckpt1.get('config', {})
#ckpt2['config'] = ckpt1['config']
torch.save(ckpt2, args.output)