#!/bin/bash
# Qwen微调模型评测脚本
# 宇宙本论 v37.5
# 兼容 axolotl 0.9.0

set -e

if [ -d "../venv" ]; then
  source ../venv/bin/activate
elif [ -d "venv" ]; then
  source venv/bin/activate
fi

axolotl evaluate config.yaml --input "$1" --output "../output/eval_result.jsonl" 