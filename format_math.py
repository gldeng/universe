import re
import os

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 处理单行数学表达式：$XXX$ -> $`XXX`$
    # 使用负向前瞻和负向后顾来避免匹配$$包围的表达式
    content = re.sub(r'(?<!\$)\$([^\$\n]+?)\$(?!\$)', r'$`\1`$', content)
    
    # 处理多行数学表达式：确保$$表达式前后有空行
    lines = content.split('\n')
    processed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == '$$':
            # 如果当前是开始的$$
            # 确保前面有空行
            if processed_lines and processed_lines[-1].strip():
                processed_lines.append('')
            processed_lines.append(line)
            
            # 添加数学表达式内容直到找到结束的$$
            i += 1
            while i < len(lines) and lines[i].strip() != '$$':
                processed_lines.append(lines[i])
                i += 1
            
            if i < len(lines):
                processed_lines.append(lines[i])  # 添加结束的$$
                # 确保后面有空行
                if i + 1 < len(lines) and lines[i + 1].strip():
                    processed_lines.append('')
        else:
            processed_lines.append(line)
        i += 1
    
    content = '\n'.join(processed_lines)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f'处理文件: {file_path}')
                process_file(file_path)

if __name__ == '__main__':
    # 获取当前目录
    current_dir = os.getcwd()
    print(f'开始处理目录: {current_dir}')
    process_directory(current_dir) 