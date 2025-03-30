import os
import re
import json
import subprocess
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple

def get_git_timestamp(file_path: str) -> int:
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ct', file_path],
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            return int(result.stdout.strip())
        return 0
    except (subprocess.CalledProcessError, ValueError):
        return 0

def extract_version(content: str) -> float:
    # 查找中文版本号
    cn_match = re.search(r'版本(\d+\.\d+)', content)
    if cn_match:
        return float(cn_match.group(1))
    
    # 查找英文版本号 (考虑 Version 和数字之间可能有空格)
    en_match = re.search(r'Version\s*(\d+\.\d+)', content)
    if en_match:
        return float(en_match.group(1))
    
    return 0.0

def is_bilingual(content: str) -> bool:
    # 检查是否同时包含中英文内容
    # 简单检查是否同时包含中文字符和英文字母
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', content))
    has_english = bool(re.search(r'[a-zA-Z]', content))
    return has_chinese and has_english

def check_file(cn_file: str) -> Dict:
    # 检查文件是否为空
    if os.path.getsize(cn_file) == 0:
        return {
            "中文文件": cn_file,
            "英文文件": "",
            "是否要更新": False,
            "中文git时间": 0,
            "英文git时间": 0,
            "中文版本": 0.0,
            "英文版本号": 0.0,
            "更新原因": "空文件，已跳过"
        }

    en_file = cn_file[:-3] + '_en.md'
    result = {
        "中文文件": cn_file,
        "英文文件": en_file if os.path.exists(en_file) else "",
        "是否要更新": False,
        "中文git时间": 0,
        "英文git时间": 0,
        "中文版本": 0.0,
        "英文版本号": 0.0,
        "更新原因": ""
    }
    
    # 读取中文文件内容
    try:
        with open(cn_file, 'r', encoding='utf-8') as f:
            cn_content = f.read()
    except:
        return result
    
    # 获取中文文件信息
    result["中文git时间"] = get_git_timestamp(cn_file)
    result["中文版本"] = extract_version(cn_content)
    
    # 如果英文文件不存在
    if not os.path.exists(en_file):
        # 检查中文文件是否已经是双语的
        if is_bilingual(cn_content):
            result["是否要更新"] = False
            return result
        else:
            result["是否要更新"] = True
            result["更新原因"] = "缺少英文版本"
            return result
    
    # 读取英文文件内容
    try:
        with open(en_file, 'r', encoding='utf-8') as f:
            en_content = f.read()
    except:
        return result
    
    # 获取英文文件信息
    result["英文git时间"] = get_git_timestamp(en_file)
    result["英文版本号"] = extract_version(en_content)
    
    # 检查是否需要更新
    if result["中文git时间"] > result["英文git时间"]:
        result["是否要更新"] = True
        result["更新原因"] = "git提交"
    elif result["中文版本"] > result["英文版本号"]:
        result["是否要更新"] = True
        result["更新原因"] = "版本号"
    
    return result

def main():
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='检查文档更新状态')
    parser.add_argument('--check-no-version', action='store_true',
                      help='将没有版本号的文件标记为需要更新')
    args = parser.parse_args()

    results = []
    stats = {
        "总文件数": 0,
        "需要更新数": 0,
        "双语文件数": 0,
        "缺少英文版本数": 0,
        "无版本号文件数": 0
    }
    
    # 遍历所有.md文件
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.md') and not file.endswith('_en.md'):
                file_path = os.path.join(root, file)
                result = check_file(file_path)
                
                # 检查是否没有版本号且需要标记
                if args.check_no_version and result["中文版本"] == 0.0:
                    result["是否要更新"] = True
                    result["更新原因"] = "缺少版本号"
                    stats["无版本号文件数"] += 1
                
                stats["总文件数"] += 1
                if result["是否要更新"]:
                    results.append(result)  # 只添加需要更新的文件到结果列表
                    stats["需要更新数"] += 1
                if not result["英文文件"] and not result["是否要更新"]:
                    stats["双语文件数"] += 1
                if not result["英文文件"] and result["是否要更新"]:
                    stats["缺少英文版本数"] += 1
    
    # 只输出需要更新的文件
    if results:
        print("需要更新的文件:")
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("没有需要更新的文件")
    
    print("\n统计信息:")
    print(json.dumps(stats, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 