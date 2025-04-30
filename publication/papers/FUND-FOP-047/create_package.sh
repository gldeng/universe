#!/bin/bash
# 创建FUND-FOP-047最终提交包

# 设置基础变量
PAPER_ID="FUND-FOP-047"
PAPER_TITLE="Golden Ratio φ, e, π and Fine Structure Constant α: Collapse Breathing Proportions"
AUTHORS="Haobo Ma and Wen Niu"
DATE=$(date +%Y-%m-%d)
VERSION="v38.0"

# 创建最终提交目录
FINAL_DIR="submission_final"
mkdir -p $FINAL_DIR

echo "======================================================"
echo "创建 $PAPER_ID 最终提交包"
echo "标题: $PAPER_TITLE"
echo "作者: $AUTHORS"
echo "日期: $DATE"
echo "版本: $VERSION"
echo "======================================================"

# 创建必要的子目录
mkdir -p $FINAL_DIR/manuscript
mkdir -p $FINAL_DIR/supplementary
mkdir -p $FINAL_DIR/figures
mkdir -p $FINAL_DIR/html
mkdir -p $FINAL_DIR/additional_documents
mkdir -p $FINAL_DIR/source_files

# 复制核心文件
echo "复制核心文件..."

# 复制源文件
cp manuscript.md $FINAL_DIR/source_files/
cp outline.md $FINAL_DIR/source_files/
cp references.md $FINAL_DIR/source_files/
cp cover_letter.md $FINAL_DIR/source_files/
cp highlights.md $FINAL_DIR/source_files/
cp submission_checklist.md $FINAL_DIR/source_files/
cp submission_instructions.md $FINAL_DIR/source_files/

# 复制图片文件
cp -r figures/* $FINAL_DIR/figures/

# 复制补充材料
cp -r supplementary/* $FINAL_DIR/supplementary/

# 复制提交文档
cp -r submission_additional_documents/* $FINAL_DIR/additional_documents/

# 复制已生成的HTML文件
if [ -d "html_output" ]; then
  cp html_output/index.html $FINAL_DIR/html/
  cp html_output/manuscript_standalone.html $FINAL_DIR/html/
  cp html_output/combined.html $FINAL_DIR/html/
  cp -r html_output/css $FINAL_DIR/html/
  cp -r html_output/images $FINAL_DIR/html/
fi

# 复制已生成的PDF文件
if [ -d "pdf_output" ]; then
  cp pdf_output/manuscript.pdf $FINAL_DIR/manuscript/
fi

# 如果PDF文件也存在于submission_package/latex_pdf目录，复制它们
if [ -d "submission_package/latex_pdf" ]; then
  cp submission_package/latex_pdf/*.pdf $FINAL_DIR/manuscript/ 2>/dev/null
  
  # 复制补充PDF（如果存在）
  if [ -d "submission_package/latex_pdf/supplementary" ]; then
    mkdir -p $FINAL_DIR/supplementary/pdf
    cp submission_package/latex_pdf/supplementary/*.pdf $FINAL_DIR/supplementary/pdf/ 2>/dev/null
  fi
fi

# 创建README文件
cat > $FINAL_DIR/README.md << EOL
# ${PAPER_TITLE}

## 提交包说明

本目录包含Golden Ratio φ, e, π and Fine Structure Constant α: Collapse Breathing Proportions论文的完整提交资料。

## 作者
- Haobo Ma (auric@aelf.io) - AELF PTE LTD., Singapore
- Wen Niu (ada@aelf.io) - AELF PTE LTD., Singapore

## 日期
${DATE}

## 版本
${VERSION}

## 目录结构
- manuscript/ - 主要论文文档（PDF格式）
- supplementary/ - 补充材料
- figures/ - 图表和图片
- html/ - HTML格式版本（包含完整数学公式支持）
- additional_documents/ - 提交所需的额外文档
- source_files/ - 源文件（Markdown格式）

## 注意事项
- HTML版本提供最佳的公式渲染效果
- 图表可在figures目录中查看
- 所有文件均基于v38.0版本

## 联系信息
如有任何问题，请联系Haobo Ma (auric@aelf.io)
EOL

# 创建目录清单
echo "创建文件清单..."
find $FINAL_DIR -type f | sort > $FINAL_DIR/file_list.txt

# 创建ZIP归档（如果有zip命令）
if command -v zip &> /dev/null; then
  echo "创建ZIP归档..."
  ZIP_NAME="${PAPER_ID}_submission_${DATE}.zip"
  (cd $FINAL_DIR && zip -r ../$ZIP_NAME .)
  echo "ZIP归档已创建: $ZIP_NAME"
fi

echo "======================================================"
echo "最终提交包已创建。位于:"
echo "- $FINAL_DIR/ (完整提交包)"
if command -v zip &> /dev/null; then
  echo "- $ZIP_NAME (ZIP归档)"
fi
echo "======================================================"

# 添加执行权限
chmod +x "$0" 