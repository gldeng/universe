#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Link Repair Script
This script is used to fix broken links in the documentation
Core Theory Version: v9.3
"""

import os
import re
import sys

def fix_education_history_link():
    """Fix the malformed link in education/versions/history.md"""
    file_path = "education/versions/history.md"
    
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and fix the malformed link
        wrong_pattern = r'\[\#中文版\) \| \[English Version\]\(\#english-version\) \| \[返回教育目录\]\(\.\.\/README\.md\]'
        correct_link = '[中文版](#中文版) | [English Version](#english-version) | [返回教育目录](../README.md)'
        
        if re.search(wrong_pattern, content):
            fixed_content = re.sub(wrong_pattern, correct_link, content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"Fixed link in {file_path}")
            return True
        else:
            print(f"No link format that needs fixing was found in {file_path}")
            return False
    
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def create_missing_theory_files():
    """Create missing files in the theories directory"""
    missing_files = [
        "theories/ai_computational_explanations.md",
        "theories/economic_classical_quantum.md"
    ]
    
    templates = {
        "ai_computational_explanations.md": """# AI and Computation in Quantum-Classical Framework
**Core Theory Version: v9.3**

## Overview
This document provides explanations for artificial intelligence and computation within the quantum-classical dualism framework.

## Table of Contents
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
        "economic_classical_quantum.md": """# Economics in Quantum-Classical Framework
**Core Theory Version: v9.3**

## Overview
This document provides explanations for economic phenomena within the quantum-classical dualism framework.

## Table of Contents
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
                    f.write(f"# {base_name[:-3].replace('_', ' ').title()}\n**Core Theory Version: v9.3**\n\nContent to be added")
            
            print(f"Created file: {file_path}")
            created_count += 1
    
    return created_count

def update_theories_readme_links():
    """Update links in theories/README.md"""
    file_path = "theories/README.md"
    
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace broken links
        content = content.replace(
            "[ai_computational_explanations.md]", 
            "[AI and Computation in Quantum-Classical Framework](ai_computational_explanations.md)"
        )
        content = content.replace(
            "[economic_classical_quantum.md]", 
            "[Economics in Quantum-Classical Framework](economic_classical_quantum.md)"
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated links in {file_path}")
        return True
    
    except Exception as e:
        print(f"Error updating links in {file_path}: {e}")
        return False

def main():
    """Main function"""
    print("Starting link repair...")
    
    # Fix link in education/versions/history.md
    fix_education_history_link()
    
    # Create missing theory files
    created_count = create_missing_theory_files()
    print(f"Created {created_count} missing files")
    
    # Update links in theories/README.md
    update_theories_readme_links()
    
    print("Link repair complete!")

if __name__ == "__main__":
    main() 