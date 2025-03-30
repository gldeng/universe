#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import glob
import sys

def extract_dimension_number(dimension):
    """从维度字符串中提取数字，用于排序"""
    if dimension == "无维度":
        return -1
    
    # 移除所有空格
    dimension = dimension.replace(" ", "")
    
    # 处理D∞或者D+∞的情况
    if "∞" in dimension:
        return float('inf')
    
    # 提取纯数字部分
    match = re.search(r'D(\d+)', dimension)
    if match:
        return int(match.group(1))
    
    return -1

def extract_dimension(content):
    """从文件内容中提取维度信息"""
    # 支持更多格式的维度表示
    dimension_patterns = [
        r'[（\(]维度\s*[：:]\s*D\s*([0-9∞\+]+)[）\)]',  # (维度：D1) 或 (维度:D1) 或 (维度：D∞)
        r'维度\s*[：:]\s*D\s*([0-9∞\+]+)',             # 维度：D1 或 维度:D1 或 维度：D∞
        r'[（\(]D\s*([0-9∞\+]+)[）\)]',                # (D1) 或 (D∞)
        r'\bD\s*([0-9∞\+]+)\s*维度',                   # D1维度 或 D∞维度
        r'维度\s*[：:]\s*([0-9∞\+]+)',                 # 维度：1 或 维度:1
    ]
    
    for pattern in dimension_patterns:
        dimension_match = re.search(pattern, content)
        if dimension_match:
            dimension = dimension_match.group(1).strip()
            # 处理数字和维度之间可能的空格
            return f"D{dimension.replace(' ', '')}"
    
    return "无维度"

def extract_dependencies(content):
    """从文件内容中提取依赖的理论"""
    dependencies_pattern = r'依赖理论:(.+?)\n'
    dependencies_match = re.search(dependencies_pattern, content)
    
    if dependencies_match:
        dependencies_text = dependencies_match.group(1)
        links_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(links_pattern, dependencies_text)
        return [link[0] for link in links]
    
    based_on_pattern = r'本文?基于(.+?)版本'
    based_on_match = re.search(based_on_pattern, content)
    
    if based_on_match:
        based_on_text = based_on_match.group(1)
        links_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(links_pattern, based_on_text)
        return [link[0] for link in links]
    
    return []

def analyze_theory_files(directory):
    """分析目录中的所有理论文件，获取维度和依赖关系"""
    files_data = []
    dependency_map = {}
    
    # 获取目录中所有.md文件
    files = glob.glob(os.path.join(directory, "*.md"))
    
    # 创建标题到文件名的映射
    title_to_filename = {}
    
    # 第一遍：收集所有文件信息和标题到文件名的映射
    for file_path in files:
        # 忽略英文版文件
        if file_path.endswith("_en.md"):
            continue
        
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            title_match = re.search(r'# (.+?) v', content)
            title = title_match.group(1) if title_match else filename
            
            dimension = extract_dimension(content)
            dependencies = extract_dependencies(content)
            
            # 保存文件信息
            file_info = {
                "文件名": filename,
                "标题": title,
                "维度": dimension,
                "依赖": dependencies
            }
            
            files_data.append(file_info)
            
            # 添加到标题到文件名的映射
            title_to_filename[title] = filename
            
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}", file=sys.stderr)
    
    # 按维度从高到低排序
    files_data.sort(key=lambda x: extract_dimension_number(x["维度"]), reverse=True)
    
    # 第二遍：构建依赖关系（使用文件名表示）
    for file_info in files_data:
        source_filename = file_info["文件名"]
        dependency_filenames = []
        
        # 将标题形式的依赖转换为文件名形式
        for dep_title in file_info["依赖"]:
            if dep_title in title_to_filename:
                dependency_filenames.append(title_to_filename[dep_title])
        
        # 只有当有依赖时才添加到依赖映射
        if dependency_filenames:
            dependency_map[source_filename] = dependency_filenames
    
    # 计算统计信息
    files_with_dimension = [f for f in files_data if f['维度'] != "无维度"]
    
    return {
        "files": files_data,
        "dependencies": dependency_map,
        "statistics": {
            "total_files": len(files_data),
            "files_with_dependencies": len(dependency_map),
            "files_with_dimension": len(files_with_dimension)
        }
    }

if __name__ == "__main__":
    # 分析形式化理论目录
    directory = "formal_theory"
    result = analyze_theory_files(directory)
    
    # 直接输出JSON到控制台
    print(json.dumps(result, ensure_ascii=False, indent=2)) 