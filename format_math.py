import re
import os

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 处理单行的 $XXX$ 转换为 $`XXX`$，但不处理已经是 $`XXX`$ 的情况
    def replace_inline_math(match):
        # 如果已经包含反引号，则不处理
        if '`' in match.group(1):
            return match.group(0)
        return f"$`{match.group(1)}`$"
    
    content = re.sub(r'\$([^$\n]+?)\$', replace_inline_math, content)

    # 2. 确保多行数学表达式前后有空行
    content = re.sub(r'([^\n])\n\$\$', r'\1\n\n$$', content)
    content = re.sub(r'\$\$\n([^\n])', r'$$\n\n\1', content)

    # 3. 将同一行的 $$表达式$$ 转换为多行格式
    def replace_inline_block_math(match):
        return f"\n\n$$\n{match.group(1)}\n$$\n\n"
    
    content = re.sub(r'\$\$([^$\n]+?)\$\$', replace_inline_block_math, content)

    # 4. 将多行的 $$...$$转换为 $`...`$
    def replace_block_math(match):
        # 去除开头和结尾的空白字符
        expr = match.group(1).strip()
        return f"\n\n$`\n{expr}\n`$\n\n"
    
    content = re.sub(r'\$\$\n(.*?)\n\$\$', replace_block_math, content, flags=re.DOTALL)

    # 清理多余的空行（超过2个的空行）
    content = re.sub(r'\n{3,}', '\n\n', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"处理文件: {file_path}")
                process_file(file_path)

if __name__ == "__main__":
    # 获取当前目录
    current_dir = os.getcwd()
    print(f"开始处理目录: {current_dir}")
    process_directory(current_dir)
    print("处理完成！") 