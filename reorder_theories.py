#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

def extract_dimension_number(dimension):
    """从维度字符串中提取数字，用于排序"""
    if dimension == "D∞":
        return float('inf')
    
    match = re.search(r'D(\d+)', dimension)
    if match:
        return int(match.group(1))
    
    return -1

def reorder_section(section_text, section_name):
    """重新排序一个部分内的理论，确保按维度从高到低排序"""
    pattern = r'- \*\*\[(.*?)\]\((.*?)\)\*\* \(v(\d+\.\d+), (D\d+[\+∞]*|D∞)\) - (.*?)(?=\n- \*\*|\n\n|$)'
    theories = re.findall(pattern, section_text, re.DOTALL)
    
    if not theories:
        return section_text
    
    # 按维度从高到低排序
    sorted_theories = sorted(theories, key=lambda x: extract_dimension_number(x[3]), reverse=True)
    
    # 重建部分文本
    new_section_text = re.sub(pattern, '', section_text, flags=re.DOTALL)
    for theory in sorted_theories:
        theory_text = f"- **[{theory[0]}]({theory[1]})** (v{theory[2]}, {theory[3]}) - {theory[4]}"
        new_section_text += theory_text + "\n"
    
    return new_section_text.strip()

def reorder_theories_in_file(file_path):
    """重新排序文件中各部分的理论条目"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 通过标题找出各部分
    section_pattern = r'(### .*?\n\n)(.*?)(?=\n### |$)'
    
    def replace_section(match):
        section_header = match.group(1)
        section_body = match.group(2)
        section_name = section_header.strip().replace('### ', '')
        new_section_body = reorder_section(section_body, section_name)
        return section_header + new_section_body
    
    new_content = re.sub(section_pattern, replace_section, content, flags=re.DOTALL)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已更新文件: {file_path}")
    return True

def main():
    """重新排序formal_theory.md中的理论条目"""
    file_path = 'formal_theory/formal_theory.md'
    reorder_theories_in_file(file_path)
    print(f"已完成对{file_path}的重新排序")

if __name__ == "__main__":
    main() 