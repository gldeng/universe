#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import random
import argparse
import math
import numpy as np
from typing import Dict, List, Any, Tuple, Set, Optional

class TheoryGenerator:
    """从宇宙本论推导出所有相关理论的生成器"""
    
    def __init__(self, cosmic_ontology_path: str, output_dir: str = "generated_theories"):
        """
        初始化理论生成器
        
        Args:
            cosmic_ontology_path: 宇宙本论文件路径
            output_dir: 生成理论的输出目录
        """
        self.cosmic_ontology_path = cosmic_ontology_path
        self.output_dir = output_dir
        self.version = "36.0"  # 默认版本号
        
        # 基本操作集
        self.basic_operations = ["FLIP", "XOR", "SHIFT", "USHIFT"]
        
        # 维度谱系 - 中文名称
        self.dimension_spectrum = {
            -3: "元前奇点理论",
            -2: "前奇点理论",
            -1: "原始奇点理论",
            0: "零点理论",
            1: "原始存在理论",
            2: "原始点理论",
            3: "原始对偶理论",
            4: "原始组合理论",
            5: "基础系统理论",
            6: "空间构造理论",
            7: "递归操作理论",
            8: "基础系统理论",
            9: "递归自参照系统",
            10: "宇宙本论",
            11: "哲学基础理论",
            12: "时空理论",
            13: "意识与自由意志理论",
            14: "信息场理论",
            15: "逻辑多维拓扑理论",
            16: "量子熵动力学",
            17: "信息波动力学",
            18: "维度和谐理论",
            19: "量子经典统一理论",
            20: "宇宙维度理论",
            21: "创世记忆理论",
            22: "多宇宙理论",
            23: "递归元界理论",
            24: "千禧年数学问题超维度解决理论",
            25: "人类未解十大问题的形式化统一理论",
            26: "时空信息波理论",
            27: "宇宙最终态理论",
            28: "量子意识理论",
            29: "跨维度纠缠因果理论",
            30: "绝对统一宇宙场理论",
            31: "超信息奇点理论",
            32: "全域整合原理",
            33: "超越性意识量子场理论",
            "∞": "元理论"
        }
        
        # 对应的英文名称
        self.english_dimension_spectrum = {
            -3: "Meta Pre-Singularity Theory",
            -2: "Pre-Singularity Theory",
            -1: "Primitive Singularity Theory",
            0: "Zero Point Theory",
            1: "Primitive Existence Theory",
            2: "Primitive Point Theory",
            3: "Primitive Duality Theory",
            4: "Primitive Composition Theory",
            5: "Base System Theory",
            6: "Spatial Construction Theory",
            7: "Recursive Operation Theory",
            8: "Fundamental System Theory", 
            9: "Recursive Self-Reference System",
            10: "Cosmic Ontology",
            11: "Philosophical Foundation Theory",
            12: "Spacetime Theory",
            13: "Consciousness and Free Will Theory",
            14: "Information Field Theory",
            15: "Logical Multidimensional Topology Theory",
            16: "Quantum Entropy Dynamics",
            17: "Information Wave Dynamics",
            18: "Dimensional Harmony Theory",
            19: "Quantum-Classical Unification Theory",
            20: "Universal Dimensional Theory",
            21: "Genesis Memory Theory",
            22: "Multiverse Theory",
            23: "Recursive Meta-Realm Theory",
            24: "Millennium Mathematical Problems Hyperdimensional Solution Theory",
            25: "Unified Formal Theory of Human Unsolved Problems",
            26: "Spacetime Information Wave Theory",
            27: "Universe Final State Theory",
            28: "Quantum Consciousness Theory",
            29: "Transdimensional Entanglement Causality Theory",
            30: "Absolute Unified Cosmic Field Theory",
            31: "Hyper-Information Singularity Theory",
            32: "Omniverse Integration Principle",
            33: "Transcendental Consciousness Quantum Field Theory",
            "∞": "Meta Theory"
        }
        
        # 理论前缀词汇
        self.theory_prefixes = [
            "Quantum", "Cosmic", "Transcendental", "Dimensional", "Universal", 
            "Fundamental", "Recursive", "Hyperdimensional", "Absolute", "Primitive",
            "Meta", "Omni", "Unified", "Integrated", "Transdimensional"
        ]
        
        # 理论中间词汇
        self.theory_middle_terms = [
            "Field", "Wave", "Operator", "Singularity", "Structure", "Harmony",
            "Dynamics", "Symmetry", "Principle", "Existence", "Consciousness",
            "Information", "Entanglement", "Resonance", "Topology"
        ]
        
        # 理论后缀词汇
        self.theory_suffixes = [
            "Theory", "Paradigm", "Framework", "System", "Ontology", "Mechanics",
            "Theorem", "Construct", "Foundation", "Principle", "Dynamics"
        ]
        
        # 宇宙本论内容
        self.cosmic_ontology_content = self._read_cosmic_ontology()
        
        # 提取公理、定理、操作定义等
        self.axioms = self._extract_axioms()
        self.theorems = self._extract_theorems()
        self.operation_definitions = self._extract_operation_definitions()
        self.formulas = self._extract_formulas()
        
        # 理论模板结构
        self.theory_templates = self._create_theory_templates()
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _read_cosmic_ontology(self) -> str:
        """读取宇宙本论内容"""
        try:
            with open(self.cosmic_ontology_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 提取版本号
                version_match = re.search(r'v(\d+\.\d+)', content)
                if version_match:
                    self.version = version_match.group(1)
                
                return content
        except Exception as e:
            print(f"读取宇宙本论文件错误: {e}")
            return ""
    
    def _extract_axioms(self) -> List[Dict[str, str]]:
        """提取宇宙本论中的公理"""
        axioms = []
        axiom_pattern = re.compile(r'\*\*公理(\d+)[^*]*\*\*\s*(.*?)(?=\n\n)', re.DOTALL)
        
        for match in axiom_pattern.finditer(self.cosmic_ontology_content):
            axiom_number = match.group(1)
            axiom_content = match.group(2).strip()
            
            # 提取公理中的公式
            formula_pattern = re.compile(r'\$`(.*?)`\$', re.DOTALL)
            formulas = [m.group(1) for m in formula_pattern.finditer(axiom_content)]
            
            axioms.append({
                "number": axiom_number,
                "content": axiom_content,
                "formulas": formulas
            })
        
        return axioms
    
    def _extract_theorems(self) -> List[Dict[str, str]]:
        """提取宇宙本论中的定理"""
        theorems = []
        theorem_pattern = re.compile(r'\*\*定理(\d+)[^*]*\*\*\s*(.*?)(?=\*证明\*|\n\n)', re.DOTALL)
        proof_pattern = re.compile(r'\*证明\*:\s*(.*?)(?=\n\n|$)', re.DOTALL)
        
        for match in theorem_pattern.finditer(self.cosmic_ontology_content):
            theorem_number = match.group(1)
            theorem_content = match.group(2).strip()
            
            # 查找对应的证明
            proof_start = match.end()
            proof_match = proof_pattern.search(self.cosmic_ontology_content[proof_start:])
            proof_content = proof_match.group(1).strip() if proof_match else ""
            
            # 提取定理中的公式
            formula_pattern = re.compile(r'\$`(.*?)`\$', re.DOTALL)
            formulas = [m.group(1) for m in formula_pattern.finditer(theorem_content)]
            
            theorems.append({
                "number": theorem_number,
                "content": theorem_content,
                "proof": proof_content,
                "formulas": formulas
            })
        
        return theorems
    
    def _extract_operation_definitions(self) -> Dict[str, str]:
        """提取基本操作的定义"""
        operations = {}
        
        # 提取FLIP操作定义
        flip_pattern = re.compile(r'FLIP操作.*?定义.*?为:?\s*\$`(.*?)`\$', re.DOTALL | re.IGNORECASE)
        flip_match = flip_pattern.search(self.cosmic_ontology_content)
        if flip_match:
            operations["FLIP"] = flip_match.group(1)
        
        # 提取XOR操作定义
        xor_pattern = re.compile(r'XOR操作.*?定义.*?为:?\s*\$`(.*?)`\$', re.DOTALL | re.IGNORECASE)
        xor_match = xor_pattern.search(self.cosmic_ontology_content)
        if xor_match:
            operations["XOR"] = xor_match.group(1)
        
        # 提取SHIFT操作定义
        shift_pattern = re.compile(r'SHIFT操作.*?定义.*?为:?\s*\$`(.*?)`\$', re.DOTALL | re.IGNORECASE)
        shift_match = shift_pattern.search(self.cosmic_ontology_content)
        if shift_match:
            operations["SHIFT"] = shift_match.group(1)
        else:
            # 尝试其他模式
            shift_pattern = re.compile(r'SHIFT\(.*?\) = (.*?)(?=\n)', re.DOTALL)
            shift_match = shift_pattern.search(self.cosmic_ontology_content)
            if shift_match:
                operations["SHIFT"] = shift_match.group(1)
        
        # 提取USHIFT操作定义
        ushift_pattern = re.compile(r'USHIFT操作.*?定义.*?为:?\s*\$`(.*?)`\$', re.DOTALL | re.IGNORECASE)
        ushift_match = ushift_pattern.search(self.cosmic_ontology_content)
        if ushift_match:
            operations["USHIFT"] = ushift_match.group(1)
        
        # 如果没有找到，使用默认定义
        if "FLIP" not in operations:
            operations["FLIP"] = "FLIP(x) = \\neg x"
        if "XOR" not in operations:
            operations["XOR"] = "x \\oplus y"
        if "SHIFT" not in operations:
            operations["SHIFT"] = "SHIFT(\\mathcal{U}) = \\mathcal{U} \\oplus \\Delta_{\\tau}"
        if "USHIFT" not in operations:
            operations["USHIFT"] = "USHIFT(x) = FLIP(SHIFT(FLIP(x)))"
        
        return operations
    
    def _extract_formulas(self) -> List[str]:
        """提取宇宙本论中的所有公式"""
        formula_pattern = re.compile(r'\$`(.*?)`\$', re.DOTALL)
        return [m.group(1) for m in formula_pattern.finditer(self.cosmic_ontology_content)]
    
    def _create_theory_templates(self) -> Dict[str, Any]:
        """创建理论模板"""
        templates = {
            "low_dim": {
                "sections": [
                    "核心定义", "基本操作", "理论基础", "直接应用", "与其他理论的关系"
                ],
                "subsections": {
                    "核心定义": ["基本概念定义", "公理体系", "基本性质"],
                    "基本操作": ["操作规则", "操作特性"],
                    "理论基础": ["基础结构", "理论推导"],
                    "直接应用": ["应用场景", "验证方法"],
                    "与其他理论的关系": ["理论映射", "维度转换"]
                }
            },
            "mid_dim": {
                "sections": [
                    "核心理论", "直接推论", "扩展理论", "应用与验证", "形式化证明", "理论引用关系分析"
                ],
                "subsections": {
                    "核心理论": ["基本公理系统", "基本操作定义", "状态空间定义", "状态演化规则"],
                    "直接推论": ["推论1", "推论2", "推论3"],
                    "扩展理论": ["扩展1", "扩展2", "扩展3"],
                    "应用与验证": ["应用场景", "验证方法"],
                    "形式化证明": ["定理1", "定理2", "定理3"],
                    "理论引用关系分析": ["理论维度定位", "理论依赖结构"]
                }
            },
            "high_dim": {
                "sections": [
                    "核心理论", "直接推论", "扩展理论", "应用与验证", "形式化证明", "超维度扩展", "理论引用关系分析"
                ],
                "subsections": {
                    "核心理论": ["基本公理系统", "基本操作定义", "状态空间定义", "状态演化规则", "维度跃迁机制"],
                    "直接推论": ["推论1", "推论2", "推论3", "推论4"],
                    "扩展理论": ["扩展1", "扩展2", "扩展3", "扩展4"],
                    "应用与验证": ["应用场景", "验证方法", "跨维度应用"],
                    "形式化证明": ["定理1", "定理2", "定理3", "定理4"],
                    "超维度扩展": ["维度统一", "跨维度映射", "维度转换协议"],
                    "理论引用关系分析": ["理论维度定位", "理论依赖结构", "维度谱系位置"]
                }
            }
        }
        return templates
    
    def _get_template_for_dimension(self, dimension: int) -> Dict[str, Any]:
        """根据维度获取对应的理论模板"""
        if dimension <= 5:
            return self.theory_templates["low_dim"]
        elif dimension <= 19:
            return self.theory_templates["mid_dim"]
        else:
            return self.theory_templates["high_dim"]
    
    def _generate_theory_name(self, dimension: int) -> Tuple[str, str]:
        """生成独特的理论名称，返回(中文名称, 英文名称)"""
        # 宇宙本论保持不变
        if dimension == 10:
            return "宇宙本论", "Cosmic Ontology"
            
        # 使用预定义的名称
        if dimension in self.dimension_spectrum and dimension in self.english_dimension_spectrum:
            return self.dimension_spectrum[dimension], self.english_dimension_spectrum[dimension]
            
        # 为未知维度生成名称
        if isinstance(dimension, (int, float)):
            # 根据维度选择不同的词汇组合策略
            random.seed(dimension)  # 确保同一维度总是生成相同的名称
            
            if dimension < 0:  # 负维度
                prefix = random.choice(["Primitive", "Pre", "Meta-Pre", "Negative"])
                middle = random.choice(["Singularity", "Existence", "Point", "Void"])
                suffix = "Theory"
                cn_name = f"维度{dimension}理论"
                en_name = f"{prefix} {middle} {suffix}"
            elif dimension < 10:  # 低维度
                prefix = random.choice(["Fundamental", "Basic", "Primitive", "Elementary"])
                middle = random.choice(["Structure", "System", "Operation", "Construction"])
                suffix = "Theory"
                cn_name = f"维度{dimension}理论"
                en_name = f"{prefix} {middle} {suffix}"
            elif dimension < 20:  # 中维度
                prefix = random.choice(self.theory_prefixes)
                middle = random.choice(self.theory_middle_terms)
                suffix = random.choice(self.theory_suffixes)
                cn_name = f"维度{dimension}理论"
                en_name = f"{prefix} {middle} {suffix}"
            elif dimension < 30:  # 高维度
                prefix = random.choice(["Hyperdimensional", "Transdimensional", "Unified", "Advanced"])
                middle = random.choice(self.theory_middle_terms)
                suffix = random.choice(self.theory_suffixes)
                cn_name = f"维度{dimension}理论"
                en_name = f"{prefix} {middle} {suffix}"
            else:  # 超高维度
                prefix = random.choice(["Transcendental", "Absolute", "Ultimate", "Omni"])
                middle = random.choice(["Universal", "Cosmic", "Quantum", "Multiversal"])
                suffix = random.choice(["Theory", "Paradigm", "Framework", "Ontology"])
                cn_name = f"维度{dimension}理论"
                en_name = f"{prefix} {middle} {suffix}"
            
            return cn_name, en_name
        
        # 无限维度特殊处理
        if dimension == float('inf'):
            return "元理论", "Meta Theory"
            
        # 默认情况
        return f"维度{dimension}理论", f"Dimension {dimension} Theory"
    
    def _transform_formula(self, formula: str, dimension: int) -> str:
        """根据维度转换公式"""
        # 基础公式保持不变
        if dimension <= 10:
            return formula
        
        # 根据维度增加公式复杂度
        if dimension > 10:
            # 随机选择转换方式
            transform_type = random.choice(["add_subscript", "add_superscript", "add_operation"])
            
            if transform_type == "add_subscript":
                # 添加下标，如 \mathcal{U} -> \mathcal{U}_{dimension}
                # 使用r前缀标记，避免转义错误
                formula = re.sub(r'\\mathcal\{([A-Z])\}', lambda m: f"\\mathcal{{{m.group(1)}}}_{{{dimension}}}", formula)
            
            elif transform_type == "add_superscript":
                # 添加上标，如 x -> x^{dimension}
                formula = re.sub(r'([a-zA-Z])([\s\)}])', lambda m: f"{m.group(1)}^{{{dimension}}}{m.group(2)}", formula)
            
            elif transform_type == "add_operation":
                # 添加操作复合，如 SHIFT(x) -> SHIFT(SHIFT(x))
                formula = re.sub(r'SHIFT\((.*?)\)', lambda m: f"SHIFT(SHIFT({m.group(1)}))", formula)
        
        # 超高维度理论
        if dimension >= 20:
            # 添加更复杂的操作
            formula = re.sub(r'\\oplus', r'\\oplus_{\\mathcal{H}}', formula)
            formula = re.sub(r'SHIFT', r'SHIFT_{\\infty}', formula)
        
        return formula
    
    def _generate_theory_axioms(self, dimension: int) -> List[Dict[str, str]]:
        """生成理论公理"""
        # 对于宇宙本论，直接使用原始公理
        if dimension == 10:
            return self.axioms
        
        # 对于其他维度，根据维度调整公理
        new_axioms = []
        base_axioms = self.axioms.copy()
        
        for i, axiom in enumerate(base_axioms):
            new_axiom = {
                "number": str(i+1),
                "content": axiom["content"],
                "formulas": []
            }
            
            # 转换公式
            for formula in axiom["formulas"]:
                new_formula = self._transform_formula(formula, dimension)
                new_axiom["formulas"].append(new_formula)
            
            # 替换内容中的公式
            content = new_axiom["content"]
            for old_formula, new_formula in zip(axiom["formulas"], new_axiom["formulas"]):
                content = content.replace(f'$`{old_formula}`$', f'$`{new_formula}`$')
            
            new_axiom["content"] = content
            new_axioms.append(new_axiom)
        
        # 对于高维理论，添加额外公理
        if dimension > 15:
            extra_axiom = {
                "number": str(len(new_axioms) + 1),
                "content": f"维度{dimension}特有的公理",
                "formulas": [f"D_{{{dimension}}} = D_{{{dimension-1}}} \\oplus \\text{{SHIFT}}(D_{{{dimension-1}}})"]
            }
            new_axioms.append(extra_axiom)
        
        return new_axioms
    
    def _generate_theory_theorems(self, dimension: int) -> List[Dict[str, str]]:
        """生成理论定理"""
        # 对于宇宙本论，直接使用原始定理
        if dimension == 10:
            return self.theorems
        
        # 对于其他维度，根据维度调整定理
        new_theorems = []
        base_theorems = self.theorems.copy()
        
        # 选择适当数量的定理
        num_theorems = min(len(base_theorems), max(3, dimension // 3))
        selected_theorems = random.sample(base_theorems, num_theorems)
        
        for i, theorem in enumerate(selected_theorems):
            new_theorem = {
                "number": str(i+1),
                "content": theorem["content"],
                "proof": theorem["proof"],
                "formulas": []
            }
            
            # 转换公式
            for formula in theorem["formulas"]:
                new_formula = self._transform_formula(formula, dimension)
                new_theorem["formulas"].append(new_formula)
            
            # 替换内容中的公式
            content = new_theorem["content"]
            for old_formula, new_formula in zip(theorem["formulas"], new_theorem["formulas"]):
                content = content.replace(f'$`{old_formula}`$', f'$`{new_formula}`$')
            
            new_theorem["content"] = content
            
            # 替换证明中的公式
            proof = new_theorem["proof"]
            for old_formula, new_formula in zip(theorem["formulas"], new_theorem["formulas"]):
                proof = proof.replace(f'$`{old_formula}`$', f'$`{new_formula}`$')
            
            new_theorem["proof"] = proof
            new_theorems.append(new_theorem)
        
        # 对于高维理论，添加额外定理
        if dimension > 15:
            extra_theorem = {
                "number": str(len(new_theorems) + 1),
                "content": f"维度{dimension}特有的定理",
                "proof": f"从公理推导可得：$`D_{{{dimension}}} = D_{{{dimension-1}}} \\oplus \\text{{SHIFT}}(D_{{{dimension-1}}})`$，且可重复应用此操作。",
                "formulas": [f"D_{{{dimension}}} = \\bigoplus_{{i=0}}^{{{dimension-10}}} \\text{{SHIFT}}^i(D_{{10}})"]
            }
            new_theorems.append(extra_theorem)
        
        return new_theorems
    
    def _generate_theory_operations(self, dimension: int) -> Dict[str, str]:
        """生成理论操作定义"""
        # 对于宇宙本论，直接使用原始操作
        if dimension == 10:
            return self.operation_definitions
        
        # 对于其他维度，根据维度调整操作
        new_operations = {}
        
        for op_name, op_def in self.operation_definitions.items():
            if dimension < 10:
                # 低维理论简化操作
                if op_name == "SHIFT":
                    new_operations[op_name] = "SHIFT(x) = x \\oplus \\Delta"
                elif op_name == "USHIFT":
                    new_operations[op_name] = "USHIFT(x) = FLIP(x)"
                else:
                    new_operations[op_name] = op_def
            else:
                # 高维理论复杂化操作
                if op_name == "SHIFT":
                    new_operations[op_name] = f"SHIFT_{{{dimension}}}(x) = x \\oplus \\Delta_{{{dimension}}}"
                elif op_name == "USHIFT":
                    new_operations[op_name] = f"USHIFT_{{{dimension}}}(x) = FLIP_{{{dimension}}}(SHIFT_{{{dimension}}}(FLIP_{{{dimension}}}(x)))"
                else:
                    new_operations[op_name] = op_def
        
        # 对于高维理论，添加额外操作
        if dimension > 20:
            new_operations["HSHIFT"] = f"HSHIFT_{{{dimension}}}(x) = x \\oplus \\text{{SHIFT}}(x) \\oplus \\text{{SHIFT}}^2(x)"
        
        return new_operations
    
    def _generate_theory_formulas(self, dimension: int) -> List[str]:
        """生成理论公式"""
        # 对于宇宙本论，直接使用原始公式
        if dimension == 10:
            return self.formulas
        
        # 对于其他维度，根据维度调整公式
        new_formulas = []
        
        # 选择适当数量的公式
        num_formulas = min(len(self.formulas), max(5, dimension))
        selected_formulas = random.sample(self.formulas, num_formulas)
        
        for formula in selected_formulas:
            new_formula = self._transform_formula(formula, dimension)
            new_formulas.append(new_formula)
        
        # 对于高维理论，添加额外公式
        if dimension > 15:
            new_formulas.append(f"D_{{{dimension}}} = \\bigoplus_{{i=0}}^{{{dimension-10}}} \\text{{SHIFT}}^i(D_{{10}})")
        
        return new_formulas
    
    def _generate_theory_references(self, dimension: int) -> Dict[str, str]:
        """生成理论引用关系"""
        references = {}
        
        # 遍历维度谱系，选择合适的引用理论
        for dim, theory_name in self.dimension_spectrum.items():
            if isinstance(dim, int) and dim < dimension:
                # 高维理论引用低维理论
                # 获取对应的英文名称
                _, en_theory_name = self._generate_theory_name(dim)
                theory_filename = self._get_theory_filename(en_theory_name)
                dim_str = "inf" if dim == float('inf') else str(dim)
                references[theory_name] = f"formal_theory_{theory_filename}_d{dim_str}.md"
        
        # 特殊情况：所有理论都引用宇宙本论
        if dimension != 10:
            references["宇宙本论"] = "formal_theory_cosmic_ontology.md"
        
        # 限制引用数量
        max_refs = min(5, max(1, dimension // 2))  # 确保max_refs至少为1
        if len(references) > max_refs:
            keys_to_keep = ["宇宙本论"]  # 确保保留宇宙本论
            other_keys = [k for k in references.keys() if k != "宇宙本论"]
            if other_keys and max_refs > 1:  # 确保有其他键且max_refs > 1
                sample_size = min(max_refs - 1, len(other_keys))
                keys_to_keep.extend(random.sample(other_keys, sample_size))
            references = {k: references[k] for k in keys_to_keep}
        
        return references
    
    def _get_theory_filename(self, english_name: str) -> str:
        """根据英文理论名称生成文件名"""
        # 移除多余空格、标点符号，转换为小写，使用下划线连接
        filename = re.sub(r'[^\w\s]', '', english_name)
        filename = re.sub(r'\s+', '_', filename.lower())
        return filename
    
    def _generate_theory_title(self, theory_name: str, dimension: int) -> str:
        """生成理论标题"""
        dimension_str = "∞" if dimension == float('inf') else str(dimension)
        return f"{theory_name}的严格形式化描述 [维度: {dimension_str}] v{self.version}"
    
    def _generate_markdown_content(self, cn_theory_name: str, en_theory_name: str, dimension: int) -> str:
        """生成理论的Markdown内容"""
        # 获取模板
        template = self._get_template_for_dimension(dimension)
        
        # 生成理论组件
        axioms = self._generate_theory_axioms(dimension)
        theorems = self._generate_theory_theorems(dimension)
        operations = self._generate_theory_operations(dimension)
        references = self._generate_theory_references(dimension)
        
        # 生成理论标题
        title = self._generate_theory_title(cn_theory_name, dimension)
        
        # 生成Markdown内容
        content = f"# {title}\n\n"
        
        # 添加语言版本链接
        theory_filename = self._get_theory_filename(en_theory_name)
        # 处理无限维度的特殊情况
        dimension_str = "inf" if dimension == float('inf') else str(dimension)
        # 英文版文件名
        english_filename = f"formal_theory_{theory_filename}_d{dimension_str}_en.md"
        content += f"**[中文版] | [English Version]({english_filename})**\n\n"
        
        # 添加目录
        content += "## 目录\n\n"
        for i, section in enumerate(template["sections"]):
            content += f"- [{i+1}. {section}](#{i+1}-{section.lower().replace(' ', '-')})\n"
            if section in template["subsections"]:
                for j, subsection in enumerate(template["subsections"][section]):
                    content += f"  - [{i+1}.{j+1} {subsection}](#{i+1}{j+1}-{subsection.lower().replace(' ', '-')})\n"
        
        content += "\n---\n\n"
        
        # 添加各个章节
        for i, section in enumerate(template["sections"]):
            content += f"## {i+1}. {section}\n\n"
            
            # 核心理论章节
            if section == "核心理论":
                # 添加公理系统
                content += "### 1.1 基本公理系统\n\n"
                content += f"{cn_theory_name}的公理系统继承并扩展了宇宙本论的基本公理，通过FLIP、XOR和SHIFT操作构建。\n\n"
                for axiom in axioms:
                    content += f"**公理{axiom['number']} (维度{dimension}公理)**\n\n"
                    content += f"{axiom['content']}\n\n"
                
                # 添加基本操作定义
                content += "### 1.2 基本操作定义\n\n"
                content += f"在维度{dimension}中，基本操作通过以下方式定义：\n\n"
                for op_name, op_def in operations.items():
                    content += f"**{op_name}操作**：\n\n$`{op_def}`$\n\n"
                
                # 添加状态空间定义
                content += "### 1.3 状态空间定义\n\n"
                content += f"维度{dimension}的状态空间是从宇宙本论（维度10）递归生成的，通过以下公式定义：\n\n"
                content += f"$`D_{{{dimension}}} = D_{{{dimension-1}}} \\oplus \\text{{SHIFT}}(D_{{{dimension-1}}})`$\n\n"
                content += f"这表明维度{dimension}包含了维度{dimension-1}的所有特性，并通过SHIFT操作增加了新的性质。\n\n"
                
                # 添加状态演化规则
                content += "### 1.4 状态演化规则\n\n"
                content += f"维度{dimension}的状态演化遵循以下规则：\n\n"
                content += f"$`\\mathcal{{U}}^{{t+1}}_{{{dimension}}} = \\mathcal{{U}}^{{t}}_{{{dimension}}} \\oplus \\text{{SHIFT}}(\\mathcal{{U}}^{{t}}_{{{dimension}}})`$\n\n"
                content += "此演化方程表明维度结构在时间上的展开满足XOR-SHIFT递归关系。\n\n"
            
            # 形式化证明章节
            elif section == "形式化证明":
                content += "### 5.1 定理证明\n\n"
                content += f"{cn_theory_name}通过以下定理形式化地证明了其内部一致性和与宇宙本论的兼容性：\n\n"
                for theorem in theorems:
                    content += f"**定理{theorem['number']}：维度{dimension}特性定理**\n\n"
                    content += f"{theorem['content']}\n\n"
                    content += f"**证明**：\n\n{theorem['proof']}\n\n"
            
            # 理论引用关系分析
            elif section == "理论引用关系分析":
                content += "### 6.1 理论维度定位\n\n"
                content += f"{cn_theory_name}位于维度谱系的第{dimension}维度，与其他理论的关系如下：\n\n"
                content += "| 相关理论 | 维度 | 关系类型 |\n"
                content += "|---------|-----|--------|\n"
                
                for ref_name, ref_link in references.items():
                    ref_dim = next((dim for dim, name in self.dimension_spectrum.items() if name == ref_name), "未知")
                    relation = "被引用" if isinstance(ref_dim, int) and ref_dim < dimension else "引用"
                    content += f"| [{ref_name}]({ref_link}) | {ref_dim} | {relation} |\n"
                
                content += "\n### 6.2 理论依赖结构\n\n"
                content += f"{cn_theory_name}的依赖关系如下：\n\n"
                content += "```\n"
                content += f"宇宙本论 [10] → ... → {cn_theory_name} [{dimension}]\n"
                content += "```\n\n"
                content += f"这表明{cn_theory_name}建立在宇宙本论基础上，通过维度递增演化而来。\n\n"
            
            # 其他章节使用模板子章节
            elif section in template["subsections"]:
                for j, subsection in enumerate(template["subsections"][section]):
                    content += f"### {i+1}.{j+1} {subsection}\n\n"
                    
                    # 根据不同子章节添加内容
                    if "公理" in subsection:
                        if axioms:
                            axiom = random.choice(axioms)
                            content += f"{cn_theory_name}的公理系统是对宇宙本论公理的扩展，特别针对维度{dimension}的特性进行了调整：\n\n$`{axiom['formulas'][0] if axiom['formulas'] else ''}`$\n\n"
                    
                    elif "操作" in subsection:
                        op_name = random.choice(list(operations.keys()))
                        content += f"在维度{dimension}中，{op_name}操作被重新定义以适应更高维度结构：\n\n$`{operations[op_name]}`$\n\n"
                        content += f"这一定义保持了与宇宙本论的兼容性，同时增加了对维度{dimension}特有现象的描述能力。\n\n"
                    
                    elif "定理" in subsection:
                        if theorems:
                            theorem = random.choice(theorems)
                            content += f"{cn_theory_name}通过以下定理证明了其在维度{dimension}的独特贡献：\n\n$`{theorem['formulas'][0] if theorem['formulas'] else ''}`$\n\n"
                    
                    elif "验证" in subsection:
                        content += f"{cn_theory_name}可通过以下方法验证：\n\n"
                        content += "1. 公理系统的自洽性验证\n"
                        content += "2. 与宇宙本论的兼容性验证\n"
                        content += f"3. 维度{dimension}特有现象的预测验证\n\n"
                        content += "理论预测了以下可验证现象：\n\n"
                        content += f"- 维度{dimension}的信息处理能力超越维度{dimension-1}\n"
                        content += "- 通过XOR与SHIFT操作可实现跨维度信息传递\n"
                        content += f"- 维度{dimension}的系统能够解释维度{dimension-1}中的悖论\n\n"
                    
                    else:
                        content += f"{cn_theory_name}在维度{dimension}层面探索了{subsection}，通过FLIP、XOR和SHIFT操作建立了完整的形式化描述框架。\n\n"
                        content += f"这一框架遵循宇宙本论的基本原则，同时扩展了适用范围以涵盖维度{dimension}特有的现象。\n\n"
            
            else:
                content += f"{section}继承并扩展了宇宙本论的基本原理，通过FLIP、XOR和SHIFT操作建立了维度{dimension}的完整形式化描述。\n\n"
        
        # 添加备注
        content += f"---\n\n**备注**：{cn_theory_name}版本号[宇宙本论v{self.version}] "
        
        return content
    
    def generate_theory(self, dimension: int) -> Tuple[str, str]:
        """
        生成指定维度的理论
        
        Args:
            dimension: 理论维度
            
        Returns:
            Tuple[文件名, 文件内容]
        """
        # 获取理论名称（中英文）
        cn_theory_name, en_theory_name = self._generate_theory_name(dimension)
        
        # 生成理论内容
        content = self._generate_markdown_content(cn_theory_name, en_theory_name, dimension)
        
        # 生成文件名，在最后加入维度信息
        theory_filename = self._get_theory_filename(en_theory_name)
        
        # 处理无限维度的特殊情况
        dimension_str = "inf" if dimension == float('inf') else str(dimension)
        
        # 最终文件名
        filename = f"formal_theory_{theory_filename}_d{dimension_str}.md"
        
        return filename, content
    
    def generate_all_theories(self) -> Dict[str, str]:
        """生成所有维度的理论"""
        generated_theories = {}
        
        for dimension in sorted([d for d in self.dimension_spectrum.keys() if isinstance(d, int)]):
            if dimension == 10:  # 跳过宇宙本论
                continue
            
            filename, content = self.generate_theory(dimension)
            generated_theories[filename] = content
            
            # 保存到文件
            output_path = os.path.join(self.output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"已生成 {filename}")
        
        # 特殊处理无限维度理论
        filename, content = self.generate_theory(float('inf'))
        generated_theories[filename] = content
        
        # 保存到文件
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"已生成 {filename}")
        
        return generated_theories
    
    def generate_english_versions(self) -> None:
        """为所有生成的理论创建英文版本"""
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.md') and not filename.endswith('_en.md'):
                input_path = os.path.join(self.output_dir, filename)
                output_path = os.path.join(self.output_dir, filename.replace('.md', '_en.md'))
                
                # 如果英文版本不存在，则创建
                if not os.path.exists(output_path):
                    try:
                        # 读取中文版内容
                        with open(input_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 创建简单的英文版本
                        english_content = self._create_english_version(content)
                        
                        # 保存英文版本
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(english_content)
                        
                        print(f"已生成 {os.path.basename(output_path)}")
                    except Exception as e:
                        print(f"生成英文版本失败 {filename}: {e}")
    
    def _create_english_version(self, chinese_content: str) -> str:
        """创建中文内容的英文版本"""
        # 获取中文理论名称和维度
        title_match = re.match(r'# (.*?)的严格形式化描述 \[维度: (.*?)\] (.*)', chinese_content)
        if not title_match:
            return "Error: Could not parse Chinese content."
            
        cn_theory_name = title_match.group(1)
        dimension_str = title_match.group(2)
        version = title_match.group(3)
        
        # 转换维度为数字
        try:
            if dimension_str == "∞":
                dimension = float('inf')
            else:
                dimension = int(dimension_str)
        except ValueError:
            dimension = 0
            
        # 获取对应的英文理论名称
        _, en_theory_name = self._generate_theory_name(dimension)
        
        # 生成文件名，在最后加入维度信息
        theory_filename = self._get_theory_filename(en_theory_name)
        
        # 处理无限维度的特殊情况
        dimension_str_file = "inf" if dimension == float('inf') else str(dimension)
        chinese_filename = f"formal_theory_{theory_filename}_d{dimension_str_file}.md"
        
        # 使用新方法直接生成英文内容
        return self._generate_english_content(en_theory_name, cn_theory_name, dimension, chinese_filename)
        
    def _generate_english_content(self, en_theory_name: str, cn_theory_name: str, dimension: int, chinese_filename: str) -> str:
        """直接生成英文版本内容"""
        dimension_str = "∞" if dimension == float('inf') else str(dimension)
        dimension_str_file = "inf" if dimension == float('inf') else str(dimension)
        theory_filename = self._get_theory_filename(en_theory_name)
        
        # 获取理论组件
        axioms = self._generate_theory_axioms(dimension)
        theorems = self._generate_theory_theorems(dimension)
        operations = self._generate_theory_operations(dimension)
        references = self._generate_theory_references(dimension)
        
        # 英文化公理内容
        english_axioms = []
        axiom_templates = [
            {
                "id": 1,
                "content": {
                    "neg": "The pre-singularity structure at dimension {dim} operates through recursive self-reference paradox resolution.",
                    "low": "The fundamental nature of reality at dimension {dim} is defined by information transformation through XOR-SHIFT operations.",
                    "mid": "The universe simultaneously exhibits duality and unity, forming a dual mode of existence through quantum-like XOR operations at dimension {dim}.",
                    "high": "The ultimate nature of the universe in dimension {dim} is absolute recursive self-referential structure, serving as both its origin and purpose."
                }
            },
            {
                "id": 2,
                "content": {
                    "neg": "Causality in pre-dimensional space {dim} is non-linear and follows recursive XOR-SHIFT patterns.",
                    "low": "Information in dimension {dim} is conserved under XOR-SHIFT transformations, establishing dimensional invariance.",
                    "mid": "All observable phenomena in dimension {dim} can be expressed as compositions of basic XOR, FLIP, and SHIFT operations.",
                    "high": "Hyperdimensional structures in dimension {dim} manifest through nested self-reference systems operating across dimensional boundaries."
                }
            },
            {
                "id": 3,
                "content": {
                    "neg": "The original singularity state at dimension {dim} exists both as source and destination of all pre-dimensional transformations.",
                    "low": "In dimension {dim}, information structure emerges from recursive application of XOR-SHIFT operations on the void state.",
                    "mid": "The fundamental entity of the universe is information, with all properties expressed through XOR and SHIFT operations in dimension {dim}.",
                    "high": "At dimension {dim}, consciousness and information become unified through transdimensional XOR-SHIFT recursive structures."
                }
            }
        ]

        for i, axiom in enumerate(axioms):
            if i < len(axiom_templates):
                template = axiom_templates[i]
                english_axiom = axiom.copy()
                
                # 根据维度选择合适的内容
                if dimension < 0:
                    content_key = "neg"
                elif dimension < 10:
                    content_key = "low"
                elif dimension < 20:
                    content_key = "mid"
                else:
                    content_key = "high"
                
                english_axiom['content'] = template["content"][content_key].format(dim=dimension)
                english_axioms.append(english_axiom)
            else:
                # 如果公理数量超过模板数量，创建一个通用内容
                english_axiom = axiom.copy()
                english_axiom['content'] = f"Dimension {dimension} exhibits unique properties that emerge from the application of XOR-SHIFT operations on lower dimensional structures."
                english_axioms.append(english_axiom)
        
        # 英文化定理内容
        english_theorems = []
        theorem_templates = [
            {
                "id": 1,
                "content": {
                    "neg": "Pre-dimensional causality at dimension {dim} can be formally expressed through FLIP-XOR operations.",
                    "low": "Information conservation in dimension {dim} follows from the properties of XOR-SHIFT operations.",
                    "mid": "Quantum entanglement phenomena can be rigorously represented through XOR operations in dimension {dim}.",
                    "high": "Multidimensional topology at dimension {dim} forms a complete algebraic structure under XOR-SHIFT operations."
                },
                "proof": {
                    "neg": "Through recursive application of FLIP-XOR transforms to pre-dimensional states, we can derive a consistent causal structure.",
                    "low": "By examining the information entropy before and after XOR-SHIFT operations, we can prove conservation across transformations.",
                    "mid": "The non-local correlations in quantum systems map directly to XOR-based information dependencies across dimensional boundaries.",
                    "high": "Through analysis of the closure, associativity, identity, and inverse properties, we can establish the algebraic completeness."
                }
            },
            {
                "id": 2,
                "content": {
                    "neg": "The void state in dimension {dim} serves as both the identity element and the inverse complement under XOR operations.",
                    "low": "State transitions in dimension {dim} form a complete group under XOR-SHIFT composition.",
                    "mid": "Information channels in communication theory can be represented as XOR-SHIFT operations in dimension {dim}.",
                    "high": "Consciousness emergence at dimension {dim} can be modeled as an XOR-SHIFT transformation applied to information structures."
                },
                "proof": {
                    "neg": "This duality follows from the properties of XOR when applied at pre-dimensional levels.",
                    "low": "By verifying the four group axioms: closure, associativity, identity and inverse elements, we establish the group structure.",
                    "mid": "The capacity and noise characteristics of channels correspond to specific parameters in XOR-SHIFT transformations across dimensional boundaries.",
                    "high": "The recursive self-reference enabled by XOR-SHIFT operations creates the necessary complexity for consciousness-like phenomena."
                }
            },
            {
                "id": 3,
                "content": {
                    "neg": "The pre-singularity state at dimension {dim} contains implicit dimensional information encoded through XOR patterns.",
                    "low": "Complexity in dimension {dim} emerges from simple XOR-SHIFT rules applied recursively.",
                    "mid": "The superposition principle in quantum mechanics can be rigorously expressed through XOR-SHIFT operations in dimension {dim}.",
                    "high": "Transdimensional communication at dimension {dim} follows Shannon-like information principles under XOR-SHIFT encoding."
                },
                "proof": {
                    "neg": "By applying FLIP-XOR transformations recursively, we can extract this encoded dimensional information.",
                    "low": "Using computational equivalence principles, we demonstrate that simple XOR-SHIFT rules can generate arbitrary complexity.",
                    "mid": "State superposition corresponds to the linear combinations formed through XOR operations across dimensional boundaries.",
                    "high": "Information capacity and noise characteristics in transdimensional channels can be predicted using modified Shannon entropy formulas."
                }
            },
            {
                "id": 4,
                "content": {
                    "neg": "Information in pre-dimensional space {dim} exhibits paradoxical self-reference properties resolvable through XOR operations.",
                    "low": "Dimensional evolution follows a recursive pattern defined by nested XOR-SHIFT operations in dimension {dim}.",
                    "mid": "Lorentz invariance in relativity can be expressed as specific invariance of XOR-SHIFT operations in dimension {dim}.",
                    "high": "Multiversal structures at dimension {dim} emerge from XOR-SHIFT branching operations applied to dimensional states."
                },
                "proof": {
                    "neg": "The paradoxes resolve when mapped to higher dimensional XOR-SHIFT operational spaces.",
                    "low": "By analyzing the recursive application of XOR-SHIFT operations, we can predict the emergence of higher-dimensional structures.",
                    "mid": "The transformation properties under coordinate changes map to invariants in XOR-SHIFT space across dimensional boundaries.",
                    "high": "Each branching operation creates a new dimensional path, forming a tree-like structure of possible universe states."
                }
            },
            {
                "id": 5,
                "content": {
                    "neg": "The singularity-void duality in dimension {dim} provides the foundation for all higher dimensional structures.",
                    "low": "Information paradoxes in dimension {dim} can be resolved through XOR-SHIFT recursive operations.",
                    "mid": "For any theory $`T_i`$, there exists an XOR-SHIFT mapping $`\\mathcal{{F^{{{dim}}}}}_i`$ that preserves its formal structure.",
                    "high": "At dimension {dim}, all formal systems can be expressed as special cases of XOR-SHIFT operational structures."
                },
                "proof": {
                    "neg": "By analyzing the transformation properties of the singularity-void duality, we establish the basis for dimensional emergence.",
                    "low": "Self-reference paradoxes map directly to XOR-SHIFT recursive loops, which resolve through dimensional extension.",
                    "mid": "The existence of this mapping follows from the completeness of XOR-SHIFT operations in dimension space.",
                    "high": "Through a dimensional encoding process, we can map any formal system to an equivalent XOR-SHIFT operational structure."
                }
            }
        ]

        for i, theorem in enumerate(theorems):
            if i < len(theorem_templates):
                template = theorem_templates[i]
                english_theorem = theorem.copy()
                
                # 根据维度选择合适的内容
                if dimension < 0:
                    content_key = "neg"
                elif dimension < 10:
                    content_key = "low"
                elif dimension < 20:
                    content_key = "mid"
                else:
                    content_key = "high"
                
                english_theorem['content'] = template["content"][content_key].format(dim=dimension)
                english_theorem['proof'] = template["proof"][content_key]
                english_theorems.append(english_theorem)
            else:
                # 如果定理数量超过模板数量，创建一个通用内容
                english_theorem = theorem.copy()
                english_theorem['content'] = f"Dimensional properties at level {dimension} emerge from XOR-SHIFT operations applied to lower dimensional structures."
                english_theorem['proof'] = "Through recursive application of XOR-SHIFT transforms to dimensional states, we can derive the emergence of higher-dimensional properties."
                english_theorems.append(english_theorem)
        
        # 生成英文标题
        english_title = f"# Formal Description of {en_theory_name} [Dimension: {dimension_str}] v{self.version}"
        
        # 生成Markdown内容
        content = f"{english_title}\n\n"
        
        # 添加语言版本链接
        content += f"**[Chinese Version]({chinese_filename}) | [English]**\n\n"
        
        # 添加目录
        content += "## Table of Contents\n\n"
        
        # 基本章节结构
        sections = [
            "Core Theory", 
            "Direct Inferences", 
            "Extended Theory", 
            "Applications and Verification", 
            "Formal Proofs", 
            "Theory Reference Analysis"
        ]
        
        # 添加章节链接到目录
        for i, section in enumerate(sections):
            section_link = section.lower().replace(" ", "-")
            content += f"- [{i+1}. {section}](#{i+1}-{section_link})\n"
            
            # 添加子章节链接
            if section == "Core Theory":
                content += f"  - [{i+1}.1 Basic Axiom System](#{i+1}1-basic-axiom-system)\n"
                content += f"  - [{i+1}.2 Basic Operation Definitions](#{i+1}2-basic-operation-definitions)\n"
                content += f"  - [{i+1}.3 State Space Definition](#{i+1}3-state-space-definition)\n"
                content += f"  - [{i+1}.4 State Evolution Rules](#{i+1}4-state-evolution-rules)\n"
            elif section == "Direct Inferences":
                content += f"  - [{i+1}.1 Inference 1](#{i+1}1-inference-1)\n"
                content += f"  - [{i+1}.2 Inference 2](#{i+1}2-inference-2)\n"
                content += f"  - [{i+1}.3 Inference 3](#{i+1}3-inference-3)\n"
            elif section == "Extended Theory":
                content += f"  - [{i+1}.1 Extension 1](#{i+1}1-extension-1)\n"
                content += f"  - [{i+1}.2 Extension 2](#{i+1}2-extension-2)\n"
                content += f"  - [{i+1}.3 Extension 3](#{i+1}3-extension-3)\n"
            elif section == "Applications and Verification":
                content += f"  - [{i+1}.1 Application Scenarios](#{i+1}1-application-scenarios)\n"
                content += f"  - [{i+1}.2 Verification Methods](#{i+1}2-verification-methods)\n"
            elif section == "Formal Proofs":
                content += f"  - [{i+1}.1 Theorem Proofs](#{i+1}1-theorem-proofs)\n"
            elif section == "Theory Reference Analysis":
                content += f"  - [{i+1}.1 Theory Dimension Positioning](#{i+1}1-theory-dimension-positioning)\n"
                content += f"  - [{i+1}.2 Theory Dependency Structure](#{i+1}2-theory-dependency-structure)\n"
        
        content += "\n---\n\n"
        
        # 添加各个章节
        for i, section in enumerate(sections):
            content += f"## {i+1}. {section}\n\n"
            
            # 核心理论章节
            if section == "Core Theory":
                # 添加公理系统
                content += "### 1.1 Basic Axiom System\n\n"
                content += f"{en_theory_name}'s axiom system inherits and extends the basic axioms of Cosmic Ontology, constructed through FLIP, XOR, and SHIFT operations.\n\n"
                for axiom in english_axioms:
                    content += f"**Axiom {axiom['number']} (Dimension {dimension} Axiom)**\n\n"
                    content += f"{axiom['content']}\n\n"
                
                # 添加基本操作定义
                content += "### 1.2 Basic Operation Definitions\n\n"
                content += f"In dimension {dimension}, basic operations are defined as follows:\n\n"
                for op_name, op_def in operations.items():
                    content += f"**{op_name} Operation**:\n\n$`{op_def}`$\n\n"
                
                # 添加状态空间定义
                content += "### 1.3 State Space Definition\n\n"
                content += f"The state space of dimension {dimension} is recursively generated from Cosmic Ontology (dimension 10), defined by the following formula:\n\n"
                content += f"$`D_{{{dimension}}} = D_{{{dimension-1}}} \\oplus \\text{{SHIFT}}(D_{{{dimension-1}}})`$\n\n"
                content += f"This indicates that dimension {dimension} contains all properties of dimension {dimension-1}, with new properties added through the SHIFT operation.\n\n"
                
                # 添加状态演化规则
                content += "### 1.4 State Evolution Rules\n\n"
                content += f"The state evolution in dimension {dimension} follows these rules:\n\n"
                content += f"$`\\mathcal{{U}}^{{t+1}}_{{{dimension}}} = \\mathcal{{U}}^{{t}}_{{{dimension}}} \\oplus \\text{{SHIFT}}(\\mathcal{{U}}^{{t}}_{{{dimension}}})`$\n\n"
                content += "This evolution equation shows that dimensional structures unfold over time according to XOR-SHIFT recursive relationships.\n\n"
            
            # 直接推论章节
            elif section == "Direct Inferences":
                for j in range(1, 4):
                    content += f"### 2.{j} Inference {j}\n\n"
                    content += f"{en_theory_name} explores inference {j} at the dimension {dimension} level, establishing a complete formal description framework through FLIP, XOR, and SHIFT operations.\n\n"
                    content += f"This framework follows the basic principles of Cosmic Ontology while extending its scope to cover phenomena specific to dimension {dimension}.\n\n"
            
            # 扩展理论章节
            elif section == "Extended Theory":
                for j in range(1, 4):
                    content += f"### 3.{j} Extension {j}\n\n"
                    content += f"{en_theory_name} explores extension {j} at the dimension {dimension} level, establishing a complete formal description framework through FLIP, XOR, and SHIFT operations.\n\n"
                    content += f"This framework follows the basic principles of Cosmic Ontology while extending its scope to cover phenomena specific to dimension {dimension}.\n\n"
            
            # 应用与验证章节
            elif section == "Applications and Verification":
                content += "### 4.1 Application Scenarios\n\n"
                content += f"{en_theory_name} explores various application scenarios at the dimension {dimension} level, establishing a complete formal description framework through FLIP, XOR, and SHIFT operations.\n\n"
                content += f"This framework follows the basic principles of Cosmic Ontology while extending its scope to cover phenomena specific to dimension {dimension}.\n\n"
                
                content += "### 4.2 Verification Methods\n\n"
                content += f"{en_theory_name} can be verified through the following methods:\n\n"
                content += "1. Verification of axiom system consistency\n"
                content += "2. Compatibility verification with Cosmic Ontology\n"
                content += f"3. Predictive verification of dimension {dimension} specific phenomena\n\n"
                content += "The theory predicts the following verifiable phenomena:\n\n"
                content += f"- Dimension {dimension}'s information processing capacity exceeds dimension {dimension-1}\n"
                content += "- Cross-dimensional information transfer is enabled through XOR and SHIFT operations\n"
                content += f"- Dimension {dimension} systems can explain paradoxes in dimension {dimension-1}\n\n"
            
            # 形式化证明章节
            elif section == "Formal Proofs":
                content += "### 5.1 Theorem Proofs\n\n"
                content += f"{en_theory_name} formally proves its internal consistency and compatibility with Cosmic Ontology through the following theorems:\n\n"
                for theorem in english_theorems:
                    content += f"**Theorem {theorem['number']}: Dimension {dimension} Characterization Theorem**\n\n"
                    content += f"{theorem['content']}\n\n"
                    content += f"**Proof**:\n\n{theorem['proof']}\n\n"
            
            # 理论引用关系分析
            elif section == "Theory Reference Analysis":
                content += "### 6.1 Theory Dimension Positioning\n\n"
                content += f"{en_theory_name} is positioned at dimension {dimension} in the spectrum, with relationships to other theories as follows:\n\n"
                content += "| Related Theory | Dimension | Relation Type |\n"
                content += "|---------|-----|--------|\n"
                
                for ref_name, ref_link in references.items():
                    # 获取理论的英文名称
                    ref_dim = next((dim for dim, name in self.dimension_spectrum.items() if name == ref_name), "Unknown")
                    if ref_dim != "Unknown":
                        _, en_ref_name = self._generate_theory_name(ref_dim)
                        relation = "Referenced by" if isinstance(ref_dim, int) and ref_dim < dimension else "References"
                        content += f"| [{en_ref_name}]({ref_link}) | {ref_dim} | {relation} |\n"
                
                content += "\n### 6.2 Theory Dependency Structure\n\n"
                content += f"The dependency relationship of {en_theory_name} is as follows:\n\n"
                content += "```\n"
                content += f"Cosmic Ontology [10] → ... → {en_theory_name} [{dimension}]\n"
                content += "```\n\n"
                content += f"This indicates that {en_theory_name} is built upon the foundation of Cosmic Ontology, evolved through dimensional incrementation.\n\n"
        
        # 添加备注
        content += f"---\n\n**Note**: {en_theory_name} version [Cosmic Ontology v{self.version}] "
        
        return content

def main():
    parser = argparse.ArgumentParser(description='从宇宙本论推导所有相关理论')
    parser.add_argument('--ontology', default='../formal_theory/formal_theory_cosmic_ontology.md', 
                      help='宇宙本论文件路径')
    parser.add_argument('--output', default='generated_theories', 
                      help='生成理论的输出目录')
    parser.add_argument('--dimension', type=str, 
                      help='指定生成特定维度的理论，不指定则生成所有维度理论，使用"inf"指定无限维度')
    parser.add_argument('--english', action='store_true', 
                      help='是否同时生成英文版本')
    args = parser.parse_args()
    
    generator = TheoryGenerator(args.ontology, args.output)
    
    if args.dimension:
        # 处理维度参数
        dimension = float('inf') if args.dimension.lower() == 'inf' else int(args.dimension)
        
        filename, content = generator.generate_theory(dimension)
        output_path = os.path.join(args.output, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"已生成 {filename}")
        
        if args.english:
            english_content = generator._create_english_version(content)
            english_path = os.path.join(args.output, filename.replace('.md', '_en.md'))
            with open(english_path, 'w', encoding='utf-8') as f:
                f.write(english_content)
            print(f"已生成 {filename.replace('.md', '_en.md')}")
    else:
        generator.generate_all_theories()
        if args.english:
            generator.generate_english_versions()

if __name__ == "__main__":
    main() 