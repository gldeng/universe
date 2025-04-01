#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import glob
import argparse
from typing import Dict, List, Any, Optional, Tuple

class TheoryParser:
    """解析形式化理论文档并生成JSON输出的类"""
    
    def __init__(self, base_dir: str = "formal_theory"):
        """
        初始化解析器
        
        Args:
            base_dir: 形式化理论文档的基本目录
        """
        self.base_dir = base_dir
        # 版本模式，匹配如 v36.0
        self.version_pattern = re.compile(r'v(\d+\.\d+)')
        # 维度模式，匹配如 [维度: ∞] 或 [维度: 10]
        self.dimension_pattern = re.compile(r'\[维度[:：]\s*([^\]]+)\]')
        # 章节标题模式
        self.section_pattern = re.compile(r'^##\s+(.*?)$', re.MULTILINE)
        # 子章节标题模式
        self.subsection_pattern = re.compile(r'^###\s+(.*?)$', re.MULTILINE)
        # 公式模式，匹配 $`...`$ 或 $$...$$
        self.formula_pattern = re.compile(r'\$`(.*?)`\$|\$\$(.*?)\$\$', re.DOTALL)
        # 定理模式
        self.theorem_pattern = re.compile(r'\*\*定理\d+[^*]*\*\*\s*(.*?)(?=\*证明\*|\n##|\Z)', re.DOTALL)
        # 证明模式
        self.proof_pattern = re.compile(r'\*证明\*:\s*(.*?)(?=Q\.E\.D\.|证毕|证明完成|\n##|\Z)', re.DOTALL)
        # 引用关系模式
        self.reference_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        # 引用维度模式
        self.ref_dimension_pattern = re.compile(r'\[(\d+|\-\d+|∞)\]')
    
    def get_all_theory_files(self) -> List[str]:
        """获取所有理论文件的路径"""
        pattern = os.path.join(self.base_dir, "formal_theory_*.md")
        return [f for f in glob.glob(pattern) if not f.endswith("_en.md")]
    
    def extract_title_and_metadata(self, content: str) -> Tuple[str, Dict[str, Any]]:
        """提取文档的标题和元数据"""
        # 提取第一行作为标题
        title_match = re.match(r'^#\s+(.*?)$', content.split('\n')[0])
        title = title_match.group(1) if title_match else "未知标题"
        
        # 提取版本
        version_match = self.version_pattern.search(title)
        version = version_match.group(1) if version_match else "未知版本"
        
        # 提取维度
        dimension_match = self.dimension_pattern.search(title)
        dimension = dimension_match.group(1) if dimension_match else "未知维度"
        
        metadata = {
            "version": version,
            "dimension": dimension,
            "title": title
        }
        
        return title, metadata
    
    def extract_sections(self, content: str) -> Dict[str, Any]:
        """提取文档中的章节内容"""
        sections = {}
        section_matches = self.section_pattern.finditer(content)
        
        prev_match_end = 0
        prev_section_name = None
        
        for match in section_matches:
            section_name = match.group(1)
            start_pos = match.end()
            
            # 存储前一个章节的内容
            if prev_section_name:
                section_content = content[prev_match_end:match.start()].strip()
                sections[prev_section_name] = self.parse_section_content(section_content)
            
            prev_match_end = start_pos
            prev_section_name = section_name
        
        # 存储最后一个章节的内容
        if prev_section_name:
            section_content = content[prev_match_end:].strip()
            sections[prev_section_name] = self.parse_section_content(section_content)
        
        return sections
    
    def parse_section_content(self, content: str) -> Dict[str, Any]:
        """解析章节内容，提取子章节、公式、定理等"""
        result = {
            "content": content,
            "subsections": {},
            "formulas": self.extract_formulas(content),
            "theorems": self.extract_theorems(content),
            "proofs": self.extract_proofs(content)
        }
        
        # 提取子章节
        subsection_matches = self.subsection_pattern.finditer(content)
        for match in subsection_matches:
            subsection_name = match.group(1)
            start_pos = match.end()
            end_pos = len(content)
            
            # 寻找下一个子章节的开始位置
            next_match = self.subsection_pattern.search(content, start_pos)
            if next_match:
                end_pos = next_match.start()
            
            subsection_content = content[start_pos:end_pos].strip()
            result["subsections"][subsection_name] = {
                "content": subsection_content,
                "formulas": self.extract_formulas(subsection_content),
                "theorems": self.extract_theorems(subsection_content),
                "proofs": self.extract_proofs(subsection_content)
            }
        
        return result
    
    def extract_formulas(self, content: str) -> List[str]:
        """提取内容中的数学公式"""
        formulas = []
        for match in self.formula_pattern.finditer(content):
            formula = match.group(1) or match.group(2)
            if formula:
                formulas.append(formula.strip())
        return formulas
    
    def extract_theorems(self, content: str) -> List[str]:
        """提取内容中的定理"""
        theorems = []
        for match in self.theorem_pattern.finditer(content):
            theorem = match.group(1)
            if theorem:
                theorems.append(theorem.strip())
        return theorems
    
    def extract_proofs(self, content: str) -> List[str]:
        """提取内容中的证明"""
        proofs = []
        for match in self.proof_pattern.finditer(content):
            proof = match.group(1)
            if proof:
                proofs.append(proof.strip())
        return proofs
    
    def extract_references(self, content: str) -> Dict[str, str]:
        """提取文档中的引用关系"""
        references = {}
        for match in self.reference_pattern.finditer(content):
            ref_name = match.group(1)
            ref_link = match.group(2)
            if ref_link.startswith("formal_theory_"):
                references[ref_name] = ref_link
        return references
    
    def extract_reference_dimensions(self, content: str) -> Dict[str, str]:
        """提取引用的理论维度"""
        ref_dimensions = {}
        # 查找类似 "宇宙本论 [10]" 的模式
        for section in ["理论维度定位", "理论依赖结构"]:
            # 修复转义序列
            section_pattern = re.compile(r'#{1,6}\s+[^#]*' + re.escape(section) + r'[^#]*$(.*?)(?=#{1,6}\s+|$)', re.MULTILINE | re.DOTALL)
            section_match = section_pattern.search(content)
            
            if section_match:
                section_content = section_match.group(1)
                ref_matches = re.finditer(r'([^\[\]]+)\s+\[(\d+|\-\d+|∞)\]', section_content)
                for match in ref_matches:
                    theory_name = match.group(1).strip()
                    dimension = match.group(2)
                    ref_dimensions[theory_name] = dimension
        
        return ref_dimensions
    
    def parse_theory_file(self, file_path: str) -> Dict[str, Any]:
        """解析单个理论文件并返回结构化数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取文件名（不含路径和扩展名）
            filename = os.path.basename(file_path)
            base_filename = os.path.splitext(filename)[0]
            
            # 提取标题和元数据
            title, metadata = self.extract_title_and_metadata(content)
            
            # 提取各章节内容
            sections = self.extract_sections(content)
            
            # 提取引用关系
            references = self.extract_references(content)
            
            # 提取引用的理论维度
            ref_dimensions = self.extract_reference_dimensions(content)
            
            # 创建结构化的理论数据
            theory_data = {
                "filename": base_filename,
                "title": title,
                "metadata": metadata,
                "sections": sections,
                "references": references,
                "reference_dimensions": ref_dimensions,
                "english_version": base_filename + "_en.md" if os.path.exists(os.path.join(self.base_dir, base_filename + "_en.md")) else None
            }
            
            return theory_data
        
        except Exception as e:
            print(f"解析文件 {file_path} 时出错: {e}")
            return {"error": str(e), "filename": os.path.basename(file_path)}
    
    def parse_all_theories(self) -> Dict[str, Any]:
        """解析所有理论文件并返回结构化数据"""
        all_theories = {}
        for file_path in self.get_all_theory_files():
            theory_data = self.parse_theory_file(file_path)
            file_id = os.path.splitext(os.path.basename(file_path))[0]
            all_theories[file_id] = theory_data
        
        # 添加理论之间的关系图
        all_theories["_meta"] = self.generate_theory_graph(all_theories)
        
        return all_theories
    
    def generate_theory_graph(self, theories: Dict[str, Any]) -> Dict[str, Any]:
        """生成理论之间的关系图"""
        theory_graph = {
            "dependencies": {},
            "dimensions": {},
            "theory_count": len(theories)
        }
        
        # 构建依赖关系
        for theory_id, theory_data in theories.items():
            if theory_id.startswith('_'):
                continue
                
            refs = theory_data.get("references", {})
            ref_links = [ref for ref in refs.values() if ref.startswith("formal_theory_")]
            
            # 去除扩展名，只保留文件名
            ref_links = [os.path.splitext(ref)[0] for ref in ref_links]
            
            theory_graph["dependencies"][theory_id] = ref_links
            
            # 添加维度信息
            dim = theory_data.get("metadata", {}).get("dimension", "未知")
            theory_graph["dimensions"][theory_id] = dim
        
        return theory_graph
    
    def save_to_json(self, output_file: str = "formal_theories.json") -> None:
        """解析所有理论并保存到JSON文件"""
        theories = self.parse_all_theories()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(theories, f, ensure_ascii=False, indent=2)
        print(f"成功解析 {len(theories) - 1} 个理论文件，结果已保存到 {output_file}")

    def generate_verification_data(self, theories: Dict[str, Any]) -> Dict[str, Any]:
        """生成用于验证的数据"""
        verification = {}
        
        for theory_id, theory_data in theories.items():
            if theory_id.startswith('_'):
                continue
                
            # 提取公式和定理，用于验证
            all_formulas = []
            all_theorems = []
            
            # 从各章节中提取公式和定理
            for section_name, section_data in theory_data.get("sections", {}).items():
                all_formulas.extend(section_data.get("formulas", []))
                all_theorems.extend(section_data.get("theorems", []))
                
                # 从子章节中提取
                for subsection_name, subsection_data in section_data.get("subsections", {}).items():
                    all_formulas.extend(subsection_data.get("formulas", []))
                    all_theorems.extend(subsection_data.get("theorems", []))
            
            verification[theory_id] = {
                "formula_count": len(all_formulas),
                "theorem_count": len(all_theorems),
                "dimension_consistent": self.check_dimension_consistency(theory_data),
                "reference_validity": self.check_reference_validity(theory_data, theories),
                "formal_verification": {
                    "is_complete": len(all_formulas) > 0 and len(all_theorems) > 0,
                    "has_proofs": any("proofs" in section_data and section_data["proofs"] 
                                    for section_data in theory_data.get("sections", {}).values())
                }
            }
        
        return verification
    
    def check_dimension_consistency(self, theory_data: Dict[str, Any]) -> bool:
        """检查理论维度的一致性"""
        # 提取标题中的维度
        title_dim = theory_data.get("metadata", {}).get("dimension", "未知")
        
        # 提取正文中提到的维度
        ref_dims = theory_data.get("reference_dimensions", {})
        theory_name = theory_data.get("title", "").split("[")[0].strip()
        
        # 如果在引用维度中找到了该理论
        if theory_name in ref_dims:
            ref_dim = ref_dims[theory_name]
            # 检查标题维度和引用维度是否一致
            return title_dim == ref_dim
        
        return True  # 如果没有在引用中找到，则视为一致
    
    def check_reference_validity(self, theory_data: Dict[str, Any], all_theories: Dict[str, Any]) -> bool:
        """检查理论引用的有效性"""
        refs = theory_data.get("references", {})
        
        for ref_link in refs.values():
            if ref_link.startswith("formal_theory_"):
                ref_id = os.path.splitext(ref_link)[0]
                if ref_id not in all_theories:
                    return False  # 引用了不存在的理论
        
        return True

def main():
    parser = argparse.ArgumentParser(description='将形式化理论文档转换为JSON格式')
    parser.add_argument('--dir', default='formal_theory', help='形式化理论文档的目录')
    parser.add_argument('--output', default='formal_theories.json', help='输出的JSON文件名')
    parser.add_argument('--verification', action='store_true', help='包含验证数据')
    args = parser.parse_args()
    
    parser = TheoryParser(args.dir)
    theories = parser.parse_all_theories()
    
    if args.verification:
        verification_data = parser.generate_verification_data(theories)
        theories["_verification"] = verification_data
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(theories, f, ensure_ascii=False, indent=2)
    
    print(f"成功解析 {len(theories) - (2 if args.verification else 1)} 个理论文件，结果已保存到 {args.output}")

if __name__ == "__main__":
    main() 