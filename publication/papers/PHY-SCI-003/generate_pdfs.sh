#!/bin/bash
# PDF生成脚本 - PHY-SCI-003
# 将Markdown文件转换为PDF格式

# 创建输出目录
mkdir -p build/pdf
mkdir -p build/pdf/additional_documents
mkdir -p build/pdf/supplementary

echo "=== 开始生成PDF文件 ==="

# 创建临时LaTeX模板
cat > template.tex <<'EOL'
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{fontspec}
\usepackage{unicode-math}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{geometry}

\geometry{margin=1in}

\begin{document}
$body$
\end{document}
EOL

# 转换主要文档
echo "转换manuscript.md到PDF..."
pandoc manuscript.md -o build/pdf/manuscript.pdf --pdf-engine=xelatex --template=template.tex --standalone

# 转换提交附加文档
echo "转换提交附加文档..."
for file in submission_additional_documents/*.md; do
  if [ -f "$file" ]; then
    filename=$(basename "$file" .md)
    echo "  处理: $filename"
    pandoc "$file" -o "build/pdf/additional_documents/${filename}.pdf" --pdf-engine=xelatex --standalone
  fi
done

# 转换补充材料
echo "转换补充材料..."
for file in supplementary/*.md; do
  if [ -f "$file" ]; then
    filename=$(basename "$file" .md)
    echo "  处理: $filename"
    pandoc "$file" -o "build/pdf/supplementary/${filename}.pdf" --pdf-engine=xelatex --template=template.tex --standalone
  fi
done

# 转换其他重要文件
echo "转换其他重要文件..."
for file in references.md cover_letter.md highlights.md outline.md; do
  if [ -f "$file" ]; then
    filename=$(basename "$file" .md)
    echo "  处理: $filename"
    pandoc "$file" -o "build/pdf/${filename}.pdf" --pdf-engine=xelatex --standalone
  fi
done

# 清理临时文件
rm -f template.tex

echo "=== PDF生成完成 ==="
echo "所有PDF文件可在build/pdf/目录中找到"

# 显示生成的PDF文件列表
echo ""
echo "已生成的PDF文件:"
find build/pdf -name "*.pdf" | sort 