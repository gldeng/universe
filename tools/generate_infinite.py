#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from theory_generator import TheoryGenerator

def main():
    """生成无限维度理论"""
    generator = TheoryGenerator('../formal_theory/formal_theory_cosmic_ontology.md', 'generated_theories')
    
    # 设置无限维度对应的理论名称
    generator.dimension_spectrum[float('inf')] = "元理论"
    
    # 生成无限维度理论
    filename, content = generator.generate_theory(float('inf'))
    output_path = os.path.join('generated_theories', filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'已生成 {filename}')
    
    # 生成英文版本
    english_content = generator._create_english_version(content)
    english_filename = filename.replace('.md', '_en.md')
    english_path = os.path.join('generated_theories', english_filename)
    
    with open(english_path, 'w', encoding='utf-8') as f:
        f.write(english_content)
    
    print(f'已生成 {english_filename}')

if __name__ == "__main__":
    main() 