#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查未被索引的文件工具

此工具用于检查哪些理论文件未被添加到索引文件中，生成JSON格式的报告。

使用方法：
python check_unindexed_files.py --dir ../formal_theory --output unindexed_files.json
"""

import os
import sys
import argparse
import json
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="检查未被索引的文件")
    parser.add_argument("--dir", default="../formal_theory", help="理论文件目录")
    parser.add_argument("--output", default="unindexed_files.json", help="输出JSON文件")
    parser.add_argument("--index", default="../formal_theory.md", help="中文索引文件")
    parser.add_argument("--index-en", default="../formal_theory_en.md", help="英文索引文件")
    return parser.parse_args()

def find_md_files(directory):
    """递归查找所有.md文件"""
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def check_unindexed_files(theory_files, index_file):
    """检查未被索引的文件"""
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            index_content = f.read()
    except Exception as e:
        print(f"读取索引文件 {index_file} 时出错: {e}")
        return []
    
    unindexed_files = []
    
    for file_path in theory_files:
        file_name = os.path.basename(file_path)
        if file_name not in index_content and f"({file_name})" not in index_content:
            unindexed_files.append(file_path)
    
    return unindexed_files

def main():
    args = parse_args()
    
    # 查找所有理论文件
    theory_files = find_md_files(args.dir)
    print(f"找到 {len(theory_files)} 个Markdown文件")
    
    # 筛选中文和英文文件
    cn_files = [f for f in theory_files if not f.endswith("_en.md")]
    en_files = [f for f in theory_files if f.endswith("_en.md")]
    
    print(f"其中中文文件 {len(cn_files)} 个，英文文件 {len(en_files)} 个")
    
    # 检查未索引的中文文件
    unindexed_cn = check_unindexed_files(cn_files, args.index)
    print(f"发现 {len(unindexed_cn)} 个未被索引的中文文件")
    
    # 检查未索引的英文文件
    unindexed_en = check_unindexed_files(en_files, args.index_en)
    print(f"发现 {len(unindexed_en)} 个未被索引的英文文件")
    
    # 生成结果报告
    result = {
        "chinese": [os.path.basename(f) for f in unindexed_cn],
        "english": [os.path.basename(f) for f in unindexed_en]
    }
    
    # 写入JSON文件
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"未索引文件报告已生成: {args.output}")
    
    # 如果有未索引文件，提供一些建议
    if unindexed_cn or unindexed_en:
        print("\n建议将这些文件添加到索引中:")
        
        for file in unindexed_cn:
            base_name = os.path.basename(file)
            print(f"- 添加到中文索引: {base_name}")
        
        for file in unindexed_en:
            base_name = os.path.basename(file)
            print(f"- 添加到英文索引: {base_name}")

if __name__ == "__main__":
    main() 