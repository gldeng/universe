#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
from pathlib import Path

def find_md_files(directory):
    """递归查找所有.md文件"""
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def fix_en_links(file_path):
    """修复文件中的英文版本链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有中文版到英文版的链接
    base_name = os.path.basename(file_path)
    if not base_name.endswith('_en.md'):
        # 这是中文文件，检查英文链接
        en_filename = base_name.replace('.md', '_en.md')
        en_filepath = os.path.join(os.path.dirname(file_path), en_filename)
        
        # 检查文件是否包含英文版本的链接
        en_link_pattern = r'\[English Version\]\((.*?)\)'
        en_links = re.findall(en_link_pattern, content)
        
        if en_links:
            # 已有英文链接，检查是否需要修复
            for link in en_links:
                if link != en_filename and os.path.exists(en_filepath):
                    # 需要修复链接
                    new_content = re.sub(en_link_pattern, f'[English Version]({en_filename})', content)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    return True, f"修复了 {base_name} 中的英文版本链接: {link} -> {en_filename}"
        else:
            # 没有英文链接，但存在对应的英文文件，添加链接
            if os.path.exists(en_filepath):
                # 在文件顶部添加英文版本链接
                header_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
                if header_match:
                    header_pos = header_match.end()
                    new_content = content[:header_pos] + f'\n\n[English Version]({en_filename})' + content[header_pos:]
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    return True, f"添加了 {base_name} 中的英文版本链接: {en_filename}"
    
    return False, "无需修复"

def fix_chinese_links(file_path):
    """修复英文文件中的中文版本链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有英文版到中文版的链接
    base_name = os.path.basename(file_path)
    if base_name.endswith('_en.md'):
        # 这是英文文件，检查中文链接
        cn_filename = base_name.replace('_en.md', '.md')
        cn_filepath = os.path.join(os.path.dirname(file_path), cn_filename)
        
        # 检查文件是否包含中文版本的链接
        cn_link_pattern = r'\[Chinese Version\]\((.*?)\)'
        cn_links = re.findall(cn_link_pattern, content)
        
        if cn_links:
            # 已有中文链接，检查是否需要修复
            for link in cn_links:
                if link != cn_filename and os.path.exists(cn_filepath):
                    # 需要修复链接
                    new_content = re.sub(cn_link_pattern, f'[Chinese Version]({cn_filename})', content)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    return True, f"修复了 {base_name} 中的中文版本链接: {link} -> {cn_filename}"
        else:
            # 没有中文链接，但存在对应的中文文件，添加链接
            if os.path.exists(cn_filepath):
                # 在文件顶部添加中文版本链接
                header_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
                if header_match:
                    header_pos = header_match.end()
                    new_content = content[:header_pos] + f'\n\n[Chinese Version]({cn_filename})' + content[header_pos:]
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    return True, f"添加了 {base_name} 中的中文版本链接: {cn_filename}"
    
    return False, "无需修复"

def main():
    if len(sys.argv) < 2:
        print("用法: python fix_critical_links.py <目录路径>")
        sys.exit(1)
        
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"错误: '{directory}' 不是一个有效的目录")
        sys.exit(1)
    
    print(f"开始修复目录 '{directory}' 中的关键链接...")
    
    md_files = find_md_files(directory)
    print(f"找到 {len(md_files)} 个Markdown文件")
    
    fixed_en_count = 0
    fixed_cn_count = 0
    
    for file_path in md_files:
        # 修复中文文件中的英文版本链接
        fixed_en, en_msg = fix_en_links(file_path)
        if fixed_en:
            fixed_en_count += 1
            print(en_msg)
        
        # 修复英文文件中的中文版本链接
        fixed_cn, cn_msg = fix_chinese_links(file_path)
        if fixed_cn:
            fixed_cn_count += 1
            print(cn_msg)
    
    print(f"\n修复完成!")
    print(f"修复了 {fixed_en_count} 个中文到英文版本的链接")
    print(f"修复了 {fixed_cn_count} 个英文到中文版本的链接")

if __name__ == "__main__":
    main() 