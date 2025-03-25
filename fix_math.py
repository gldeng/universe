#!/usr/bin/env python3
import re
import sys
import os

def fix_math_expressions(content):
    # 1. 首先找出并保护所有已经是 $`XXX`$ 格式的表达式
    placeholders = {}
    correct_pattern = r'\$`([^`]+?)`\$'
    for i, match in enumerate(re.finditer(correct_pattern, content)):
        placeholder = f"CORRECT_MATH_PLACEHOLDER_{i}"
        placeholders[placeholder] = match.group(0)
        content = content.replace(match.group(0), placeholder, 1)
    
    # 2. 处理跨行的表达式 $$\n表达式\n$$ -> $`\n表达式\n`$
    def replace_multiline(match):
        expr = match.group(1)
        # 检查表达式中是否有空行
        if re.search(r'\n\s*\n', expr):
            # 如果有空行，不修改
            return match.group(0)
        return f"$`\n{expr}`$"
    
    content = re.sub(r'\$\$\n([\s\S]+?)\n\$\$', replace_multiline, content)
    
    # 3. 处理同一行的双美元符号表达式 $$表达式$$ -> $`表达式`$
    content = re.sub(r'\$\$([^\$\n]+?)\$\$', r'$`\1`$', content)
    
    # 4. 最后处理单行表达式 $XXX$ -> $`XXX`$
    content = re.sub(r'\$([^\$\n]+?)\$', r'$`\1`$', content)
    
    # 5. 还原所有占位符
    for placeholder, original in placeholders.items():
        content = content.replace(placeholder, original)
    
    return content

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        modified_content = fix_math_expressions(content)
        
        if content != modified_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
            print(f"已更新文件: {file_path}")
        else:
            print(f"文件无变化: {file_path}")
            
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                process_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isfile(path) and path.endswith('.md'):
            process_file(path)
        elif os.path.isdir(path):
            process_directory(path)
        else:
            print("提供的路径不是有效的Markdown文件或目录")
    else:
        print("用法: python fix_math.py <文件路径或目录路径>") 