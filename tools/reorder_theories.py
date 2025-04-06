#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys

def extract_theories_with_dimensions(content):
    """从文件内容中提取理论及其维度信息"""
    theories = []
    
    # 使用正则表达式提取所有理论链接及其维度
    # 匹配形如 [理论名称 [维度: X]](链接) 的模式
    pattern = r'\[([^]]+)(?:\s*\[维度:\s*([^\]]+)\])?\]\(([^)]+)\)'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        title, dimension_str, link = match.groups()
        
        if dimension_str:
            try:
                dimension = float(dimension_str.strip())
            except ValueError:
                # 如果无法解析维度值，则设为0
                dimension = 0
        else:
            dimension = 0
        
        theories.append({
            'title': title,
            'dimension': dimension,
            'link': link,
            'full_match': match.group(0)
        })
    
    return theories

def reorder_theories_in_file(file_path):
    """根据维度重新排序文件中的理论链接"""
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在 {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取所有章节（使用二级标题作为章节分隔）
        sections = re.split(r'(## .*?\n)', content)
        
        for i in range(1, len(sections), 2):
            section_header = sections[i]
            section_content = sections[i+1] if i+1 < len(sections) else ""
            
            # 提取并排序理论
            theories = extract_theories_with_dimensions(section_content)
            if theories:
                theories.sort(key=lambda x: x['dimension'], reverse=True)
                
                # 重建章节内容
                new_section_content = ""
                for theory in theories:
                    new_section_content += f"{theory['full_match']}\n\n"
                
                # 更新章节内容
                sections[i+1] = new_section_content
        
        # 重建文件内容
        new_content = ''.join(sections)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已成功重新排序文件 {file_path} 中的理论")
        return True
    
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    # 修改文件路径，索引文件位于根目录
    file_path = 'formal_theory.md'
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    print(f"正在对文件 {file_path} 中的理论按维度进行重排序...")
    reorder_theories_in_file(file_path)

if __name__ == "__main__":
    main() 