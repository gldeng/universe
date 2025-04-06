#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
宇宙本论形式化理论体系维护报告生成工具

此工具用于生成理论体系维护报告，包括以下内容：
1. 理论文件统计信息
2. 维度分布情况
3. 未索引文件检查
4. 链接完整性检查
5. 中英文文件同步情况
6. 版本一致性检查

使用方法：
python generate_maintenance_report.py --output maintenance_report.md
"""

import os
import re
import sys
import json
import argparse
import datetime
from pathlib import Path
from collections import defaultdict, Counter

def parse_args():
    parser = argparse.ArgumentParser(description="生成理论体系维护报告")
    parser.add_argument("--dir", default="../", help="项目根目录，默认为上级目录")
    parser.add_argument("--theory_dir", default="../formal_theory", help="理论文件目录")
    parser.add_argument("--output", default="maintenance_report.md", help="输出报告文件名")
    parser.add_argument("--index", default="../formal_theory.md", help="中文索引文件")
    parser.add_argument("--index_en", default="../formal_theory_en.md", help="英文索引文件")
    return parser.parse_args()

def find_md_files(directory):
    """递归查找所有.md文件"""
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_dimension(content):
    """从文件内容中提取维度信息"""
    dimension_pattern = r'\[维度[:：]\s*(\d+|∞)\]'
    dimension_match = re.search(dimension_pattern, content)
    if dimension_match:
        dimension = dimension_match.group(1)
        return dimension
    return "未知"

def extract_version(content):
    """从文件内容中提取版本号"""
    version_pattern = r'v(\d+\.\d+)'
    version_match = re.search(version_pattern, content)
    if version_match:
        return version_match.group(1)
    return "未知"

def count_by_dimension(theory_files):
    """按维度统计理论文件数量"""
    dimension_counts = defaultdict(int)
    
    for file_path in theory_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                dimension = extract_dimension(content)
                dimension_counts[dimension] += 1
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
    
    return dimension_counts

def check_unindexed_files(index_file, theory_files):
    """检查未被索引的文件"""
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            index_content = f.read()
    except Exception as e:
        print(f"读取索引文件 {index_file} 时出错: {e}")
        return []
    
    unindexed_files = []
    
    for file_path in theory_files:
        if file_path.endswith("_en.md"):
            continue  # 跳过英文版本文件
        
        file_name = os.path.basename(file_path)
        if file_name not in index_content and f"({file_name})" not in index_content:
            unindexed_files.append(file_path)
    
    return unindexed_files

def check_language_sync(theory_files):
    """检查中英文文件同步情况"""
    chinese_files = [f for f in theory_files if not f.endswith("_en.md") and f.startswith("formal_theory_")]
    english_files = [f for f in theory_files if f.endswith("_en.md")]
    
    missing_english = []
    missing_chinese = []
    
    for cn_file in chinese_files:
        en_file = cn_file[:-3] + "_en.md"
        if en_file not in english_files:
            missing_english.append(cn_file)
    
    for en_file in english_files:
        cn_file = en_file[:-6] + ".md"
        if cn_file not in chinese_files:
            missing_chinese.append(en_file)
    
    return missing_english, missing_chinese

def check_version_consistency(theory_files):
    """检查版本一致性"""
    versions = {}
    inconsistent_files = []
    
    for file_path in theory_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                version = extract_version(content)
                versions[file_path] = version
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
    
    if len(set(versions.values())) > 1:
        # 找出最常见的版本号
        version_counter = Counter(versions.values())
        most_common_version = version_counter.most_common(1)[0][0]
        
        for file_path, version in versions.items():
            if version != most_common_version and version != "未知":
                inconsistent_files.append((file_path, version, most_common_version))
    
    return inconsistent_files, most_common_version if versions else "未知"

def check_links(theory_files):
    """检查链接完整性"""
    broken_links = []
    
    for file_path in theory_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 查找所有Markdown链接
                link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
                links = re.findall(link_pattern, content)
                
                for link_text, link_target in links:
                    # 忽略外部链接和锚点链接
                    if link_target.startswith(('http', 'www', '#')):
                        continue
                    
                    # 构建链接的绝对路径
                    if not os.path.isabs(link_target):
                        target_path = os.path.normpath(os.path.join(os.path.dirname(file_path), link_target))
                    else:
                        target_path = link_target
                    
                    # 检查文件是否存在
                    if not os.path.exists(target_path):
                        broken_links.append((file_path, link_text, link_target))
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
    
    return broken_links

def generate_markdown_report(args, stats):
    """生成Markdown格式的报告"""
    report = f"""# 宇宙本论形式化理论体系维护报告

生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 统计信息

- 理论文件总数: {stats['total_files']}
- 中文理论文件数: {stats['chinese_files']}
- 英文理论文件数: {stats['english_files']}
- 最常用版本号: {stats['common_version']}

## 维度分布

| 维度 | 文件数量 |
|------|----------|
"""
    
    # 按维度从高到低排序
    sorted_dimensions = sorted(stats['dimension_counts'].items(), 
                              key=lambda x: float('inf') if x[0] == '∞' else int(x[0]), 
                              reverse=True)
    
    for dimension, count in sorted_dimensions:
        report += f"| {dimension} | {count} |\n"
    
    report += f"""
## 版本一致性检查

"""
    
    if stats['inconsistent_versions']:
        report += f"发现 {len(stats['inconsistent_versions'])} 个版本不一致的文件：\n\n"
        for file_path, version, common_version in stats['inconsistent_versions']:
            report += f"- {os.path.basename(file_path)}: 当前版本 {version}，应为 {common_version}\n"
    else:
        report += "所有文件版本一致。\n"
    
    report += f"""
## 未索引文件检查

### 中文索引

"""
    
    if stats['unindexed_cn']:
        report += f"发现 {len(stats['unindexed_cn'])} 个未在中文索引中的文件：\n\n"
        for file_path in stats['unindexed_cn']:
            report += f"- {os.path.basename(file_path)}\n"
    else:
        report += "所有中文文件已被索引。\n"
    
    report += f"""
### 英文索引

"""
    
    if stats['unindexed_en']:
        report += f"发现 {len(stats['unindexed_en'])} 个未在英文索引中的文件：\n\n"
        for file_path in stats['unindexed_en']:
            report += f"- {os.path.basename(file_path)}\n"
    else:
        report += "所有英文文件已被索引。\n"
    
    report += f"""
## 中英文同步检查

"""
    
    if stats['missing_english']:
        report += f"发现 {len(stats['missing_english'])} 个缺少英文版本的中文文件：\n\n"
        for file_path in stats['missing_english']:
            report += f"- {os.path.basename(file_path)}\n"
    else:
        report += "所有中文文件都有对应的英文版本。\n"
    
    report += f"""
## 链接完整性检查

"""
    
    if stats['broken_links']:
        report += f"发现 {len(stats['broken_links'])} 个损坏的链接：\n\n"
        for file_path, link_text, link_target in stats['broken_links']:
            report += f"- {os.path.basename(file_path)}: [{link_text}]({link_target})\n"
    else:
        report += "所有链接都是有效的。\n"
    
    report += f"""
## 维护建议

1. """
    
    recommendations = []
    
    if stats['unindexed_cn'] or stats['unindexed_en']:
        recommendations.append("添加未索引的文件到相应的索引文件中")
    
    if stats['missing_english']:
        recommendations.append("为缺少英文版本的文件创建对应的英文文档")
    
    if stats['inconsistent_versions']:
        recommendations.append("更新版本不一致的文件到最新版本")
    
    if stats['broken_links']:
        recommendations.append("修复损坏的链接")
    
    if not recommendations:
        recommendations.append("理论体系维护良好，无需立即采取行动")
    
    report += "\n2. ".join(recommendations)
    
    return report

def main():
    args = parse_args()
    
    # 查找所有理论文件
    theory_files = find_md_files(args.theory_dir)
    
    # 按维度统计理论文件
    dimension_counts = count_by_dimension(theory_files)
    
    # 检查未索引的文件
    unindexed_cn = check_unindexed_files(args.index, theory_files)
    unindexed_en = []
    if os.path.exists(args.index_en):
        unindexed_en = check_unindexed_files(args.index_en, [f for f in theory_files if f.endswith("_en.md")])
    
    # 检查中英文文件同步情况
    missing_english, missing_chinese = check_language_sync(theory_files)
    
    # 检查版本一致性
    inconsistent_versions, common_version = check_version_consistency(theory_files)
    
    # 检查链接完整性
    broken_links = check_links(theory_files)
    
    # 统计信息
    stats = {
        'total_files': len(theory_files),
        'chinese_files': len([f for f in theory_files if not f.endswith("_en.md")]),
        'english_files': len([f for f in theory_files if f.endswith("_en.md")]),
        'dimension_counts': dimension_counts,
        'unindexed_cn': unindexed_cn,
        'unindexed_en': unindexed_en,
        'missing_english': missing_english,
        'missing_chinese': missing_chinese,
        'inconsistent_versions': inconsistent_versions,
        'common_version': common_version,
        'broken_links': broken_links
    }
    
    # 生成报告
    report = generate_markdown_report(args, stats)
    
    # 写入文件
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"维护报告已生成：{args.output}")

if __name__ == "__main__":
    main() 