#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

def extract_dimensions_from_formal_theory():
    """从formal_theory.md索引文件中提取各个理论的维度信息"""
    file_dimension_map = {}
    
    # 修改文件路径，索引文件位于根目录
    with open('formal_theory.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有文件维度信息
    pattern = r'\[([^]]+)(?:\s*\[维度:\s*([^\]]+)\])?\]\(([^)]+)\)'
    for match in re.finditer(pattern, content):
        title, dimension, filepath = match.groups()
        filename = os.path.basename(filepath)
        
        if dimension:
            try:
                dimension = float(dimension.strip())
                file_dimension_map[filename] = dimension
            except ValueError:
                print(f"警告: 无法解析维度值 '{dimension}' 对于文件 {filename}")
    
    return file_dimension_map

def update_dimension_in_file(file_path, dimension):
    """在理论文件中更新或添加维度信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经存在维度信息
        if "维度:" in content:
            # 尝试更新现有维度信息
            updated_content = re.sub(r'维度:\s*[\d.-]+', f'维度: {dimension}', content)
        else:
            # 尝试在标题后添加维度信息
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if title_match:
                title_end = title_match.end()
                updated_content = content[:title_end] + f'\n\n**维度: {dimension}**' + content[title_end:]
            else:
                # 无法找到合适位置，在文件开头添加
                updated_content = f'**维度: {dimension}**\n\n' + content
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return True
    except Exception as e:
        print(f"更新文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    # 获取索引文件中的维度信息
    file_dimension_map = extract_dimensions_from_formal_theory()
    
    print(f"从索引文件中提取了 {len(file_dimension_map)} 个文件的维度信息")
    
    # 更新理论文件中的维度
    updated_count = 0
    for filename, dimension in file_dimension_map.items():
        # 构建完整文件路径 - 在formal_theory目录下寻找理论文件
        file_path = os.path.join('formal_theory', filename)
        
        if os.path.exists(file_path):
            if update_dimension_in_file(file_path, dimension):
                updated_count += 1
                print(f"已更新 {filename} 的维度为 {dimension}")
        else:
            print(f"警告: 找不到文件 {file_path}")
    
    print(f"\n更新完成! 已更新 {updated_count}/{len(file_dimension_map)} 个文件的维度信息")

if __name__ == "__main__":
    main() 