#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import sys
from graphviz import Digraph

def get_dimension_number(dimension):
    """从维度字符串中提取数字，用于排序"""
    if not dimension or dimension == "无维度":
        return -999
    
    # 移除所有空格
    dimension = dimension.replace(" ", "")
    
    # 处理D∞或者D+∞的情况
    if "∞" in dimension:
        return float('inf')
    
    # 提取数字部分，支持负数
    match = re.search(r'D([+-]?\d+)', dimension)
    if match:
        return int(match.group(1))
    
    return -999

def get_color_by_dimension(dimension_number):
    """根据维度返回颜色"""
    if dimension_number == float('inf'):
        return "#FF00FF"  # 紫色用于无穷维度
    elif dimension_number >= 50:
        return "#FF0000"  # 红色用于超高维度 (≥50)
    elif dimension_number >= 30:
        return "#FF4500"  # 橙红色用于高维度 (30-49)
    elif dimension_number >= 20:
        return "#FFA500"  # 橙色用于中高维度 (20-29)
    elif dimension_number >= 10:
        return "#008000"  # 绿色用于中维度 (10-19)
    elif dimension_number >= 0:
        return "#0000FF"  # 蓝色用于低维度 (0-9)
    else:
        return "#808080"  # 灰色用于负维度或未知维度

def get_node_style(file_info):
    """根据文件信息返回节点样式"""
    dimension = file_info.get("维度", "无维度")
    dimension_number = get_dimension_number(dimension)
    color = get_color_by_dimension(dimension_number)
    
    # 根据是否需要重新生成设置节点形状
    shape = "ellipse" if not file_info.get("需要重新生成", True) else "box"
    
    # 根据维度设置样式
    style = "filled"
    
    # 根据维度范围设置填充颜色
    fillcolor = color
    fontcolor = "white" if dimension_number >= 10 else "black"
    
    return {
        "shape": shape,
        "style": style,
        "color": color,
        "fillcolor": fillcolor,
        "fontcolor": fontcolor
    }

def create_legend(dot):
    """创建图例"""
    with dot.subgraph(name="cluster_legend") as legend:
        legend.attr(label="图例", style="filled", fillcolor="white")
        
        # 维度范围图例
        legend.node("legend_inf", "无穷维度", style="filled", fillcolor="#FF00FF", fontcolor="white")
        legend.node("legend_50plus", "超高维度 (≥50)", style="filled", fillcolor="#FF0000", fontcolor="white")
        legend.node("legend_30to49", "高维度 (30-49)", style="filled", fillcolor="#FF4500", fontcolor="white")
        legend.node("legend_20to29", "中高维度 (20-29)", style="filled", fillcolor="#FFA500", fontcolor="white")
        legend.node("legend_10to19", "中维度 (10-19)", style="filled", fillcolor="#008000", fontcolor="white")
        legend.node("legend_0to9", "低维度 (0-9)", style="filled", fillcolor="#0000FF", fontcolor="white")
        legend.node("legend_neg", "负维度", style="filled", fillcolor="#808080", fontcolor="white")
        
        # 节点和边的类型图例
        legend.node("legend_complete", "完整理论", shape="ellipse", style="filled", fillcolor="#CCCCCC")
        legend.node("legend_incomplete", "需要重新生成的理论", shape="box", style="filled", fillcolor="#CCCCCC")
        
        # 创建虚拟节点来显示边的类型
        legend.node("legend_edge1", "", style="invis")
        legend.node("legend_edge2", "", style="invis")
        legend.node("legend_resolved", "已解析依赖", shape="plaintext")
        legend.node("legend_unresolved", "未解析依赖", shape="plaintext")
        
        legend.edge("legend_edge1", "legend_resolved", style="solid")
        legend.edge("legend_edge2", "legend_unresolved", style="dashed")
        
        # 排列图例项
        legend.attr(rank="same")
        for i in range(6):
            legend.edge(f"legend_{50-i*10}plus" if i == 0 else 
                       f"legend_{30-i*10}to{49-i*10}" if i < 3 else
                       f"legend_{10-(i-3)*10}to{19-(i-3)*10}" if i == 3 else
                       f"legend_0to9" if i == 4 else
                       f"legend_neg",
                       f"legend_{30-i*10}to{49-i*10}" if i < 3 else
                       f"legend_{10-(i-3)*10}to{19-(i-3)*10}" if i == 3 else
                       f"legend_0to9" if i == 4 else
                       f"legend_neg" if i == 5 else "",
                       style="invis")

def generate_theory_graph(json_file, output_file, max_nodes=None, filter_dimension=None, highlight_file=None):
    """生成理论依赖关系图
    
    Args:
        json_file: JSON分析结果文件路径
        output_file: 输出图文件路径（不含扩展名）
        max_nodes: 最大节点数量限制
        filter_dimension: 按维度范围过滤(例如: "D10-D20")
        highlight_file: 要高亮显示的文件名
    """
    # 加载JSON数据
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 创建有向图
    dot = Digraph(comment='理论依赖关系图', format='pdf')
    dot.attr(rankdir='BT')  # 从下到上的布局
    dot.attr(size='100,100')  # 图大小
    dot.attr(ratio='compress')  # 自动调整比例
    dot.attr(margin='0.5')  # 边距
    dot.attr(fontname='SimSun')  # 字体
    dot.attr('node', fontname='SimSun')
    dot.attr('edge', fontname='SimSun')
    
    # 创建图例
    create_legend(dot)
    
    # 处理维度过滤
    min_dim = -999
    max_dim = float('inf')
    if filter_dimension:
        match = re.match(r'D([+-]?\d+)-D([+-]?\d+|\+?∞)', filter_dimension)
        if match:
            min_dim = int(match.group(1))
            if match.group(2) == '∞' or match.group(2) == '+∞':
                max_dim = float('inf')
            else:
                max_dim = int(match.group(2))
    
    # 获取文件信息字典，用于快速查找
    files_dict = {file_info["文件名"]: file_info for file_info in data["files"]}
    
    # 确定要包含的节点和边
    deps_map = data["dependencies"]
    included_nodes = set()
    edges = []
    
    # 如果指定了要高亮的文件，一定包含它
    if highlight_file and highlight_file in files_dict:
        included_nodes.add(highlight_file)
        
        # 添加其依赖和被依赖的文件
        if highlight_file in deps_map:
            for dep in deps_map[highlight_file]["resolved_deps"]:
                included_nodes.add(dep)
        
        # 找出所有依赖该文件的文件
        for src, deps in deps_map.items():
            if highlight_file in deps["resolved_deps"]:
                included_nodes.add(src)
    
    # 如果没有指定高亮文件，则根据过滤条件选择节点
    else:
        # 按维度过滤文件
        filtered_files = []
        for file_info in data["files"]:
            dim_num = get_dimension_number(file_info["维度"])
            if min_dim <= dim_num <= max_dim:
                filtered_files.append(file_info)
        
        # 如果有最大节点数限制，按维度从高到低排序并截取
        if max_nodes and len(filtered_files) > max_nodes:
            filtered_files.sort(key=lambda x: get_dimension_number(x["维度"]), reverse=True)
            filtered_files = filtered_files[:max_nodes]
        
        # 添加所选文件及其依赖
        for file_info in filtered_files:
            filename = file_info["文件名"]
            included_nodes.add(filename)
            
            # 添加直接依赖
            if filename in deps_map:
                for dep in deps_map[filename]["resolved_deps"]:
                    included_nodes.add(dep)
    
    # 创建节点
    for node in included_nodes:
        if node in files_dict:
            file_info = files_dict[node]
            title = file_info.get("标题", node)
            dimension = file_info.get("维度", "无维度")
            
            # 显示简化的标题
            short_title = re.sub(r'的严格形式化描述.*$', '', title).strip()
            # 如果标题太长，进一步简化
            if len(short_title) > 20:
                short_title = short_title[:18] + "..."
            
            label = f"{short_title}\n[{dimension}]"
            
            # 为高亮节点添加特殊样式
            if highlight_file and node == highlight_file:
                dot.node(node, label, **get_node_style(file_info), penwidth='3')
            else:
                dot.node(node, label, **get_node_style(file_info))
    
    # 添加边（依赖关系）
    for src in included_nodes:
        if src in deps_map:
            # 添加已解析的依赖边
            for target in deps_map[src]["resolved_deps"]:
                if target in included_nodes:
                    edges.append((src, target, "resolved"))
            
            # 添加未解析依赖作为说明注释
            if deps_map[src]["unresolved_deps"]:
                unresolved_str = ", ".join(deps_map[src]["unresolved_deps"])
                if len(unresolved_str) > 30:
                    unresolved_str = unresolved_str[:27] + "..."
                
                # 创建一个代表未解析依赖的虚拟节点
                unresolved_node = f"{src}_unresolved"
                dot.node(unresolved_node, f"未解析:\n{unresolved_str}", shape="note", style="filled", fillcolor="#FFFF99")
                edges.append((src, unresolved_node, "unresolved"))
    
    # 添加所有边
    for src, target, edge_type in edges:
        if edge_type == "resolved":
            dot.edge(src, target, style="solid")
        else:
            dot.edge(src, target, style="dashed", color="red")
    
    # 生成图
    dot.render(output_file, view=False, cleanup=True)
    print(f"理论依赖关系图已生成：{output_file}.pdf")
    
    # 生成简化版
    if not highlight_file:
        simple_dot = Digraph(comment='理论依赖关系图（简化版）', format='pdf')
        simple_dot.attr(rankdir='BT')
        simple_dot.attr(size='50,50')
        simple_dot.attr(ratio='compress')
        simple_dot.attr(margin='0.5')
        simple_dot.attr(fontname='SimSun')
        simple_dot.attr('node', fontname='SimSun')
        simple_dot.attr('edge', fontname='SimSun')
        
        # 只保留文件名和关系，不显示其他信息
        for node in included_nodes:
            if node in files_dict:
                simple_dot.node(node, node, shape="box")
        
        # 只添加已解析的依赖边
        for src, target, edge_type in edges:
            if edge_type == "resolved":
                simple_dot.edge(src, target)
        
        # 生成简化图
        simple_output = f"{output_file}_simple"
        simple_dot.render(simple_output, view=False, cleanup=True)
        print(f"简化版理论依赖关系图已生成：{simple_output}.pdf")

def main():
    if len(sys.argv) < 3:
        print("用法: python generate_theory_graph.py <json文件> <输出文件> [最大节点数] [维度过滤] [高亮文件]")
        print("示例: python generate_theory_graph.py theory_analysis.json theory_graph 50 D10-D20 formal_theory_cosmic_ontology.md")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_file = sys.argv[2]
    
    max_nodes = int(sys.argv[3]) if len(sys.argv) > 3 else None
    filter_dimension = sys.argv[4] if len(sys.argv) > 4 else None
    highlight_file = sys.argv[5] if len(sys.argv) > 5 else None
    
    generate_theory_graph(json_file, output_file, max_nodes, filter_dimension, highlight_file)

if __name__ == "__main__":
    main() 