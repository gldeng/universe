#!/bin/bash

# 创建目标目录（如果不存在）
mkdir -p ../latex_pdf

# 运行LaTeX编译过程
echo "Starting LaTeX compilation for supplementary materials..."
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

# 检查PDF是否生成
if [ -f "main.pdf" ]; then
    # 移动输出PDF到latex_pdf目录
    cp main.pdf ../latex_pdf/supplementary.pdf
    echo "PDF compilation complete. Output saved to ../latex_pdf/supplementary.pdf"
else
    echo "Error: PDF compilation failed. Check log file for errors."
    exit 1
fi 