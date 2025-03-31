#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import glob
import sys
import argparse

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
                
            title_match = re.search(r'# (.+?)(?:v|\[)', content)
            title = title_match.group(1).strip() if title_match else filename
            
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

def generate_mermaid_graph(theory_data):
    """根据理论数据生成Mermaid图表代码"""
    # 按维度分组理论
    dimension_groups = {}
    for file_info in theory_data["files"]:
        dim = file_info["维度"]
        if dim not in dimension_groups:
            dimension_groups[dim] = []
        dimension_groups[dim].append(file_info)
    
    # 生成Mermaid图表头部
    mermaid_code = '''```mermaid
%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'nodeBorder': '#333',
      'mainBkg': '#fff',
      'nodeTextColor': '#000',
      'fontSize': '14px',
      'primaryBorderColor': '#0000FF',
      'edgeLabelBackground': '#fff',
      'lineHeight': '1.3',
      'lineColor': '#00AA00',
      'edgeColor': '#00AA00'
    },
    'flowchart': {
      'nodeSpacing': 25,
      'rankSpacing': 70,
      'curve': 'basis',
      'useMaxWidth': false,
      'htmlLabels': true
    }
  }
}%%

flowchart TD
    %% 使用子图按维度分组节点
'''
    
    # 获取所有维度并排序
    dimensions = sorted(dimension_groups.keys(), 
                       key=lambda dim: extract_dimension_number(dim), 
                       reverse=True)
    
    # 创建节点ID映射
    node_ids = {}
    
    # 为每个维度创建子图并添加节点
    for dim in dimensions:
        if dim == "无维度":
            mermaid_code += f'''    
    subgraph D0["无维度文档"]
'''
        else:
            dim_number = extract_dimension_number(dim)
            mermaid_code += f'''    
    subgraph D{dim_number}["维度 {dim}"]
'''
        
        # 添加该维度下的所有节点
        for file_info in dimension_groups[dim]:
            # 从文件名创建节点ID
            filename = file_info["文件名"]
            node_id = filename.replace("formal_theory_", "").replace(".md", "")
            node_ids[filename] = node_id
            
            # 添加节点定义
            title = file_info["标题"]
            dim_display = f"(D{extract_dimension_number(dim)})" if dim != "无维度" else "(无维度)"
            mermaid_code += f'        {node_id}["{title}<br>{dim_display}"]\n'
        
        mermaid_code += "    end\n"
    
    # 添加维度层次排序
    mermaid_code += "\n    %% 设置子图方向和排序\n    "
    dim_links = []
    for dim in dimensions:
        if dim == "无维度":
            dim_links.append("D0")
        else:
            dim_number = extract_dimension_number(dim)
            dim_links.append(f"D{dim_number}")
    
    mermaid_code += " --- ".join(dim_links) + "\n"
    
    # 添加极高维理论依赖
    mermaid_code += '''    
    %% 极高维理论依赖
'''
    
    # 添加超高维理论依赖
    mermaid_code += '''    
    %% 超高维理论依赖
'''
    
    # 添加高维理论依赖
    mermaid_code += '''    
    %% 高维理论依赖
'''
    
    # 添加中维理论依赖
    mermaid_code += '''    
    %% 中维理论依赖
'''
    
    # 添加基础维度理论依赖
    mermaid_code += '''    
    %% 基础维度理论依赖
'''
    
    # 为所有依赖关系添加连接线
    dependencies = theory_data["dependencies"]
    added_deps = set()  # 已添加的依赖关系
    
    for source_file, target_files in dependencies.items():
        if source_file in node_ids:
            source_id = node_ids[source_file]
            for target_file in target_files:
                if target_file in node_ids:
                    target_id = node_ids[target_file]
                    dep_key = f"{source_id}->{target_id}"
                    if dep_key not in added_deps:
                        mermaid_code += f"    {source_id} --> {target_id}\n"
                        added_deps.add(dep_key)
    
    # 添加样式设置
    mermaid_code += '''    
    %% 子图样式设置
    style D0 fill:#fbf,stroke:#333,stroke-width:2px
'''
    
    # 为每个维度添加样式
    for dim in dimensions:
        if dim != "无维度":
            dim_number = extract_dimension_number(dim)
            color = f"#{max(3, 10-dim_number//5)}{max(3, 10-dim_number//4)}f" if dim_number > 0 else "#fbf"
            mermaid_code += f"    style D{dim_number} fill:{color},stroke:#333,stroke-width:2px\n"
    
    # 添加结束标记
    mermaid_code += '''    
    %% 样式设置
    style core fill:#f9f,stroke:#333,stroke-width:2px
    
    %% 无维度文档样式
    style terminology fill:#fbf,stroke:#333,stroke-width:2px
    style theory_structure fill:#fbf,stroke:#333,stroke-width:2px
```'''

    return mermaid_code

def update_graph_file(mermaid_code, file_path, file_path_en=None):
    """更新图表文件中的Mermaid代码部分"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找现有的Mermaid代码块并替换
        pattern = r'```mermaid.*?```'
        updated_content = re.sub(pattern, mermaid_code, content, flags=re.DOTALL)
        
        # 找到图表说明部分
        explanation_match = re.search(r'##\s+图表说明', updated_content)
        if explanation_match:
            # 截取代码块结束和图表说明之间的内容，确保它们之间只有一个换行符
            mermaid_end = updated_content.find("```\n\n", 0, explanation_match.start())
            if mermaid_end != -1:
                updated_content = updated_content[:mermaid_end+4] + "\n\n" + updated_content[explanation_match.start():]
        
        # 清理文件末尾可能存在的百分号
        updated_content = updated_content.rstrip()
        if updated_content.endswith('%'):
            updated_content = updated_content[:-1].rstrip()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"成功更新图表文件: {file_path}")
        
        # 如果提供了英文版文件路径，也更新英文版
        if file_path_en:
            # 读取英文版文件
            with open(file_path_en, 'r', encoding='utf-8') as f:
                en_content = f.read()
            
            # 将中文版的Mermaid代码转换为英文版
            en_mermaid_code = convert_to_english(mermaid_code)
            
            # 替换英文版的Mermaid代码
            updated_en_content = re.sub(pattern, en_mermaid_code, en_content, flags=re.DOTALL)
            
            # 找到图表说明部分(英文版)
            explanation_match_en = re.search(r'##\s+Diagram\s+Explanation', updated_en_content)
            if explanation_match_en:
                # 截取代码块结束和图表说明之间的内容，确保它们之间只有一个换行符
                mermaid_end_en = updated_en_content.find("```\n\n", 0, explanation_match_en.start())
                if mermaid_end_en != -1:
                    updated_en_content = updated_en_content[:mermaid_end_en+4] + "\n\n" + updated_en_content[explanation_match_en.start():]
            
            # 清理文件末尾可能存在的百分号
            updated_en_content = updated_en_content.rstrip()
            if updated_en_content.endswith('%'):
                updated_en_content = updated_en_content[:-1].rstrip()
            
            with open(file_path_en, 'w', encoding='utf-8') as f:
                f.write(updated_en_content)
            
            print(f"成功更新英文图表文件: {file_path_en}")
        
    except Exception as e:
        print(f"更新图表文件时出错: {e}", file=sys.stderr)

def convert_to_english(mermaid_code):
    """将中文Mermaid代码转换为英文版"""
    # 将中文标题换成英文
    en_mermaid_code = mermaid_code.replace("维度", "Dimension")
    en_mermaid_code = en_mermaid_code.replace("无维度文档", "No Dimension Documents")
    en_mermaid_code = en_mermaid_code.replace("极高维理论依赖", "Ultra-High Dimensional Theory Dependencies")
    en_mermaid_code = en_mermaid_code.replace("超高维理论依赖", "Ultra-High Dimensional Theory Dependencies")
    en_mermaid_code = en_mermaid_code.replace("高维理论依赖", "High Dimensional Theory Dependencies")
    en_mermaid_code = en_mermaid_code.replace("中维理论依赖", "Middle Dimensional Theory Dependencies")
    en_mermaid_code = en_mermaid_code.replace("基础维度理论依赖", "Foundational Dimensional Theory Dependencies")
    en_mermaid_code = en_mermaid_code.replace("子图样式设置", "Subgraph style settings")
    en_mermaid_code = en_mermaid_code.replace("样式设置", "Style settings")
    en_mermaid_code = en_mermaid_code.replace("无维度文档样式", "Non-Dimensional Document Styles")
    en_mermaid_code = en_mermaid_code.replace("设置子图方向和排序", "Setting subgraph direction and ordering")
    en_mermaid_code = en_mermaid_code.replace("使用子图按维度分组节点", "Using subgraphs to group nodes by dimension")
    
    return en_mermaid_code

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='分析理论文件并生成JSON数据或更新图表')
    parser.add_argument('--update-graph', action='store_true', help='更新理论关系图文件')
    parser.add_argument('--graph-file', default='formal_theory_graph.md', help='要更新的图表文件路径')
    parser.add_argument('--graph-file-en', default='formal_theory_graph_en.md', help='要更新的英文图表文件路径')
    parser.add_argument('--directory', default='formal_theory', help='形式化理论目录')
    args = parser.parse_args()
    
    # 分析形式化理论目录
    directory = args.directory
    print(f"分析目录: {os.path.abspath(directory)}", file=sys.stderr)
    result = analyze_theory_files(directory)
    
    if args.update_graph:
        # 生成并更新Mermaid图表
        mermaid_code = generate_mermaid_graph(result)
        update_graph_file(mermaid_code, args.graph_file, args.graph_file_en)
    else:
        # 输出JSON到控制台
        print(json.dumps(result, ensure_ascii=False, indent=2)) 