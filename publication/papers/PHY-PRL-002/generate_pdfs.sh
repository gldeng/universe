#!/bin/bash
# PDF生成脚本 - 将Markdown文件转换为PDF格式

# 显示进度消息
echo "开始生成PHY-PRL-002论文的PDF文件..."

# 创建输出目录结构
mkdir -p pdf_output
mkdir -p pdf_output/supplementary
mkdir -p pdf_output/additional_documents

# 设置pandoc选项 - 使用更通用的字体设置
PANDOC_OPTS="--pdf-engine=xelatex -V colorlinks=true -V linkcolor=blue -V urlcolor=blue -V toccolor=blue"

# 转换主论文
echo "正在转换主论文..."
pandoc manuscript.md -o pdf_output/manuscript.pdf $PANDOC_OPTS

# 转换补充材料
echo "正在转换补充材料..."
for file in supplementary/*.md; do
  filename=$(basename "$file" .md)
  echo "处理: $filename"
  pandoc "$file" -o "pdf_output/supplementary/${filename}.pdf" $PANDOC_OPTS
done

# 转换额外提交文件
echo "正在转换额外提交文件..."
for file in submission_additional_documents/*.md; do
  filename=$(basename "$file" .md)
  echo "处理: $filename"
  pandoc "$file" -o "pdf_output/additional_documents/${filename}.pdf" $PANDOC_OPTS
done

# 创建合并的补充材料PDF
if [ -d "supplementary" ] && [ "$(ls -A supplementary)" ]; then
  echo "正在创建合并的补充材料PDF..."
  
  # 创建临时文件，包含所有补充材料
  tmp_file=$(mktemp)
  echo "# Supplementary Materials" > "$tmp_file"
  echo "" >> "$tmp_file"
  
  # 将所有补充材料文件内容合并到临时文件
  for file in supplementary/*.md; do
    echo "" >> "$tmp_file"
    echo "## $(basename "$file" .md)" >> "$tmp_file"
    echo "" >> "$tmp_file"
    cat "$file" >> "$tmp_file"
    echo "" >> "$tmp_file"
    echo "---" >> "$tmp_file"
    echo "" >> "$tmp_file"
  done
  
  # 转换合并后的文件
  pandoc "$tmp_file" -o "pdf_output/supplementary.pdf" $PANDOC_OPTS
  
  # 删除临时文件
  rm "$tmp_file"
fi

echo "PDF生成完成！文件位于pdf_output目录。"
echo "主论文: pdf_output/manuscript.pdf"
echo "补充材料: pdf_output/supplementary.pdf"
echo "单个补充文件和额外文件位于对应子目录中" 