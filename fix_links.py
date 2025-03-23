#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
链接修复脚本
该脚本用于修复文档中的损坏链接
核心理论版本: v9.3
"""

import os
import re
import sys

def fix_education_history_link():
    """修复 education/versions/history.md 中的格式错误链接"""
    file_path = "education/versions/history.md"
    
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并修复格式错误的链接
        wrong_pattern = r'\[\#中文版\) \| \[English Version\]\(\#english-version\) \| \[返回教育目录\]\(\.\.\/README\.md\]'
        correct_link = '[中文版](#中文版) | [English Version](#english-version) | [返回教育目录](../README.md)'
        
        if re.search(wrong_pattern, content):
            fixed_content = re.sub(wrong_pattern, correct_link, content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"已修复 {file_path} 中的链接")
            return True
        else:
            print(f"在 {file_path} 中未找到需要修复的链接格式")
            return False
    
    except Exception as e:
        print(f"修复 {file_path} 时出错: {e}")
        return False

def create_missing_theory_files():
    """创建 theories 目录下缺失的文件"""
    missing_files = [
        "theories/ai_computational_explanations.md",
        "theories/economic_classical_quantum.md"
    ]
    
    templates = {
        "ai_computational_explanations.md": """# AI与计算的量子经典解释
**核心理论版本: v9.3**

## 概述
本文档提供了关于人工智能和计算在量子经典二元论框架下的解释。

## 目录
- [中文版](#中文版)
- [English Version](#english-version)

## 中文版
### 量子域与经典域中的AI
在量子经典二元论框架下，AI系统可以被视为在量子域和经典域之间运作的复杂系统。

### 计算的本质与观察者维度
计算过程可以理解为有序信息在观察者维度中的处理流程，涉及到从量子可能性到经典确定性的转换。

## English Version
### AI in Quantum and Classical Domains
In the quantum-classical dualism framework, AI systems can be viewed as complex systems operating between quantum and classical domains.

### The Nature of Computation and Observer Dimensions
Computational processes can be understood as the ordered processing of information across observer dimensions, involving the transition from quantum possibilities to classical determinism.
""",
        "economic_classical_quantum.md": """# 经济学的量子经典解释
**核心理论版本: v9.3**

## 概述
本文档提供了经济学现象在量子经典二元论框架下的解释。

## 目录
- [中文版](#中文版)
- [English Version](#english-version)

## 中文版
### 量子经济学基础
经济系统可以被视为大规模量子纠缠网络，其中个体决策者的行为呈现出量子叠加特性。

### 市场波动与经典化
市场波动可以理解为量子可能性向经典结果的经典化过程，受到集体观察者意识的影响。

## English Version
### Foundations of Quantum Economics
Economic systems can be viewed as large-scale quantum entanglement networks where individual decision-makers' behaviors exhibit quantum superposition properties.

### Market Fluctuations and Classicalization
Market fluctuations can be understood as the classicalization process of quantum possibilities into classical outcomes, influenced by collective observer consciousness.
"""
    }
    
    created_count = 0
    for file_path in missing_files:
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        
        if not os.path.exists(file_path):
            base_name = os.path.basename(file_path)
            with open(file_path, 'w', encoding='utf-8') as f:
                if base_name in templates:
                    f.write(templates[base_name])
                else:
                    f.write(f"# {base_name[:-3].replace('_', ' ').title()}\n**核心理论版本: v9.3**\n\n内容待添加")
            
            print(f"已创建文件: {file_path}")
            created_count += 1
    
    return created_count

def update_theories_readme_links():
    """更新 theories/README.md 中的链接"""
    file_path = "theories/README.md"
    
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换损坏的链接
        content = content.replace(
            "[ai_computational_explanations.md]", 
            "[AI与计算的量子经典解释](ai_computational_explanations.md)"
        )
        content = content.replace(
            "[economic_classical_quantum.md]", 
            "[经济学的量子经典解释](economic_classical_quantum.md)"
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"已更新 {file_path} 中的链接")
        return True
    
    except Exception as e:
        print(f"更新 {file_path} 中的链接时出错: {e}")
        return False

def main():
    """主函数"""
    print("开始修复链接...")
    
    # 修复education/versions/history.md中的链接
    fix_education_history_link()
    
    # 创建缺失的理论文件
    created_count = create_missing_theory_files()
    print(f"已创建 {created_count} 个缺失文件")
    
    # 更新theories/README.md中的链接
    update_theories_readme_links()
    
    print("链接修复完成!")

if __name__ == "__main__":
    main() 