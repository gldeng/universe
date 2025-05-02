#!/bin/bash
# Axolotl+QLoRA Qwen微调一键启动脚本
# 宇宙本论 v37.5

set -e

if [ -d "../venv" ]; then
  source ../venv/bin/activate
elif [ -d "venv" ]; then
  source venv/bin/activate
fi

axolotl train config.yaml 