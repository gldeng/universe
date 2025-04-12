#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
添加未索引理论文件工具

此工具用于自动将未索引的理论文件添加到索引文件中。
通过分析文件名和内容，确定理论的维度和分类，然后将它们添加到适当的索引部分。

使用方法：
python add_unindexed_files.py --unindexed_file ../output/unindexed_files.json --index ../formal_theory.md --index-en ../formal_theory_en.md
"""

import os
import sys
import json
import re
import argparse
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description="添加未索引理论文件到索引中")
    parser.add_argument("--unindexed_file", default="../output/unindexed_files.json", help="未索引文件JSON数据")
    parser.add_argument("--index", default="../formal_theory.md", help="中文索引文件")
    parser.add_argument("--index-en", default="../formal_theory_en.md", help="英文索引文件")
    parser.add_argument("--theory_dir", default="../formal_theory", help="理论文件目录")
    parser.add_argument("--dry-run", action="store_true", help="仅模拟运行，不实际修改文件")
    return parser.parse_args()

def extract_dimension_from_file(file_path):
    """从理论文件中提取维度信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 尝试从文件内容中提取维度标记
        dimension_match = re.search(r'维度:\s*([\d.∞]+)', content)
        if dimension_match:
            dimension_str = dimension_match.group(1)
            if dimension_str == "∞":
                return float('inf')
            try:
                return float(dimension_str)
            except ValueError:
                return None
        return None
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return None

def infer_dimension_from_filename(filename):
    """从文件名推断可能的维度"""
    # 根据文件名中的关键词推断维度
    dimension_indicators = {
        # 基础操作 (D1-D2)
        'flip_operation': 1,
        'xor_operation': 2,
        'shift_operation': 2,
        'ushift_operation': 2,
        
        # 底层理论 (D3-D4)
        'recursive_operation': 3,
        
        # 基础维度理论 (D5-D9)
        'biological_information': 5,
        'cellular_complexity': 5,
        'biological_clock': 5,
        'immune_system': 5,
        'neurogenesis': 5,
        'quantum_xor_entanglement_recursive': 5,
        'flip_based_emergent': 5,
        'psychological_dynamics': 5,
        'information_dynamics': 5,
        
        # 中维理论 (D10-D14)
        'cosmic_ontology': 10,
        'unified_physics': 10,
        'consciousness_essence': 11,
        'dark_matter_dark_energy': 13,
        
        # 高维理论 (D15-D24)
        'quantum_classical_boundary': 17,
        'prime_frequency_harmony': 18,
        
        # 极高维理论 (D25+)
        'transdimensional_unified': 41,
        'superintelligent_consciousness': 42,
        'quantum_information_entropy_field': 42
    }
    
    # 将英文文件名后缀去除
    base_filename = filename.replace('_en.md', '.md')
    
    for key, dim in dimension_indicators.items():
        if key in base_filename:
            return dim
    
    # 如果无法从关键词推断，则分析文件名结构
    if 'shift_' in base_filename or 'unshift_' in base_filename:
        return 7  # 默认为基础操作的高级应用
    
    if 'quantum_' in base_filename:
        return 9  # 默认量子理论
    
    return 15  # 默认为中等维度理论

def classify_theory(dimension):
    """根据维度对理论进行分类"""
    if dimension == float('inf'):
        return "顶级维度理论（D∞）", "Top-Level Dimension Theory (D∞)"
    elif 50 <= dimension <= 66:
        return "超高维理论（D50-D66）", "Ultra-High Dimension Theory (D50-D66)"
    elif 43 <= dimension <= 49:
        return "极高维理论（D43-D49）", "Extremely High Dimension Theory (D43-D49)"
    elif 34 <= dimension <= 42:
        return "极高维理论（D34-D42）", "Extremely High Dimension Theory (D34-D42)"
    elif 25 <= dimension <= 33:
        return "非常高维理论（D25-D33）", "Very High Dimension Theory (D25-D33)"
    elif 15 <= dimension <= 24:
        return "高维理论（D15-D24）", "High Dimension Theory (D15-D24)"
    elif 10 <= dimension <= 14:
        return "中维理论（D10-D14）", "Medium Dimension Theory (D10-D14)"
    elif 5 <= dimension <= 9:
        return "基础维度理论（D5-D9）", "Basic Dimension Theory (D5-D9)"
    elif 0 <= dimension <= 4:
        return "底层理论（D0-D4）", "Fundamental Theory (D0-D4)"
    else:
        return "未分类理论", "Unclassified Theory"

def get_theory_title(filename, is_english=False):
    """根据文件名生成理论标题"""
    # 移除前缀和后缀
    name = filename.replace('formal_theory_', '').replace('.md', '').replace('_en', '')
    
    # 将下划线转换为空格，并将每个单词首字母大写
    words = name.split('_')
    
    if is_english:
        # 英文版本
        title = ' '.join(word.capitalize() for word in words)
        return f"Formalized Theory of {title}"
    else:
        # 中文版本 - 使用映射表将关键词转为中文
        cn_keywords = {
            'quantum': '量子',
            'consciousness': '意识',
            'information': '信息',
            'energy': '能量',
            'dark': '暗',
            'matter': '物质',
            'unified': '统一',
            'physics': '物理学',
            'theory': '理论',
            'dimension': '维度',
            'cosmic': '宇宙',
            'ontology': '本体论',
            'shift': '位移',
            'unshift': '逆位移',
            'xor': '异或',
            'flip': '翻转',
            'recursion': '递归',
            'emergence': '涌现',
            'complexity': '复杂性',
            'state': '状态',
            'symmetry': '对称性',
            'primitive': '原始',
            'dynamics': '动力学',
            'singularity': '奇点',
            'holography': '全息',
            'entanglement': '纠缠',
            'network': '网络',
            'field': '场',
            'boundary': '边界',
            'foundation': '基础',
            'cognition': '认知',
            'classical': '经典',
            'entropy': '熵',
            'mechanism': '机制',
            'paradigm': '范式',
            'element': '元素',
            'compression': '压缩',
            'transition': '转换',
            'oscillation': '振荡',
            'projection': '投影',
            'transformation': '变换',
            'regulation': '调节',
            'preservation': '保持',
            'inversion': '反转',
            'mapping': '映射',
            'probability': '概率',
            'flow': '流',
            'conservation': '守恒',
            'pattern': '模式',
            'reduction': '减少',
            'recognition': '识别',
            'stability': '稳定性',
            'duality': '二元性',
            'temporal': '时间',
            'spatial': '空间',
            'causality': '因果性',
            'memory': '记忆',
            'soul': '灵魂',
            'coherence': '相干性',
            'mental': '心理',
            'health': '健康',
            'neutrino': '中微子',
            'gravity': '引力',
            'frequency': '频率',
            'resonance': '共振',
            'essence': '本质',
            'structure': '结构',
            'topology': '拓扑',
            'evolution': '演化',
            'cycle': '循环',
            'measurement': '测量',
            'integration': '整合',
            'generation': '生成',
            'bifurcation': '分岔',
            'fractal': '分形',
            'feedback': '反馈'
        }
        
        # 尝试将英文关键词转为中文
        cn_name = []
        for word in words:
            if word in cn_keywords:
                cn_name.append(cn_keywords[word])
            else:
                # 如果没有对应的中文词，保留英文
                cn_name.append(word)
        
        title = ''.join(cn_name)
        return f"{title}的严格形式化描述"

def add_theory_to_index(index_content, filename, dimension, is_english=False):
    """将理论添加到索引中的适当位置"""
    # 获取理论分类
    cn_category, en_category = classify_theory(dimension)
    category = en_category if is_english else cn_category
    
    # 查找分类部分
    category_pattern = f"^###\\s*{re.escape(category)}$"
    category_match = re.search(category_pattern, index_content, re.MULTILINE)
    
    if not category_match:
        # 如果找不到分类，尝试创建新分类
        # 这需要确定在内容中的合适位置
        print(f"警告: 找不到分类 '{category}'，将添加到文件末尾")
        
        # 获取理论标题和链接
        title = get_theory_title(filename, is_english)
        link_path = f"formal_theory/{filename}"
        
        # 准备要添加的内容
        if is_english:
            new_entry = f"\n### {category}\n[{title} [Dimension: {dimension}]]({link_path})  \n"
        else:
            new_entry = f"\n### {category}\n[{title} [维度: {dimension}]]({link_path})  \n"
        
        # 添加到文件末尾
        return index_content + new_entry
    
    # 找到分类的下一个分类或文件结尾
    next_category_match = re.search(r"^###\s+", index_content[category_match.end():], re.MULTILINE)
    
    if next_category_match:
        insert_position = category_match.end() + next_category_match.start()
    else:
        insert_position = len(index_content)
    
    # 获取理论标题和链接
    title = get_theory_title(filename, is_english)
    link_path = f"formal_theory/{filename}"
    
    # 准备要添加的内容
    if is_english:
        new_entry = f"[{title} [Dimension: {dimension}]]({link_path})  \n"
    else:
        new_entry = f"[{title} [维度: {dimension}]]({link_path})  \n"
    
    # 在分类的最后一个条目后插入新条目
    section = index_content[category_match.end():insert_position]
    last_entry_match = re.search(r"(\]\([^)]+\))  \n", section)
    
    if last_entry_match:
        insert_at = category_match.end() + last_entry_match.end()
        return index_content[:insert_at] + new_entry + index_content[insert_at:]
    else:
        # 如果找不到最后一个条目，在分类标题后添加
        insert_at = category_match.end()
        return index_content[:insert_at] + "\n" + new_entry + index_content[insert_at:]

def main():
    args = parse_args()
    
    try:
        # 加载未索引文件数据
        with open(args.unindexed_file, 'r', encoding='utf-8') as f:
            unindexed_data = json.load(f)
        
        cn_unindexed = unindexed_data.get("chinese", [])
        en_unindexed = unindexed_data.get("english", [])
        
        print(f"加载了 {len(cn_unindexed)} 个未索引的中文文件和 {len(en_unindexed)} 个未索引的英文文件")
        
        # 读取索引文件
        with open(args.index, 'r', encoding='utf-8') as f:
            cn_index_content = f.read()
        
        with open(args.index_en, 'r', encoding='utf-8') as f:
            en_index_content = f.read()
        
        # 按维度分组理论文件
        cn_theories_by_dimension = defaultdict(list)
        en_theories_by_dimension = defaultdict(list)
        
        # 处理中文文件
        for filename in cn_unindexed:
            file_path = os.path.join(args.theory_dir, filename)
            dimension = extract_dimension_from_file(file_path)
            
            if dimension is None:
                dimension = infer_dimension_from_filename(filename)
            
            cn_theories_by_dimension[dimension].append(filename)
        
        # 处理英文文件
        for filename in en_unindexed:
            file_path = os.path.join(args.theory_dir, filename)
            dimension = extract_dimension_from_file(file_path)
            
            if dimension is None:
                base_filename = filename.replace('_en.md', '.md')
                dimension = infer_dimension_from_filename(base_filename)
            
            en_theories_by_dimension[dimension].append(filename)
        
        # 添加理论到索引
        updated_cn_index = cn_index_content
        updated_en_index = en_index_content
        
        # 按维度从高到低添加中文理论
        for dimension in sorted(cn_theories_by_dimension.keys(), reverse=True):
            for filename in cn_theories_by_dimension[dimension]:
                print(f"添加中文理论: {filename} [维度: {dimension}]")
                if not args.dry_run:
                    updated_cn_index = add_theory_to_index(updated_cn_index, filename, dimension, False)
        
        # 按维度从高到低添加英文理论
        for dimension in sorted(en_theories_by_dimension.keys(), reverse=True):
            for filename in en_theories_by_dimension[dimension]:
                print(f"添加英文理论: {filename} [Dimension: {dimension}]")
                if not args.dry_run:
                    updated_en_index = add_theory_to_index(updated_en_index, filename, dimension, True)
        
        # 写回索引文件
        if not args.dry_run:
            with open(args.index, 'w', encoding='utf-8') as f:
                f.write(updated_cn_index)
            
            with open(args.index_en, 'w', encoding='utf-8') as f:
                f.write(updated_en_index)
            
            print(f"索引文件已更新!")
        else:
            print("模拟运行完成，未实际修改索引文件")
        
    except Exception as e:
        print(f"处理未索引文件时出错: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 