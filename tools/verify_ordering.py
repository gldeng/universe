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

def verify_ordering_in_section(section_text, section_name):
    """验证一个部分内的理论是否按维度从高到低排序"""
    pattern = r'\*\*\[(.*?)\]\((.*?)\)\*\* \(v\d+\.\d+, (D\d+[\+∞]*|D∞)\)'
    theories = re.findall(pattern, section_text)
    
    if not theories:
        print(f"在'{section_name}'部分未找到理论条目")
        return True
    
    dimensions = [theory[2] for theory in theories]
    dimension_numbers = [extract_dimension_number(dim) for dim in dimensions]
    
    # 检查是否按维度从高到低排序
    is_ordered = all(dimension_numbers[i] >= dimension_numbers[i+1] for i in range(len(dimension_numbers)-1))
    
    if not is_ordered:
        print(f"'{section_name}'部分中的理论未按维度从高到低排序:")
        for i in range(len(theories)):
            print(f"  {theories[i][0]} ({dimensions[i]})")
        return False
    
    print(f"'{section_name}'部分中的理论已正确按维度从高到低排序")
    return True

def main():
    """验证formal_theory.md中的所有部分是否按维度从高到低排序"""
    with open('formal_theory/formal_theory.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 通过标题找出各部分
    section_pattern = r'### (.*?)\n\n(.*?)(?=\n### |$)'
    sections = re.findall(section_pattern, content, re.DOTALL)
    
    all_ordered = True
    for section_name, section_text in sections:
        is_ordered = verify_ordering_in_section(section_text, section_name)
        all_ordered = all_ordered and is_ordered
    
    if all_ordered:
        print("\n所有部分都已正确按维度从高到低排序")
    else:
        print("\n存在部分未按维度从高到低排序，请检查上述提示进行修正")

if __name__ == "__main__":
    main() 