#!/bin/bash
# Qwen微调模型评测脚本
# 宇宙本论 v37.5

set -e

if [ -d "../venv" ]; then
  source ../venv/bin/activate
elif [ -d "venv" ]; then
  source venv/bin/activate
fi

axolotl eval config.yaml --input "$1" --output "../output/eval_result.jsonl" 