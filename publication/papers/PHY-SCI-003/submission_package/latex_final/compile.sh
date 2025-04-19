#!/bin/bash

# 创建目标目录（如果不存在）
mkdir -p ../latex_pdf

# 创建空文件（如果不存在）
for file in methods.tex theory.tex verification.tex discussion.tex conclusion.tex acknowledgments.tex; do
    if [ ! -f "$file" ]; then
        touch "$file"
        echo "Created empty file: $file"
    fi
done

# 运行LaTeX编译过程
echo "Starting LaTeX compilation..."
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

# 检查PDF是否生成
if [ -f "main.pdf" ]; then
    # 移动输出PDF到latex_pdf目录
    cp main.pdf ../latex_pdf/manuscript.pdf
    echo "PDF compilation complete. Output saved to ../latex_pdf/manuscript.pdf"
else
    echo "Error: PDF compilation failed. Check log file for errors."
    exit 1
fi 