#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import argparse
from pathlib import Path

def find_md_files(directory):
    """递归查找所有.md文件"""
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_links(file_path):
    """从Markdown文件中提取链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取Markdown链接格式 [text](link.md) 和 [text](mdc:link.md)
    links = re.findall(r'\[.*?\]\((mdc:)?(.*?\.md)(\#.*?)?\)', content)
    return [(prefix, link, anchor) for prefix, link, anchor in links]

def check_link_exists(base_dir, file_path, link_path):
    """检查链接是否存在"""
    # 获取文件所在目录
    file_dir = os.path.dirname(file_path)
    
    # 特殊处理根目录的核心文件
    root_core_files = ['core.md', 'core_en.md', 'formal_theory_core.md', 'formal_theory_core_en.md']
    if link_path in root_core_files or link_path.endswith(tuple(root_core_files)):
        # 如果链接指向根目录的文件，直接检查根目录
        root_path = os.path.normpath(os.path.join(base_dir, os.path.basename(link_path)))
        if os.path.exists(root_path):
            return root_path
    
    # 构建可能的路径
    possible_paths = [
        os.path.normpath(os.path.join(file_dir, link_path)),  # 相对当前文件
        os.path.normpath(os.path.join(os.path.dirname(file_dir), link_path)),  # 上一级目录
        os.path.normpath(os.path.join(base_dir, link_path)),  # 根目录
        os.path.normpath(os.path.join(base_dir, os.path.basename(link_path))),  # 根目录+文件名
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def replace_formal_theory_links(file_path):
    """替换对core.md, formal_theory.md和formal_theory_en.md的引用"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换core.md链接
    updated_content = re.sub(
        r'\[(.*?)\]\((mdc:)?core\.md(\#.*?)?\)', 
        r'[\1](\2core.md\3)', 
        content
    )
    
    # 处理带相对路径的core.md
    updated_content = re.sub(
        r'\[(.*?)\]\((mdc:)?(\.\./)+core\.md(\#.*?)?\)', 
        r'[\1](\2core.md\4)', 
        updated_content
    )
    
    # 替换formal_theory/formal_theory.md链接 - 中文版
    updated_content = re.sub(
        r'\[(.*?)\]\((mdc:)?formal_theory/formal_theory\.md(\#.*?)?\)', 
        r'[\1](\2formal_theory_core.md\3)', 
        updated_content
    )
    # 替换formal_theory.md链接 - 中文版
    updated_content = re.sub(
        r'\[(.*?)\]\((mdc:)?formal_theory\.md(\#.*?)?\)', 
        r'[\1](\2formal_theory_core.md\3)', 
        updated_content
    )
    
    # 处理带相对路径的中文版 (../../formal_theory.md 或 ../../formal_theory/formal_theory.md)
    updated_content = re.sub(
        r'\[(.*?)\]\((mdc:)?(\.\./)+formal_theory/formal_theory\.md(\#.*?)?\)', 
        r'[\1](\2formal_theory_core.md\4)', 
        updated_content
    )
    updated_content = re.sub(
        r'\[(.*?)\]\((mdc:)?(\.\./)+formal_theory\.md(\#.*?)?\)', 
        r'[\1](\2formal_theory_core.md\4)', 
        updated_content
    )
    
    # 替换链接 - 英文版（带_en后缀）
    updated_content = re.sub(
        r'\[(.*?)\]\((mdc:)?formal_theory/formal_theory_en\.md(\#.*?)?\)', 
        r'[\1](\2formal_theory_core_en.md\3)', 
        updated_content
    )
    updated_content = re.sub(
        r'\[(.*?)\]\((mdc:)?formal_theory_en\.md(\#.*?)?\)', 
        r'[\1](\2formal_theory_core_en.md\3)', 
        updated_content
    )
    
    # 处理带相对路径的英文版 (../../formal_theory_en.md 或 ../../formal_theory/formal_theory_en.md)
    updated_content = re.sub(
        r'\[(.*?)\]\((mdc:)?(\.\./)+formal_theory/formal_theory_en\.md(\#.*?)?\)', 
        r'[\1](\2formal_theory_core_en.md\4)', 
        updated_content
    )
    updated_content = re.sub(
        r'\[(.*?)\]\((mdc:)?(\.\./)+formal_theory_en\.md(\#.*?)?\)', 
        r'[\1](\2formal_theory_core_en.md\4)', 
        updated_content
    )
    
    # 如果内容发生变化，写回文件
    if content != updated_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        return True
    
    return False

def calculate_relative_path(from_path, to_path, base_dir=None):
    """计算从一个文件到另一个文件的相对路径"""
    from_dir = os.path.dirname(os.path.abspath(from_path))
    to_path_abs = os.path.abspath(to_path)
    
    # 针对根目录特殊文件的处理
    root_core_files = ['core.md', 'core_en.md', 'formal_theory_core.md', 'formal_theory_core_en.md']
    if base_dir and os.path.basename(to_path) in root_core_files:
        # 如果是根目录的特殊文件，优先使用这种形式
        # 可能需要计算从当前目录到根目录的路径
        relative_to_root = os.path.relpath(base_dir, from_dir)
        if relative_to_root == '.':
            # 如果已经在根目录
            return os.path.basename(to_path)
        else:
            # 否则拼接到根目录的路径
            return os.path.join(relative_to_root, os.path.basename(to_path))
    
    # 常规相对路径计算
    rel_path = os.path.relpath(to_path_abs, from_dir)
    return rel_path

def fix_link_path(file_path, old_link, target_file_path, anchor="", base_dir=None):
    """修复链接路径，使用相对于文件的路径"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 计算从当前文件到目标文件的相对路径
        new_link = calculate_relative_path(file_path, target_file_path, base_dir)
        
        # 替换链接
        pattern = re.escape(f'[') + r'(.*?)' + re.escape(f']({old_link}{anchor})')
        replacement = r'[\1](' + new_link + anchor + r')'
        updated_content = re.sub(pattern, replacement, content)
        
        # 如果内容发生变化，写回文件
        if content != updated_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True, new_link
        
        return False, old_link
    except Exception as e:
        print(f"修复链接时出错: {e}")
        return False, old_link

def main():
    parser = argparse.ArgumentParser(description='检查Markdown文件中的链接并替换formal_theory.md引用')
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help='要检查的目录路径（默认为当前目录）')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='显示详细输出信息')
    parser.add_argument('-f', '--fix', action='store_true',
                        help='尝试修复可修正的链接')
    parser.add_argument('--formal-theory-only', action='store_true',
                        help='仅替换formal_theory.md的引用，不检查其他链接')
    
    args = parser.parse_args()
    
    # 获取工作目录
    base_dir = args.directory
    
    print(f"在目录 {base_dir} 中检查Markdown链接...")
    
    # 查找所有.md文件
    md_files = find_md_files(base_dir)
    print(f"找到 {len(md_files)} 个Markdown文件")
    
    # 检查每个文件中的链接
    broken_links = []
    replaced_count = 0
    fixed_count = 0
    
    for file_path in md_files:
        rel_path = os.path.relpath(file_path, base_dir)
        
        if args.verbose:
            print(f"\n检查文件: {rel_path}")
        
        # 替换formal_theory.md引用
        if replace_formal_theory_links(file_path):
            replaced_count += 1
            if args.verbose:
                print(f"  已将formal_theory.md的引用替换为formal_theory_core.md")
        
        # 如果仅替换formal_theory.md，则跳过链接检查
        if args.formal_theory_only:
            continue
        
        # 提取并检查链接
        links = extract_links(file_path)
        for prefix, link, anchor in links:
            # 跳过外部链接和带mdc:前缀的链接
            if link.startswith(('http://', 'https://', 'ftp://')) or prefix:
                continue
                
            # 检查链接是否存在
            link_target_path = check_link_exists(base_dir, file_path, link)
            if not link_target_path:
                broken_links.append((file_path, link))
                if args.verbose:
                    print(f"  链接损坏: [{link}] 在文件 {rel_path}")
            else:
                # 计算并比较相对路径
                correct_rel_path = calculate_relative_path(file_path, link_target_path, base_dir)
                if link != correct_rel_path:
                    if args.verbose:
                        print(f"  链接可修正: [{link}] -> [{correct_rel_path}]")
                    
                    # 修复链接
                    if args.fix:
                        fixed, new_path = fix_link_path(file_path, link, link_target_path, anchor, base_dir)
                        if fixed:
                            fixed_count += 1
                            if args.verbose:
                                print(f"  已修复链接: [{link}] -> [{new_path}]")
    
    print("\n检查完成!")
    print(f"替换了 {replaced_count} 个formal_theory.md的引用")
    
    if not args.formal_theory_only:
        if args.fix:
            print(f"修复了 {fixed_count} 个可修正的链接")
        
        if broken_links:
            print(f"发现 {len(broken_links)} 个损坏的链接")
        else:
            print("未发现损坏的链接")

if __name__ == "__main__":
    main() 