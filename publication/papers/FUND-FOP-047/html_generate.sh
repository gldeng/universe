#!/bin/bash
# HTML专注生成脚本 - FUND-FOP-047
# 最终解决方案：创建高质量HTML文档，解决Unicode和数学公式问题

# 设置基础变量
PAPER_ID="FUND-FOP-047"
PAPER_TITLE="Golden Ratio φ, e, π and Fine Structure Constant α: Collapse Breathing Proportions"
AUTHORS="Haobo Ma and Wen Niu"
DATE=$(date +%Y-%m-%d)
VERSION="v38.0"

# 创建输出目录
mkdir -p html_output
mkdir -p html_output/images
mkdir -p html_output/css
mkdir -p html_output/js
mkdir -p html_output/supplementary
mkdir -p submission_package/html

echo "======================================================"
echo "生成高质量HTML版本 $PAPER_ID"
echo "标题: $PAPER_TITLE"
echo "作者: $AUTHORS"
echo "日期: $DATE"
echo "版本: $VERSION"
echo "======================================================"

# 创建CSS样式
cat > html_output/css/style.css << 'EOL'
body {
  font-family: 'Georgia', serif;
  line-height: 1.6;
  color: #333;
  max-width: 1000px;
  margin: 0 auto;
  padding: 1em;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Arial', sans-serif;
  color: #2c3e50;
  margin-top: 1.5em;
}

h1 {
  font-size: 2.2em;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
}

h2 {
  font-size: 1.8em;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
}

a {
  color: #3498db;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

pre, code {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  padding: 0.2em 0.4em;
}

pre {
  padding: 1em;
  overflow-x: auto;
}

blockquote {
  background-color: #f9f9f9;
  border-left: 4px solid #ccc;
  margin: 1em 0;
  padding: 0.5em 1em;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 2em auto;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

.toc {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 1em;
  margin: 1em 0;
}

.figure {
  margin: 2em 0;
  text-align: center;
}

.figure img {
  max-width: 90%;
  border: 1px solid #ddd;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.figure-caption {
  margin-top: 0.5em;
  font-style: italic;
  text-align: center;
}

.meta {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 1em;
  margin: 1em 0;
  font-style: italic;
}

.footnotes {
  border-top: 1px solid #ddd;
  margin-top: 2em;
  padding-top: 1em;
}

.math {
  font-size: 1.1em;
}
EOL

# 生成主HTML文档
echo "生成主文档HTML..."

# 添加额外的HTML头部指定确保MathJax正确加载
cat > html_output/header.html << 'EOL'
<link rel="stylesheet" href="css/style.css">
<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true
  },
  svg: {
    fontCache: 'global'
  },
  options: {
    enableMenu: false
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>
EOL

pandoc \
  manuscript.md \
  -o html_output/index.html \
  -s \
  --metadata title="$PAPER_TITLE" \
  --metadata author="$AUTHORS" \
  --metadata date="$DATE" \
  --include-in-header=html_output/header.html \
  --toc \
  --toc-depth=3 \
  --mathjax \
  --highlight-style=pygments \
  --standalone

# 处理图片
echo "处理图片..."
cp figures/*.svg html_output/images/
cp figures/*.png html_output/images/

# 处理补充材料
echo "处理补充材料..."
for md in supplementary/*.md; do
  if [ -f "$md" ]; then
    filename=$(basename "$md" .md)
    pandoc \
      "$md" \
      -o "html_output/supplementary/${filename}.html" \
      -s \
      --metadata title="Supplementary: $filename" \
      --metadata author="$AUTHORS" \
      --metadata date="$DATE" \
      --include-in-header=html_output/header.html \
      --mathjax \
      --highlight-style=pygments \
      --standalone
  fi
done

# 创建组合版本
echo "创建组合HTML文档..."

# 创建HTML头部
cat > html_output/combined.html << EOL
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${PAPER_TITLE}</title>
  <link rel="stylesheet" href="css/style.css">
  <script>
  MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
      displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
      processEscapes: true,
      processEnvironments: true
    },
    svg: {
      fontCache: 'global'
    }
  };
  </script>
  <script type="text/javascript" id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
  </script>
</head>
<body>
  <header>
    <h1>${PAPER_TITLE}</h1>
    <div class="meta">
      <p><strong>Authors:</strong> ${AUTHORS}</p>
      <p><strong>Date:</strong> ${DATE}</p>
      <p><strong>Version:</strong> ${VERSION}</p>
    </div>
  </header>
  <nav class="toc">
    <h2>Table of Contents</h2>
    <!-- TOC will be inserted here -->
  </nav>
EOL

# 提取并修复主文档内容
pandoc manuscript.md \
  -t html \
  --mathjax \
  | sed 's|src="figures/|src="images/|g' \
  >> html_output/combined.html

# 添加补充材料
echo "<h1>Supplementary Materials</h1>" >> html_output/combined.html

for md in supplementary/*.md; do
  if [ -f "$md" ]; then
    filename=$(basename "$md" .md)
    echo "<h2>$filename</h2>" >> html_output/combined.html
    
    pandoc "$md" \
      -t html \
      --mathjax \
      | sed 's|src="figures/|src="images/|g' \
      >> html_output/combined.html
  fi
done

# 添加页脚与关闭标签
cat >> html_output/combined.html << 'EOL'
  <footer>
    <p>&copy; 2025 AELF PTE LTD. All rights reserved.</p>
  </footer>
  
  <script>
    // 生成目录
    document.addEventListener('DOMContentLoaded', function() {
      const toc = document.querySelector('.toc');
      const headings = document.querySelectorAll('h1:not(:first-child), h2, h3');
      const tocList = document.createElement('ul');
      
      headings.forEach(function(heading, index) {
        const id = 'section-' + index;
        heading.id = id;
        
        const listItem = document.createElement('li');
        const link = document.createElement('a');
        link.href = '#' + id;
        link.textContent = heading.textContent;
        link.style.marginLeft = (heading.tagName.charAt(1) - 1) * 20 + 'px';
        
        listItem.appendChild(link);
        tocList.appendChild(listItem);
      });
      
      toc.appendChild(tocList);
    });
  </script>
</body>
</html>
EOL

# 优化图片引用
echo "修复图片引用路径..."
sed -i'.bak' 's|src="figures/|src="images/|g' html_output/index.html
sed -i'.bak' 's|src="figures/|src="../images/|g' html_output/supplementary/*.html
rm html_output/*.bak
rm html_output/supplementary/*.bak 2>/dev/null

# 创建自包含HTML版本（纯HTML，没有外部依赖）
echo "创建自包含HTML版本..."
pandoc \
  manuscript.md \
  -o html_output/manuscript_standalone.html \
  -s \
  --metadata title="$PAPER_TITLE" \
  --metadata author="$AUTHORS" \
  --metadata date="$DATE" \
  --self-contained \
  --toc \
  --toc-depth=3 \
  --mathjax \
  --highlight-style=pygments \
  --standalone

# 复制到提交目录
echo "复制文件到提交目录..."
cp -r html_output/* submission_package/html/

echo "======================================================"
echo "HTML生成完成。文件位于:"
echo "- html_output/ (HTML文件及资源)"
echo "- html_output/index.html (主HTML文档)"
echo "- html_output/combined.html (完整组合版)"
echo "- html_output/manuscript_standalone.html (自包含版)"
echo "- submission_package/html/ (提交版本)"
echo "======================================================"

# 尝试使用工具启动本地服务器预览HTML
if command -v python3 &> /dev/null; then
  echo "可以通过以下命令在浏览器中预览HTML版本:"
  echo "cd html_output && python3 -m http.server"
fi

# 添加执行权限
chmod +x "$0" 