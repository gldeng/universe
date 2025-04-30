#!/bin/bash
# 最终版PDF生成脚本 - FUND-FOP-047
# 完善的PDF生成，支持Unicode字符和数学公式

# 设置基础变量
PAPER_ID="FUND-FOP-047"
PAPER_TITLE="Golden Ratio φ, e, π and Fine Structure Constant α: Collapse Breathing Proportions"
AUTHORS="Haobo Ma and Wen Niu"
DATE=$(date +%Y-%m-%d)
VERSION="v38.0"

# 创建输出目录
mkdir -p final_output
mkdir -p final_output/figures
mkdir -p final_output/supplementary
mkdir -p final_output/additional_documents

echo "======================================================"
echo "生成最终版 $PAPER_ID 文档"
echo "标题: $PAPER_TITLE"
echo "作者: $AUTHORS"
echo "日期: $DATE"
echo "版本: $VERSION"
echo "======================================================"

# 创建临时LaTeX模板，提供Unicode支持
cat > unicode_template.tex << 'EOL'
\documentclass[12pt, a4paper]{article}
\usepackage{fontspec}
\usepackage{unicode-math}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{setspace}
\usepackage{listings}
\usepackage{booktabs}

% 设置Unicode支持
\setmainfont{Times New Roman}
\setmathfont{XITS Math}

% 页面设置
\geometry{margin=1in}

% 超链接设置
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=blue,
    pdftitle={$title$},
    pdfauthor={$author$}
}

% 页眉页脚
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{$title$}
\fancyhead[R]{Universe Ontology $version$}
\fancyfoot[C]{Page \thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% 标题信息
\title{$title$}
\author{$author$}
\date{$date$}

\begin{document}

\begin{titlepage}
\begin{center}
\vspace*{1cm}
{\LARGE\textbf{$title$}\par}
\vspace{1.5cm}
{\large\textbf{$author$}\par}
\vspace{1cm}
{\large $date$\par}
\vspace{1cm}
{\large Version: $version$\par}
\vfill
\end{center}
\end{titlepage}

$body$

\end{document}
EOL

# 转换主要文档 - 多种格式
echo "转换 manuscript.md 为多种格式..."

# 1. 生成HTML版本
echo "生成HTML版本..."
pandoc \
  manuscript.md \
  -o final_output/manuscript.html \
  --standalone \
  --metadata title="$PAPER_TITLE" \
  --metadata author="$AUTHORS" \
  --metadata date="$DATE" \
  --toc \
  --toc-depth=3 \
  --mathjax

# 2. 生成Word文档版本
echo "生成Word文档版本..."
pandoc \
  manuscript.md \
  -o final_output/manuscript.docx \
  --standalone \
  --metadata title="$PAPER_TITLE" \
  --metadata author="$AUTHORS" \
  --metadata date="$DATE" \
  --toc \
  --toc-depth=3 \
  --reference-doc=../../common/templates/reference.docx

# 3. 尝试使用自定义模板生成PDF
echo "使用自定义模板生成PDF版本..."
pandoc \
  manuscript.md \
  -o final_output/manuscript.pdf \
  --standalone \
  --template=unicode_template.tex \
  --variable title="$PAPER_TITLE" \
  --variable author="$AUTHORS" \
  --variable date="$DATE" \
  --variable version="$VERSION" \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3

# 处理图片
echo "处理图片文件..."
cp figures/*.svg final_output/figures/
cp figures/*.png final_output/figures/

# 转换SVG图片为PDF
echo "转换SVG图片为PDF格式..."
for svg in figures/*.svg; do
  if [ -f "$svg" ]; then
    filename=$(basename "$svg" .svg)
    
    # 检测可用的转换工具
    if command -v rsvg-convert &> /dev/null; then
      rsvg-convert -f pdf -o "final_output/figures/${filename}.pdf" "$svg"
    elif command -v convert &> /dev/null; then
      convert "$svg" "final_output/figures/${filename}.pdf"
    fi
  fi
done

# 处理补充材料
echo "处理补充材料..."
for md in supplementary/*.md; do
  if [ -f "$md" ]; then
    filename=$(basename "$md" .md)
    echo "处理 $md..."
    
    # 生成HTML版本
    pandoc \
      "$md" \
      -o "final_output/supplementary/${filename}.html" \
      --standalone \
      --metadata title="Supplementary: $filename" \
      --metadata author="$AUTHORS" \
      --metadata date="$DATE" \
      --mathjax
      
    # 尝试生成PDF版本
    pandoc \
      "$md" \
      -o "final_output/supplementary/${filename}.pdf" \
      --standalone \
      --template=unicode_template.tex \
      --variable title="Supplementary: $filename" \
      --variable author="$AUTHORS" \
      --variable date="$DATE" \
      --variable version="$VERSION" \
      --pdf-engine=xelatex
  fi
done

# 处理其他文档
echo "处理其他文档..."
for file in submission_additional_documents/*.md; do
  if [ -f "$file" ]; then
    filename=$(basename "$file" .md)
    echo "处理 $file..."
    
    # 生成HTML版本
    pandoc \
      "$file" \
      -o "final_output/additional_documents/${filename}.html" \
      --standalone \
      --metadata title="$filename" \
      --metadata author="$AUTHORS" \
      --metadata date="$DATE"
      
    # 尝试生成PDF版本  
    pandoc \
      "$file" \
      -o "final_output/additional_documents/${filename}.pdf" \
      --standalone \
      --template=unicode_template.tex \
      --variable title="$filename" \
      --variable author="$AUTHORS" \
      --variable date="$DATE" \
      --variable version="$VERSION" \
      --pdf-engine=xelatex
  fi
done

# 尝试创建组合版本
echo "创建组合版本..."
COMBINED_HTML="final_output/combined_manuscript.html"
echo "<html><head><title>$PAPER_TITLE</title></head><body>" > $COMBINED_HTML
echo "<h1>$PAPER_TITLE</h1>" >> $COMBINED_HTML
echo "<h2>Author: $AUTHORS</h2>" >> $COMBINED_HTML
echo "<h3>Date: $DATE (Version: $VERSION)</h3>" >> $COMBINED_HTML
echo "<hr>" >> $COMBINED_HTML

# 添加主文档
cat final_output/manuscript.html | sed -n '/<body>/,/<\/body>/p' | sed '1d;$d' >> $COMBINED_HTML

# 添加补充材料
for html in final_output/supplementary/*.html; do
  if [ -f "$html" ]; then
    echo "<hr><h2>Supplementary Material: $(basename "$html" .html)</h2>" >> $COMBINED_HTML
    cat "$html" | sed -n '/<body>/,/<\/body>/p' | sed '1d;$d' >> $COMBINED_HTML
  fi
done

echo "</body></html>" >> $COMBINED_HTML

# 尝试合并PDF（如果有工具）
if command -v pdfunite &> /dev/null && [ -f "final_output/manuscript.pdf" ]; then
  PDF_LIST=("final_output/manuscript.pdf")
  
  for pdf in final_output/supplementary/*.pdf; do
    if [ -f "$pdf" ]; then
      PDF_LIST+=("$pdf")
    fi
  done
  
  if [ ${#PDF_LIST[@]} -gt 1 ]; then
    pdfunite "${PDF_LIST[@]}" "final_output/combined_manuscript.pdf"
    echo "已创建组合PDF: final_output/combined_manuscript.pdf"
  fi
fi

# 将生成的文件复制到提交目录
echo "复制文件到提交目录..."
mkdir -p submission_package/latex_pdf/figures
cp final_output/*.pdf submission_package/latex_pdf/ 2>/dev/null
cp final_output/figures/*.pdf submission_package/latex_pdf/figures/ 2>/dev/null

echo "======================================================"
echo "文档生成完成。文件位于:"
echo "- final_output/ (所有格式)"
echo "- submission_package/latex_pdf/ (PDF文件)"
echo "======================================================"

# 清理临时文件
rm -f unicode_template.tex

# 添加执行权限
chmod +x "$0" 