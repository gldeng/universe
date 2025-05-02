#!/bin/bash
# Qwen微调模型推理脚本
# 宇宙本论 v37.5

set -e

if [ -d "../venv" ]; then
  source ../venv/bin/activate
elif [ -d "venv" ]; then
  source venv/bin/activate
fi

axolotl infer config.yaml --input "$1" --output "../output/infer_result.jsonl" 