import re
import sys
from pathlib import Path

def format_math_expressions(content):
    # 1. 处理单行的 $XXX$ 表达式，但不处理已经是 $`XXX`$ 的情况
    def replace_inline_math(match):
        if '`' not in match.group(1):  # 只处理不包含 ` 的表达式
            return f"$`{match.group(1)}`$"
        return match.group(0)
    
    content = re.sub(r'\$([^$\n]+?)\$(?!\$)', replace_inline_math, content)
    
    # 2. 确保多行数学表达式前后有空行，并处理单行$$表达式$$
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # 处理单行的 $$表达式$$ 情况
        if '$$' in line:
            # 使用正则表达式提取$$之间的内容
            matches = list(re.finditer(r'\$\$(.*?)\$\$', line))
            if matches:
                current_pos = 0
                for match in matches:
                    # 添加$$之前的文本
                    new_lines.append(line[current_pos:match.start()].rstrip())
                    
                    # 添加数学表达式
                    expr = match.group(1).strip()
                    if expr:  # 如果表达式不为空
                        # 确保前面有空行
                        if new_lines and new_lines[-1].strip():
                            new_lines.append('')
                        new_lines.append('$$')
                        new_lines.append(expr)
                        new_lines.append('$$')
                        # 确保后面有空行
                        new_lines.append('')
                    
                    current_pos = match.end()
                
                # 添加最后一个$$后的文本
                if current_pos < len(line):
                    new_lines.append(line[current_pos:].lstrip())
                
                i += 1
                continue
        
        # 处理多行数学表达式
        if line.strip() == '$$':
            # 确保前面有空行
            if new_lines and new_lines[-1].strip():
                new_lines.append('')
            
            new_lines.append(line)  # 添加开始的 $$
            i += 1
            
            # 收集数学表达式直到找到结束的 $$
            while i < len(lines) and lines[i].strip() != '$$':
                new_lines.append(lines[i])
                i += 1
            
            if i < len(lines):
                new_lines.append(lines[i])  # 添加结束的 $$
                # 确保后面有空行
                if i + 1 < len(lines) and lines[i + 1].strip():
                    new_lines.append('')
        else:
            new_lines.append(line)
        i += 1
    
    # 3. 清理空行：删除连续的空行，保留单个空行
    cleaned_lines = []
    for line in new_lines:
        if line.strip() or (cleaned_lines and cleaned_lines[-1].strip()):
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def process_file(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"错误：文件 {file_path} 不存在")
        return
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 处理内容
        new_content = format_math_expressions(content)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"文件 {file_path} 处理完成")
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")

def process_directory(directory):
    path = Path(directory)
    if not path.exists():
        print(f"错误：目录 {directory} 不存在")
        return
    
    # 递归查找所有 .md 文件
    md_files = list(path.rglob('*.md'))
    total_files = len(md_files)
    
    if total_files == 0:
        print("未找到任何 Markdown 文件")
        return
    
    print(f"找到 {total_files} 个 Markdown 文件")
    
    # 处理每个文件
    for i, file_path in enumerate(md_files, 1):
        print(f"[{i}/{total_files}] 处理文件: {file_path}")
        process_file(file_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法: python format_math.py <文件路径或目录路径>")
        sys.exit(1)
    
    target = sys.argv[1]
    if Path(target).is_dir():
        process_directory(target)
    else:
        process_file(target) 