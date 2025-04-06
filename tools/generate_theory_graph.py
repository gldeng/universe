#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
宇宙本论理论依赖关系图生成工具

此工具用于分析理论之间的依赖关系，并生成可视化的依赖关系图。
支持不同的输出格式，包括DOT文件、PNG图像和HTML交互式图表。

使用方法：
python generate_theory_graph.py --output theory_graph.html --format html
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False
    print("警告：未安装networkx库，部分功能将不可用。可通过运行 pip install networkx 安装。")

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("警告：未安装matplotlib库，部分功能将不可用。可通过运行 pip install matplotlib 安装。")

def parse_args():
    parser = argparse.ArgumentParser(description="生成理论依赖关系图")
    parser.add_argument("--theory_dir", default="../formal_theory", help="理论文件目录")
    parser.add_argument("--output", default="theory_graph", help="输出文件名（不含扩展名）")
    parser.add_argument("--format", default="dot", choices=["dot", "png", "html", "all"], help="输出格式")
    parser.add_argument("--filter_dimension", type=int, help="按维度过滤理论（仅包含大于等于指定维度的理论）")
    parser.add_argument("--filter_theory", help="按理论名过滤（只显示与指定理论相关的理论）")
    parser.add_argument("--json_input", help="使用JSON文件作为输入，而不是直接分析理论文件")
    parser.add_argument("--layout", default="dot", choices=["dot", "neato", "fdp", "sfdp", "twopi", "circo"], 
                       help="图布局算法（需要安装Graphviz）")
    return parser.parse_args()

def find_md_files(directory):
    """递归查找所有.md文件"""
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and not file.endswith('_en.md'):  # 排除英文版本
                md_files.append(os.path.join(root, file))
    return md_files

def extract_theory_info(file_path):
    """从理论文件提取标题、维度和引用关系"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 提取标题
            title_pattern = r'^# (.*?)(?:\[维度[:：]\s*(\d+|∞)\])?'
            title_match = re.search(title_pattern, content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                dimension = title_match.group(2) if title_match.group(2) else "未知"
            else:
                title = os.path.basename(file_path).replace('.md', '')
                dimension = "未知"
            
            # 提取引用关系
            references = []
            reference_section = re.search(r'## 理论依赖(?:.|\n)*?(?=##|$)', content)
            if reference_section:
                ref_section_content = reference_section.group(0)
                # 查找所有Markdown链接
                link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
                links = re.findall(link_pattern, ref_section_content)
                references = [link[1] for link in links if link[1].endswith('.md')]
            
            return {
                'file_path': file_path,
                'title': title,
                'dimension': dimension,
                'references': references
            }
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return None

def process_theories(theory_files):
    """处理所有理论文件，提取信息和依赖关系"""
    theories = {}
    dependencies = defaultdict(list)
    
    for file_path in theory_files:
        info = extract_theory_info(file_path)
        if info:
            file_name = os.path.basename(file_path)
            theories[file_name] = info
            
            # 处理依赖
            for ref in info['references']:
                ref_name = os.path.basename(ref)
                if ref_name != file_name:  # 避免自引用
                    dependencies[file_name].append(ref_name)
    
    return theories, dependencies

def create_networkx_graph(theories, dependencies):
    """使用NetworkX创建图对象"""
    if not HAS_NETWORKX:
        print("错误：需要安装NetworkX库才能创建图")
        return None
    
    G = nx.DiGraph()
    
    # 添加节点
    for name, info in theories.items():
        G.add_node(name, title=info['title'], dimension=info['dimension'])
    
    # 添加边
    for source, targets in dependencies.items():
        for target in targets:
            if target in theories:  # 确保目标理论存在
                G.add_edge(source, target)
    
    return G

def filter_graph(G, filter_dimension=None, filter_theory=None):
    """根据条件过滤图"""
    if not G:
        return None
    
    if filter_dimension is not None:
        # 按维度过滤
        nodes_to_keep = [n for n, attr in G.nodes(data=True) 
                        if attr['dimension'] != "未知" and 
                        (attr['dimension'] == "∞" or int(attr['dimension']) >= filter_dimension)]
        
        # 创建子图
        G = G.subgraph(nodes_to_keep)
    
    if filter_theory is not None:
        # 只保留与指定理论相关的节点
        if filter_theory in G:
            # 找出与指定理论相关的所有节点
            related_nodes = set()
            related_nodes.add(filter_theory)
            
            # 添加依赖节点
            for path in nx.all_simple_paths(G, filter_theory, filter_theory):
                related_nodes.update(path)
            
            # 添加被依赖节点
            for node in G.nodes():
                if nx.has_path(G, node, filter_theory):
                    related_nodes.add(node)
                    for path in nx.all_simple_paths(G, node, filter_theory):
                        related_nodes.update(path)
            
            # 创建子图
            G = G.subgraph(related_nodes)
    
    return G

def generate_dot_file(G, output_file):
    """生成DOT文件"""
    if not G:
        return False
    
    try:
        # 创建DOT文件头
        dot_content = "digraph theories {\n"
        dot_content += "  graph [rankdir=TB, splines=true, overlap=false];\n"
        dot_content += "  node [shape=box, style=filled, fontname=\"Arial\"];\n"
        
        # 添加节点
        for node, attr in G.nodes(data=True):
            dimension = attr['dimension']
            title = attr['title']
            
            # 根据维度设置节点颜色
            if dimension == "∞":
                color = "gold1"
            elif dimension == "未知":
                color = "lightgray"
            else:
                dim = int(dimension)
                if dim >= 50:
                    color = "red"
                elif dim >= 40:
                    color = "orange"
                elif dim >= 30:
                    color = "yellow"
                elif dim >= 20:
                    color = "lightgreen"
                elif dim >= 10:
                    color = "skyblue"
                else:
                    color = "lightblue"
            
            # 添加节点定义
            dot_content += f'  "{node}" [label="{title}\\n[维度: {dimension}]", fillcolor="{color}"];\n'
        
        # 添加边
        for source, target in G.edges():
            dot_content += f'  "{source}" -> "{target}";\n'
        
        # 关闭DOT文件
        dot_content += "}\n"
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(dot_content)
        
        return True
    except Exception as e:
        print(f"生成DOT文件时出错: {e}")
        return False

def generate_png_file(dot_file, output_file, layout="dot"):
    """使用Graphviz生成PNG文件"""
    try:
        import subprocess
        cmd = [layout, "-Tpng", dot_file, "-o", output_file]
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"生成PNG文件时出错: {e}")
        return False

def generate_html_file(G, output_file):
    """生成交互式HTML文件"""
    if not G:
        return False
    
    try:
        html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>宇宙本论理论依赖关系图</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        #graph-container {
            width: 100%;
            height: 100vh;
            background-color: white;
        }
        .node {
            cursor: pointer;
        }
        .node text {
            font-size: 12px;
            fill: #333;
        }
        .link {
            stroke: #999;
            stroke-opacity: 0.6;
            stroke-width: 1.5px;
        }
        .tooltip {
            position: absolute;
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            pointer-events: none;
            font-size: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .controls {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(255, 255, 255, 0.9);
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        select, button {
            margin: 5px;
            padding: 5px;
        }
    </style>
</head>
<body>
    <div class="controls">
        <div>
            <label for="dimension-filter">维度过滤:</label>
            <select id="dimension-filter">
                <option value="0">全部显示</option>
                <option value="10">≥10</option>
                <option value="20">≥20</option>
                <option value="30">≥30</option>
                <option value="40">≥40</option>
                <option value="50">≥50</option>
            </select>
        </div>
        <div>
            <label for="layout">布局:</label>
            <select id="layout">
                <option value="force">力导向</option>
                <option value="radial">放射状</option>
                <option value="hierarchical">层次结构</option>
            </select>
        </div>
        <div>
            <button id="reset-zoom">重置视图</button>
            <button id="toggle-labels">显示/隐藏标签</button>
        </div>
    </div>
    <div id="graph-container"></div>
    <script>
        // 图数据
        const graphData = {
            nodes: [
"""
        
        # 添加节点数据
        for i, (node, attr) in enumerate(G.nodes(data=True)):
            dimension = attr['dimension']
            title = attr['title']
            
            # 确定节点颜色
            if dimension == "∞":
                color = "#FFD700"  # gold1
            elif dimension == "未知":
                color = "#D3D3D3"  # lightgray
            else:
                dim = int(dimension)
                if dim >= 50:
                    color = "#FF4500"  # red
                elif dim >= 40:
                    color = "#FFA500"  # orange
                elif dim >= 30:
                    color = "#FFFF00"  # yellow
                elif dim >= 20:
                    color = "#90EE90"  # lightgreen
                elif dim >= 10:
                    color = "#87CEEB"  # skyblue
                else:
                    color = "#ADD8E6"  # lightblue
            
            # 添加节点数据
            html_content += f'                {{id: "{node}", title: "{title}", dimension: "{dimension}", color: "{color}"}}'
            if i < len(G.nodes()) - 1:
                html_content += ","
            html_content += "\n"
        
        html_content += """            ],
            links: [
"""
        
        # 添加边数据
        for i, (source, target) in enumerate(G.edges()):
            html_content += f'                {{source: "{source}", target: "{target}"}}'
            if i < len(G.edges()) - 1:
                html_content += ","
            html_content += "\n"
        
        html_content += """            ]
        };

        // D3.js 图表绘制
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        const svg = d3.select('#graph-container')
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        // 添加缩放功能
        const g = svg.append('g');
        svg.call(d3.zoom()
            .scaleExtent([0.1, 4])
            .on('zoom', (event) => {
                g.attr('transform', event.transform);
            }));
        
        // 添加箭头标记
        svg.append('defs').append('marker')
            .attr('id', 'arrowhead')
            .attr('viewBox', '-0 -5 10 10')
            .attr('refX', 20)
            .attr('refY', 0)
            .attr('orient', 'auto')
            .attr('markerWidth', 10)
            .attr('markerHeight', 10)
            .attr('xoverflow', 'visible')
            .append('svg:path')
            .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
            .attr('fill', '#999')
            .style('stroke', 'none');
        
        let simulation = d3.forceSimulation()
            .force('link', d3.forceLink().id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2));
        
        // 创建连线
        const link = g.append('g')
            .selectAll('line')
            .data(graphData.links)
            .enter().append('line')
            .attr('class', 'link')
            .attr('marker-end', 'url(#arrowhead)');
        
        // 创建节点
        const node = g.append('g')
            .selectAll('.node')
            .data(graphData.nodes)
            .enter().append('g')
            .attr('class', 'node')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));
        
        // 添加节点圆形
        node.append('circle')
            .attr('r', 8)
            .style('fill', d => d.color);
        
        // 添加节点文本
        const labels = node.append('text')
            .attr('dy', -15)
            .attr('text-anchor', 'middle')
            .text(d => d.title);
        
        // 添加工具提示
        const tooltip = d3.select('body').append('div')
            .attr('class', 'tooltip')
            .style('opacity', 0);
        
        node.on('mouseover', function(event, d) {
            tooltip.transition()
                .duration(200)
                .style('opacity', .9);
            tooltip.html(`<strong>${d.title}</strong><br/>维度: ${d.dimension}<br/>文件: ${d.id}`)
                .style('left', (event.pageX + 10) + 'px')
                .style('top', (event.pageY - 28) + 'px');
        })
        .on('mouseout', function() {
            tooltip.transition()
                .duration(500)
                .style('opacity', 0);
        });
        
        // 更新图布局
        simulation
            .nodes(graphData.nodes)
            .on('tick', ticked);
        
        simulation.force('link')
            .links(graphData.links);
        
        function ticked() {
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            node
                .attr('transform', d => `translate(${d.x},${d.y})`);
        }
        
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
        
        // 维度过滤功能
        document.getElementById('dimension-filter').addEventListener('change', function() {
            const minDimension = parseInt(this.value);
            const filteredNodes = graphData.nodes.filter(node => {
                if (node.dimension === "∞") return true;
                if (node.dimension === "未知") return minDimension === 0;
                return parseInt(node.dimension) >= minDimension;
            });
            
            const filteredNodeIds = new Set(filteredNodes.map(node => node.id));
            
            const filteredLinks = graphData.links.filter(link => 
                filteredNodeIds.has(link.source.id || link.source) && 
                filteredNodeIds.has(link.target.id || link.target)
            );
            
            updateGraph(filteredNodes, filteredLinks);
        });
        
        // 布局切换功能
        document.getElementById('layout').addEventListener('change', function() {
            const layout = this.value;
            
            if (layout === 'force') {
                simulation
                    .force('link', d3.forceLink().id(d => d.id).distance(100))
                    .force('charge', d3.forceManyBody().strength(-300))
                    .force('center', d3.forceCenter(width / 2, height / 2))
                    .alpha(1).restart();
            } else if (layout === 'radial') {
                simulation
                    .force('link', d3.forceLink().id(d => d.id).distance(100))
                    .force('charge', d3.forceManyBody().strength(-100))
                    .force('r', d3.forceRadial(width / 3, width / 2, height / 2))
                    .force('center', d3.forceCenter(width / 2, height / 2))
                    .alpha(1).restart();
            } else if (layout === 'hierarchical') {
                simulation
                    .force('link', d3.forceLink().id(d => d.id).distance(60).strength(1))
                    .force('charge', d3.forceManyBody().strength(-300))
                    .force('x', d3.forceX(width / 2).strength(0.1))
                    .force('y', d3.forceY().strength(0.1).y(d => {
                        if (d.dimension === "∞") return height * 0.1;
                        if (d.dimension === "未知") return height * 0.9;
                        return height * (0.2 + (60 - parseInt(d.dimension)) / 60 * 0.7);
                    }))
                    .alpha(1).restart();
            }
        });
        
        // 重置视图按钮
        document.getElementById('reset-zoom').addEventListener('click', function() {
            svg.transition().duration(750).call(
                d3.zoom().transform,
                d3.zoomIdentity
            );
        });
        
        // 显示/隐藏标签按钮
        document.getElementById('toggle-labels').addEventListener('click', function() {
            const currentOpacity = labels.style('opacity');
            labels.style('opacity', currentOpacity == 1 ? 0 : 1);
        });
        
        function updateGraph(nodes, links) {
            // 移除旧的元素
            g.selectAll('.node').remove();
            g.selectAll('.link').remove();
            
            // 重新创建连线
            const link = g.append('g')
                .selectAll('line')
                .data(links)
                .enter().append('line')
                .attr('class', 'link')
                .attr('marker-end', 'url(#arrowhead)');
            
            // 重新创建节点
            const node = g.append('g')
                .selectAll('.node')
                .data(nodes)
                .enter().append('g')
                .attr('class', 'node')
                .call(d3.drag()
                    .on('start', dragstarted)
                    .on('drag', dragged)
                    .on('end', dragended));
            
            // 添加节点圆形
            node.append('circle')
                .attr('r', 8)
                .style('fill', d => d.color);
            
            // 添加节点文本
            const labels = node.append('text')
                .attr('dy', -15)
                .attr('text-anchor', 'middle')
                .text(d => d.title);
            
            // 添加工具提示事件
            node.on('mouseover', function(event, d) {
                tooltip.transition()
                    .duration(200)
                    .style('opacity', .9);
                tooltip.html(`<strong>${d.title}</strong><br/>维度: ${d.dimension}<br/>文件: ${d.id}`)
                    .style('left', (event.pageX + 10) + 'px')
                    .style('top', (event.pageY - 28) + 'px');
            })
            .on('mouseout', function() {
                tooltip.transition()
                    .duration(500)
                    .style('opacity', 0);
            });
            
            // 重启模拟
            simulation.nodes(nodes);
            simulation.force('link').links(links);
            simulation.alpha(1).restart();
        }
    </script>
</body>
</html>
"""
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True
    except Exception as e:
        print(f"生成HTML文件时出错: {e}")
        return False

def load_from_json(json_file):
    """从JSON文件加载理论数据"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        theories = {}
        dependencies = defaultdict(list)
        
        # 处理理论数据
        for name, info in data.items():
            if name.startswith('_'):  # 跳过元数据
                continue
            
            theories[name + '.md'] = {
                'file_path': name + '.md',
                'title': info.get('metadata', {}).get('title', name),
                'dimension': info.get('metadata', {}).get('dimension', '未知')
            }
            
            # 处理依赖关系
            references = []
            for ref in info.get('references', {}).values():
                if ref.endswith('.md'):
                    references.append(ref)
            
            dependencies[name + '.md'] = references
        
        return theories, dependencies
    except Exception as e:
        print(f"从JSON文件加载数据时出错: {e}")
        return {}, defaultdict(list)

def main():
    args = parse_args()
    
    theories = {}
    dependencies = defaultdict(list)
    
    if args.json_input:
        # 从JSON文件加载
        theories, dependencies = load_from_json(args.json_input)
    else:
        # 从理论文件分析
        theory_files = find_md_files(args.theory_dir)
        theories, dependencies = process_theories(theory_files)
    
    # 创建图
    G = create_networkx_graph(theories, dependencies)
    
    if G:
        # 应用过滤
        G = filter_graph(G, args.filter_dimension, args.filter_theory)
        
        if args.format == 'dot' or args.format == 'all':
            dot_file = f"{args.output}.dot"
            if generate_dot_file(G, dot_file):
                print(f"DOT文件已生成: {dot_file}")
        
        if (args.format == 'png' or args.format == 'all') and HAS_MATPLOTLIB:
            png_file = f"{args.output}.png"
            if args.layout:
                if generate_png_file(f"{args.output}.dot", png_file, args.layout):
                    print(f"PNG文件已生成: {png_file}")
            else:
                # 使用matplotlib
                plt.figure(figsize=(12, 10))
                pos = nx.nx_agraph.graphviz_layout(G, prog='dot') if nx.nx_agraph.graphviz_layout else nx.spring_layout(G)
                
                # 设置节点颜色
                node_colors = []
                for _, attr in G.nodes(data=True):
                    dimension = attr['dimension']
                    if dimension == "∞":
                        node_colors.append('gold')
                    elif dimension == "未知":
                        node_colors.append('lightgray')
                    else:
                        dim = int(dimension)
                        if dim >= 50:
                            node_colors.append('red')
                        elif dim >= 40:
                            node_colors.append('orange')
                        elif dim >= 30:
                            node_colors.append('yellow')
                        elif dim >= 20:
                            node_colors.append('lightgreen')
                        elif dim >= 10:
                            node_colors.append('skyblue')
                        else:
                            node_colors.append('lightblue')
                
                # 绘制图
                nx.draw(G, pos, with_labels=True, node_color=node_colors, 
                       node_size=500, font_size=8, font_weight='bold', 
                       edge_color='gray', width=1.0, arrows=True)
                
                plt.savefig(png_file, dpi=300, bbox_inches='tight')
                plt.close()
                print(f"PNG文件已生成: {png_file}")
        
        if args.format == 'html' or args.format == 'all':
            html_file = f"{args.output}.html"
            if generate_html_file(G, html_file):
                print(f"HTML文件已生成: {html_file}")
    else:
        print("无法创建依赖关系图")

if __name__ == "__main__":
    main() 