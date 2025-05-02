# Qwen Small Model Fine-Tuning with Axolotl + QLoRA

【Qwen小模型Axolotl+QLoRA微调项目】

- 兼容宇宙本论 v37.5
- 目标：以Axolotl+QLoRA高效微调Qwen小模型，兼顾推理性能与易用性

---

## 项目简介 | Project Overview

本项目用于基于[Qwen](https://github.com/QwenLM/Qwen)小模型，采用[Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl)和QLoRA方法进行高效微调，适合个人GPU和小型服务器环境。

This project provides a fine-tuning pipeline for Qwen small models using Axolotl and QLoRA, optimized for reasonable inference performance on consumer GPUs and small servers.

---

## 目录结构 | Directory Structure

- `README.md`         —— 项目说明
- `config.yaml`       —— Axolotl微调配置（Qwen+QLoRA）
- `requirements.txt`  —— 依赖包列表
- `data/`             —— 训练数据集（用户自备）
- `output/`           —— 微调输出模型
- `scripts/`          —— 常用脚本（启动、推理、评测等）

---

## 依赖安装 | Installation

```bash
# 推荐使用Python 3.10+
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # 确保axolotl==0.9.0
```

---

## 快速开始 | Quick Start

1. 准备训练数据，放入`data/`目录。
2. 根据需求修改`config.yaml`（已兼容axolotl 0.9.0）。
3. 启动微调：

```bash
axolotl train config.yaml
```

4. 微调模型保存在`output/`目录。

---

## 主要依赖 | Main Dependencies

- axolotl == 0.9.0
- transformers >= 4.35.0
- peft >= 0.7.0
- bitsandbytes >= 0.41.0
- accelerate >= 0.23.0
- qwen >= 1.0.0

---

## 版本号 | Version

宇宙本论 v37.5

---

## 参考链接 | References

- [Qwen 官方仓库](https://github.com/QwenLM/Qwen)
- [Axolotl 官方仓库](https://github.com/OpenAccess-AI-Collective/axolotl)
- [QLoRA 论文](https://arxiv.org/abs/2305.14314)

---

> 本项目遵循宇宙本论理论体系，所有操作以XOR-SHIFT为本体论基础。 