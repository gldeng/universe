#!/bin/bash

# 创建目标目录（如果不存在）
mkdir -p ../latex_pdf

# 运行LaTeX编译过程
echo "Starting Supplementary Materials LaTeX compilation..."
pdflatex -interaction=nonstopmode supplementary.tex
pdflatex -interaction=nonstopmode supplementary.tex

# 检查PDF是否生成
if [ -f "supplementary.pdf" ]; then
    # 移动输出PDF到latex_pdf目录
    cp supplementary.pdf ../latex_pdf/supplementary.pdf
    echo "PDF compilation complete. Output saved to ../latex_pdf/supplementary.pdf"
else
    echo "Error: Supplementary PDF compilation failed. Check log file for errors."
    exit 1
fi 