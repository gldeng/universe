import re
import os
import sys

def convert_math_expressions(text):
    """将文档中的数学表达式格式转换为指定格式"""
    
    # 1. 跳过所有 $` 与 `$ 的情况，不处理
    # 先检查文本中是否已经有 $` 和 `$ 模式
    skip_pattern = r'\$`.*?`\$'
    
    # 将文本分割成需要处理和不需要处理的部分
    parts = []
    last_end = 0
    
    for match in re.finditer(skip_pattern, text, re.DOTALL):
        start, end = match.span()
        # 添加前面需要处理的部分
        if start > last_end:
            parts.append((text[last_end:start], True))
        # 添加不需要处理的部分
        parts.append((text[start:end], False))
        last_end = end
    
    # 添加最后一部分
    if last_end < len(text):
        parts.append((text[last_end:], True))
    
    # 处理需要转换的部分
    result = []
    for part, should_process in parts:
        if should_process:
            # 2. 处理多行数学表达式，将 $$ expr $$ 转为 $` expr `$
            # 匹配多行的 $$ ... $$ 表达式（不包含空行）
            multi_line_pattern = r'(?<!\$)\$\$((?!\n\n)[\s\S]+?)\$\$(?!\$)'
            part = re.sub(multi_line_pattern, r'$`\1`$', part)
            
            # 3. 处理同一行的 $$表达式$$ 转为 $`表达式`$
            # 这里专门处理内联的双美元符表达式
            inline_double_dollar_pattern = r'(?<!\$)\$\$([^\n]*?)\$\$(?!\$)'
            part = re.sub(inline_double_dollar_pattern, r'$`\1`$', part)
            
            # 4和5. 处理 $表达式$ 转为 $`表达式`$（包括各种情况如 $a$ 或 $\djy okk$）
            # 确保不会匹配已经转换的表达式
            single_dollar_pattern = r'(?<!\$)\$([^\$\n`]+?)\$(?!\$)'
            part = re.sub(single_dollar_pattern, r'$`\1`$', part)
        
        result.append(part)
    
    return ''.join(result)

def process_file(file_path):
    """处理单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 转换内容
        new_content = convert_math_expressions(content)
        
        # 内容有变化时才写入
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"已处理文件: {file_path}")
        else:
            print(f"文件无需更改: {file_path}")
            
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")

def process_directory(directory):
    """处理目录中的所有markdown文件"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                file_path = os.path.join(root, file)
                process_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if os.path.isfile(target):
            process_file(target)
        elif os.path.isdir(target):
            process_directory(target)
        else:
            print(f"目标不存在: {target}")
    else:
        print("用法: python math_expr_converter.py <文件或目录路径>")
        print("例如: python math_expr_converter.py ./docs")
        print("      python math_expr_converter.py ./document.md") 