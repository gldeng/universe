#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
宇宙本论项目自动化工作流

此工具用于自动化完善宇宙本论项目，包括以下功能：
1. 检查并生成理论维护报告
2. 修复中英文文档链接
3. 重新生成理论索引
4. 更新理论依赖关系图
5. 检查未索引文件并添加到索引
6. 维度统一性检查与修复
7. 生成社交媒体分享内容

使用方法：
python universe_automation.py --all
"""

import os
import sys
import argparse
import subprocess
import datetime
import re
from pathlib import Path
import json

def parse_args():
    parser = argparse.ArgumentParser(description="宇宙本论项目自动化工作流")
    parser.add_argument("--all", action="store_true", help="执行所有自动化任务")
    parser.add_argument("--report", action="store_true", help="生成理论维护报告")
    parser.add_argument("--fix-links", action="store_true", help="修复中英文文档链接")
    parser.add_argument("--update-graph", action="store_true", help="更新理论依赖关系图")
    parser.add_argument("--check-index", action="store_true", help="检查未索引文件")
    parser.add_argument("--update-dimensions", action="store_true", help="维度统一性检查与修复")
    parser.add_argument("--generate-share", action="store_true", help="生成社交媒体分享内容")
    parser.add_argument("--theory-dir", default="../formal_theory", help="理论文件目录")
    parser.add_argument("--output-dir", default="../output", help="输出目录")
    parser.add_argument("--share-platforms", default="all", help="社交媒体平台，用逗号分隔")
    parser.add_argument("--force", action="store_true", help="强制执行所有操作，不询问确认")
    return parser.parse_args()

def run_command(command, desc, verbose=True):
    """运行命令并返回结果"""
    if verbose:
        print(f"执行: {desc}")
        print(f"命令: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if verbose:
            print(f"✅ {desc}成功")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        if verbose:
            print(f"❌ {desc}失败")
            print(f"错误: {e.stderr}")
        return False, e.stderr

def create_output_dir(output_dir):
    """创建输出目录（如果不存在）"""
    os.makedirs(output_dir, exist_ok=True)
    print(f"✅ 确保输出目录存在: {output_dir}")

def generate_maintenance_report(args):
    """生成理论维护报告"""
    output_file = os.path.join(args.output_dir, f"maintenance_report_{datetime.datetime.now().strftime('%Y%m%d')}.md")
    
    # 确保相对路径正确
    theory_dir_arg = os.path.relpath(args.theory_dir, os.path.dirname(__file__))
    
    command = [
        sys.executable,
        "generate_maintenance_report.py",
        "--theory_dir", theory_dir_arg,
        "--output", output_file
    ]
    
    success, output = run_command(command, "生成理论维护报告")
    
    if success:
        print(f"维护报告已生成: {output_file}")
        # 检查报告中是否有问题需要解决
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                report_content = f.read()
                
            # 检查是否有推荐操作
            recommendations = re.search(r'## 维护建议\n\n(.*?)$', report_content, re.DOTALL)
            if recommendations and "理论体系维护良好" not in recommendations.group(1):
                print("\n⚠️ 维护报告中发现以下建议:")
                print(recommendations.group(1))
                
                if not args.force and not args.all:
                    answer = input("\n是否要自动修复这些问题? (y/n): ")
                    if answer.lower() != 'y':
                        return
                    
                # 根据报告建议执行自动修复
                if "添加未索引的文件" in recommendations.group(1):
                    args.check_index = True
                if "为缺少英文版本的文件创建对应的英文文档" in recommendations.group(1):
                    args.sync_languages = True
                if "修复损坏的链接" in recommendations.group(1):
                    args.fix_links = True
                if "更新版本不一致的文件" in recommendations.group(1):
                    args.update_versions = True
        except Exception as e:
            print(f"分析报告时出错: {e}")
    
    return success

def fix_critical_links(args):
    """修复中英文文档链接"""
    command = [
        sys.executable,
        "fix_critical_links.py",
        os.path.relpath(args.theory_dir, os.path.dirname(__file__))
    ]
    
    success, output = run_command(command, "修复中英文文档链接")
    return success

def update_theory_graph(args):
    """更新理论依赖关系图"""
    output_file = os.path.join(args.output_dir, "theory_graph")
    
    command = [
        sys.executable,
        "generate_theory_graph.py",
        "--theory_dir", os.path.relpath(args.theory_dir, os.path.dirname(__file__)),
        "--output", output_file,
        "--format", "all"
    ]
    
    success, output = run_command(command, "更新理论依赖关系图")
    
    if success:
        print(f"理论依赖关系图已生成:")
        print(f"- DOT: {output_file}.dot")
        print(f"- PNG: {output_file}.png")
        print(f"- HTML: {output_file}.html")
    
    return success

def check_unindexed_files(args):
    """检查未索引文件并添加到索引"""
    # 首先运行检查未索引文件的工具
    command = [
        sys.executable,
        "check_unindexed_files.py",
        "--dir", os.path.relpath(args.theory_dir, os.path.dirname(__file__)),
        "--output", os.path.join(args.output_dir, "unindexed_files.json")
    ]
    
    success, output = run_command(command, "检查未索引文件")
    
    if not success:
        return False
    
    # 分析结果并询问是否要添加到索引
    try:
        with open(os.path.join(args.output_dir, "unindexed_files.json"), 'r', encoding='utf-8') as f:
            unindexed_data = json.load(f)
        
        cn_unindexed = unindexed_data.get("chinese", [])
        en_unindexed = unindexed_data.get("english", [])
        
        if not cn_unindexed and not en_unindexed:
            print("✅ 没有发现未索引的文件")
            return True
        
        print(f"\n⚠️ 发现 {len(cn_unindexed)} 个未索引的中文文件，{len(en_unindexed)} 个未索引的英文文件")
        
        if not args.force and not args.all:
            answer = input("\n是否要将未索引文件添加到索引? (y/n): ")
            if answer.lower() != 'y':
                return True
        
        # 添加未索引文件到索引
        # 这里只是示例，实际需要根据您的索引文件结构编写更复杂的逻辑
        print("自动添加未索引文件到索引功能尚未实现")
        print("请手动将以下文件添加到索引:")
        
        for file in cn_unindexed:
            print(f"- 中文: {file}")
        
        for file in en_unindexed:
            print(f"- 英文: {file}")
        
        return True
    except Exception as e:
        print(f"处理未索引文件数据时出错: {e}")
        return False

def update_dimensions(args):
    """维度统一性检查与修复"""
    command = [
        sys.executable,
        "update_dimensions.py",
        "--dir", os.path.relpath(args.theory_dir, os.path.dirname(__file__))
    ]
    
    success, output = run_command(command, "维度统一性检查与修复")
    return success

def generate_theories_json(args):
    """生成理论JSON数据"""
    output_file = os.path.join(args.output_dir, f"formal_theories_{datetime.datetime.now().strftime('%Y%m%d')}.json")
    
    command = [
        sys.executable,
        "generate_theory_json.py",
        "--dir", os.path.relpath(args.theory_dir, os.path.dirname(__file__)),
        "--output", output_file,
        "--verification"
    ]
    
    success, output = run_command(command, "生成理论JSON数据")
    
    if success:
        print(f"理论JSON数据已生成: {output_file}")
    
    return success

def generate_share_content(args):
    """生成社交媒体分享内容"""
    # 创建社交媒体分享内容输出目录
    share_output_dir = os.path.join(args.output_dir, "share")
    os.makedirs(share_output_dir, exist_ok=True)
    
    # 获取理论文件目录下的核心理论文件
    theory_dir = os.path.relpath(args.theory_dir, os.path.dirname(__file__))
    core_theories = [
        "formal_theory_cosmic_ontology.md",
        "formal_theory_consciousness_essence_origin.md",
        "formal_theory_dark_matter_dark_energy.md",
        "formal_theory_unified_physics.md",
    ]
    
    # 处理需要生成的社交媒体平台
    platforms = args.share_platforms.split(',') if args.share_platforms != "all" else ["all"]
    
    success_count = 0
    total_count = len(core_theories)
    
    for theory_file in core_theories:
        theory_path = os.path.join(theory_dir, theory_file)
        
        # 检查文件是否存在
        if not os.path.exists(theory_path):
            print(f"⚠️ 理论文件不存在: {theory_path}")
            continue
        
        # 为每个理论生成分享内容
        command = [
            sys.executable,
            "share_tool_generator.py",
            "--input", theory_path,
            "--output-dir", share_output_dir,
            "--platform", platforms[0]  # 使用第一个平台或"all"
        ]
        
        success, output = run_command(command, f"为 {theory_file} 生成社交媒体分享内容")
        
        if success:
            success_count += 1
    
    print(f"\n成功为 {success_count}/{total_count} 个核心理论生成了社交媒体分享内容")
    print(f"分享内容已保存到: {share_output_dir}")
    
    return success_count > 0

def main():
    args = parse_args()
    
    # 如果指定了--all，则执行所有任务
    if args.all:
        args.report = True
        args.fix_links = True
        args.update_graph = True
        args.check_index = True
        args.update_dimensions = True
        args.generate_share = True
    
    # 确保输出目录存在
    create_output_dir(args.output_dir)
    
    # 显示当前工作目录
    print(f"当前工作目录: {os.getcwd()}")
    print(f"理论文件目录: {args.theory_dir}")
    print(f"输出目录: {args.output_dir}")
    
    # 显示要执行的任务
    tasks = []
    if args.report:
        tasks.append("生成理论维护报告")
    if args.fix_links:
        tasks.append("修复中英文文档链接")
    if args.update_graph:
        tasks.append("更新理论依赖关系图")
    if args.check_index:
        tasks.append("检查未索引文件")
    if args.update_dimensions:
        tasks.append("维度统一性检查与修复")
    if args.generate_share:
        tasks.append("生成社交媒体分享内容")
    
    print("\n将执行以下任务:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    
    if not args.force and not tasks:
        print("未指定任何任务，使用 --help 查看可用选项")
        return
    
    print("\n开始执行自动化工作流...\n")
    
    # 执行任务
    results = {}
    
    if args.report:
        results["report"] = generate_maintenance_report(args)
    
    if args.fix_links:
        results["fix_links"] = fix_critical_links(args)
    
    if args.update_graph:
        results["update_graph"] = update_theory_graph(args)
    
    if args.check_index:
        results["check_index"] = check_unindexed_files(args)
    
    if args.update_dimensions:
        results["update_dimensions"] = update_dimensions(args)
    
    if args.generate_share:
        results["generate_share"] = generate_share_content(args)
    
    # 生成理论JSON数据（作为最后一步）
    if any(results.values()):
        results["generate_json"] = generate_theories_json(args)
    
    # 输出结果摘要
    print("\n工作流执行结果摘要:")
    for task, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        task_name = {
            "report": "生成理论维护报告",
            "fix_links": "修复中英文文档链接",
            "update_graph": "更新理论依赖关系图",
            "check_index": "检查未索引文件",
            "update_dimensions": "维度统一性检查与修复",
            "generate_share": "生成社交媒体分享内容",
            "generate_json": "生成理论JSON数据"
        }.get(task, task)
        
        print(f"{status} {task_name}")
    
    # 最终总结
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"\n总结: 成功完成 {successful}/{total} 项任务")
    
    if successful == total:
        print("\n🎉 宇宙本论项目自动化工作流完成!")
    else:
        print("\n⚠️ 宇宙本论项目自动化工作流完成，但有些任务失败，请查看详细日志")

if __name__ == "__main__":
    main() 