#!/bin/bash
# PDF生成脚本 for FUND-FOP-047

# 设置基础变量
PAPER_ID="FUND-FOP-047"
PAPER_TITLE="Golden Ratio φ, e, π and Fine Structure Constant α: Collapse Breathing Proportions"
AUTHORS="Haobo Ma and Wen Niu"
DATE=$(date +%Y-%m-%d)
PAPER_DIR="$(pwd)"
VERSION="v38.0"

# 创建输出目录
mkdir -p submission_package/latex_pdf

echo "===================================================="
echo "生成 $PAPER_ID PDF 文件"
echo "标题: $PAPER_TITLE"
echo "作者: $AUTHORS"
echo "日期: $DATE"
echo "===================================================="

# 转换主要文档
echo "转换 manuscript.md 为 PDF..."
pandoc \
  --standalone \
  --from markdown \
  --template=../../common/templates/springer_article.tex \
  --variable title="$PAPER_TITLE" \
  --variable author="$AUTHORS" \
  --variable date="$DATE" \
  --variable version="$VERSION" \
  --variable documentclass=article \
  --variable fontsize=11pt \
  --variable geometry:margin=1in \
  --variable linkcolor=blue \
  --variable urlcolor=blue \
  --variable lang=en-US \
  --citeproc \
  --bibliography=references.md \
  --pdf-engine=xelatex \
  --output=submission_package/latex_pdf/manuscript.pdf \
  manuscript.md

echo "主要文档 PDF 生成完成。"

# 转换补充材料
echo "转换补充材料为 PDF..."
find supplementary -name "*.md" | while read file; do
  filename=$(basename "$file" .md)
  echo "处理 $file..."
  
  pandoc \
    --standalone \
    --from markdown \
    --template=../../common/templates/springer_supplement.tex \
    --variable title="Supplementary Material: $filename" \
    --variable author="$AUTHORS" \
    --variable date="$DATE" \
    --variable version="$VERSION" \
    --variable documentclass=article \
    --variable fontsize=11pt \
    --variable geometry:margin=1in \
    --variable linkcolor=blue \
    --variable urlcolor=blue \
    --pdf-engine=xelatex \
    --output="submission_package/latex_pdf/supplementary_${filename}.pdf" \
    "$file"
done

echo "补充材料 PDF 生成完成。"

# 转换提交文档
echo "转换提交文档为 PDF..."
mkdir -p submission_package/latex_pdf/additional_documents

# 处理提交附加文档
find submission_additional_documents -name "*.md" | while read file; do
  filename=$(basename "$file" .md)
  echo "处理 $file..."
  
  pandoc \
    --standalone \
    --from markdown \
    --template=../../common/templates/simple.tex \
    --variable title="$filename" \
    --variable author="$AUTHORS" \
    --variable date="$DATE" \
    --variable version="$VERSION" \
    --variable documentclass=article \
    --variable fontsize=11pt \
    --variable geometry:margin=1in \
    --pdf-engine=xelatex \
    --output="submission_package/latex_pdf/additional_documents/${filename}.pdf" \
    "$file"
done

# 处理其他文档
for file in cover_letter.md highlights.md submission_checklist.md; do
  if [ -f "$file" ]; then
    filename=$(basename "$file" .md)
    echo "处理 $file..."
    
    pandoc \
      --standalone \
      --from markdown \
      --template=../../common/templates/simple.tex \
      --variable title="$filename" \
      --variable author="$AUTHORS" \
      --variable date="$DATE" \
      --variable version="$VERSION" \
      --variable documentclass=article \
      --variable fontsize=11pt \
      --variable geometry:margin=1in \
      --pdf-engine=xelatex \
      --output="submission_package/latex_pdf/${filename}.pdf" \
      "$file"
  fi
done

echo "提交文档 PDF 生成完成。"

# 生成合并版本的补充材料
echo "生成合并版本的补充材料..."
find supplementary -name "*.md" | sort | xargs cat > submission_package/combined_supplementary.md
echo "处理合并的补充材料..."
pandoc \
  --standalone \
  --from markdown \
  --template=../../common/templates/springer_supplement.tex \
  --variable title="Supplementary Materials" \
  --variable author="$AUTHORS" \
  --variable date="$DATE" \
  --variable version="$VERSION" \
  --variable documentclass=article \
  --variable fontsize=11pt \
  --variable geometry:margin=1in \
  --variable linkcolor=blue \
  --variable urlcolor=blue \
  --pdf-engine=xelatex \
  --output="submission_package/latex_pdf/all_supplementary.pdf" \
  submission_package/combined_supplementary.md

echo "合并版本的补充材料生成完成。"

echo "===================================================="
echo "所有 PDF 文件生成完成。文件位于:"
echo "submission_package/latex_pdf/"
echo "===================================================="

# 添加执行权限
chmod +x "$0"
