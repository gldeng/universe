import os
import re
import sys

def extract_referenced_files(markdown_file):
    """从markdown文件中提取所有被引用的文件路径"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配Markdown链接中的文件路径: [text](path)
    referenced_files = re.findall(r'\[.*?\]\((.*?)\)', content)
    
    # 过滤出仅formal_theory目录下的文件引用（排除上级目录引用如../core.md）
    formal_theory_refs = set()
    for ref in referenced_files:
        # 如果是formal_theory目录下的文件，提取文件名
        if 'formal_theory_' in ref and not ref.startswith('../'):
            # 获取链接的基本文件名
            basename = os.path.basename(ref)
            formal_theory_refs.add(basename)
    
    # 调试输出
    print(f"在 {markdown_file} 中找到 {len(formal_theory_refs)} 个引用:")
    for ref in sorted(formal_theory_refs):
        print(f"  - {ref}")
    
    return formal_theory_refs

def get_all_markdown_files(directory):
    """获取指定目录下的所有markdown文件"""
    all_files = []
    for file in os.listdir(directory):
        if file.endswith('.md') and 'formal_theory_' in file:
            all_files.append(file)
    
    # 调试输出
    print(f"\n在目录 {directory} 中找到 {len(all_files)} 个Markdown文件")
    print(f"其中部分文件示例:")
    for file in sorted(all_files)[:10]:  # 只显示前10个文件作为示例
        print(f"  - {file}")
    print("  ...")
    
    return set(all_files)

def main():
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"脚本目录: {script_dir}")
    
    # 假设formal_theory目录与脚本在同一层级
    formal_theory_dir = os.path.join(script_dir, 'formal_theory')
    
    # 如果formal_theory目录不存在，尝试使用当前目录
    if not os.path.exists(formal_theory_dir):
        print(f"目录 {formal_theory_dir} 不存在，使用当前目录")
        formal_theory_dir = os.getcwd()
    
    print(f"使用目录: {formal_theory_dir}")
    
    # formal_theory.md文件路径
    index_file = os.path.join(formal_theory_dir, 'formal_theory.md')
    print(f"索引文件: {index_file}")
    
    # 检查文件是否存在
    if not os.path.exists(index_file):
        print(f"错误：索引文件 {index_file} 不存在!")
        sys.exit(1)
    
    # 获取所有被引用的文件
    referenced_files = extract_referenced_files(index_file)
    
    # 获取目录下的所有markdown文件
    all_md_files = get_all_markdown_files(formal_theory_dir)
    
    # 过滤不需要检查的文件
    exclude_files = {'formal_theory.md', 'formal_theory_core.md', 'formal_theory_en.md'}
    all_md_files = {f for f in all_md_files if f not in exclude_files}
    
    print(f"\n排除特定文件后剩余 {len(all_md_files)} 个需要检查的文件")
    
    # 查找未被索引的文件（排除英文版文件）
    unindexed_files = set()
    for file in all_md_files:
        # 跳过英文版文件（通常以_en.md结尾）
        if file.endswith('_en.md'):
            continue
        
        if file not in referenced_files:
            unindexed_files.add(file)
            print(f"DEBUG: 未索引文件 {file}")
    
    # 输出结果
    if unindexed_files:
        print("\n以下文件在 formal_theory.md 中未被索引:")
        for file in sorted(unindexed_files):
            print(f"- {file}")
        print(f"\n共发现 {len(unindexed_files)} 个未索引的文件。")
    else:
        print("\n所有文件都已在 formal_theory.md 中被索引!")

if __name__ == "__main__":
    main() 