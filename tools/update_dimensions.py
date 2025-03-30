#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

def extract_dimensions_from_formal_theory():
    """从formal_theory.md文件中提取文件名与维度的映射"""
    file_dimension_map = {}
    pattern = r'\*\*\[(.*?)\]\((.*?)\)\*\* \(v\d+\.\d+, (D\d+[\+∞]*)\)'
    
    with open('formal_theory/formal_theory.md', 'r', encoding='utf-8') as f:
        content = f.read()
        
    matches = re.findall(pattern, content)
    for match in matches:
        title, file_path, dimension = match
        # 提取文件名（去掉路径）
        file_name = os.path.basename(file_path)
        file_dimension_map[file_name] = dimension
    
    return file_dimension_map

def update_file_with_dimension(file_path, dimension):
    """更新文件，在标题中添加维度标注"""
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查文件是否已经包含维度标注
    if re.search(r'维度：D\d+[\+∞]*', content[:200]):
        print(f"文件已包含维度标注: {file_path}")
        return False
    
    # 查找标题行并添加维度信息
    title_pattern = r'^# (.*?) v(\d+\.\d+)$'
    updated_content = re.sub(title_pattern, f'# \\1 v\\2（维度：{dimension}）', content, count=1, flags=re.MULTILINE)
    
    if content == updated_content:
        print(f"未能在文件中找到标题行: {file_path}")
        return False
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"已更新文件: {file_path} 维度: {dimension}")
    return True

def main():
    # 提取维度映射
    file_dimension_map = extract_dimensions_from_formal_theory()
    print(f"从formal_theory.md中提取了{len(file_dimension_map)}个维度映射")
    
    # 更新文件
    base_path = 'formal_theory/'
    updated_count = 0
    
    for file_name, dimension in file_dimension_map.items():
        file_path = os.path.join(base_path, file_name)
        if update_file_with_dimension(file_path, dimension):
            updated_count += 1
    
    print(f"总共更新了{updated_count}个文件")

if __name__ == "__main__":
    main() 