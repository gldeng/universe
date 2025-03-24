#!/usr/bin/env python3
import os
import re
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json

def get_git_last_commit_date(file_path: str) -> Optional[datetime]:
    """获取文件最后一次提交的日期"""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%at', file_path],
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            return datetime.fromtimestamp(int(result.stdout.strip()))
        return None
    except subprocess.CalledProcessError:
        return None

def extract_version(content: str) -> Optional[str]:
    """从文件内容中提取版本号
    支持格式：版本X.X
    """
    pattern = r'版本\s*(\d+\.\d+)'
    
    # 首先检查文件的前20行
    first_lines = content.split('\n')[:20]
    first_content = '\n'.join(first_lines)
    
    match = re.search(pattern, first_content)
    if match:
        return match.group(1)
        
    # 如果在前20行没找到，检查整个文件
    match = re.search(pattern, content)
    if match:
        return match.group(1)
            
    return None

def get_english_file_paths(chinese_file: str) -> List[str]:
    """获取所有可能的英文文件路径"""
    base, ext = os.path.splitext(chinese_file)
    paths = []
    
    # 检查 _en 结尾的文件
    en_path = f"{base}_en{ext}"
    paths.append(en_path)
    
    # 检查 .en 中间的文件
    if base.endswith('.zh'):
        base = base[:-3]
    en_path_2 = f"{base}.en{ext}"
    if en_path_2 not in paths:
        paths.append(en_path_2)
        
    return paths

def is_bilingual_file(content: str) -> bool:
    """检查文件是否为双语文件"""
    # 检查是否同时包含足够的中文和英文内容
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', content))
    
    # 如果中英文内容都超过一定数量，认为是双语文件
    # 这里的阈值可以根据实际情况调整
    return chinese_chars > 50 and english_words > 50

def check_file_exists(file_path: str) -> bool:
    """检查文件是否存在"""
    return os.path.exists(file_path)

def read_file_content(file_path: str) -> Optional[str]:
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None

def compare_versions(ver1: str, ver2: str) -> int:
    """比较版本号，如果ver1大于ver2返回1，相等返回0，小于返回-1"""
    if not ver1 or not ver2:
        return 0
    v1_parts = [int(x) for x in ver1.split('.')]
    v2_parts = [int(x) for x in ver2.split('.')]
    
    for i in range(max(len(v1_parts), len(v2_parts))):
        v1 = v1_parts[i] if i < len(v1_parts) else 0
        v2 = v2_parts[i] if i < len(v2_parts) else 0
        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
    return 0

def find_markdown_files(directory: str) -> List[str]:
    """查找所有的中文Markdown文件"""
    markdown_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.zh.md')) and not file.endswith(('_en.md', '.en.md')):
                full_path = os.path.join(root, file)
                # 检查文件是否包含中文内容
                content = read_file_content(full_path)
                if content and re.search(r'[\u4e00-\u9fff]', content):
                    markdown_files.append(full_path)
    return markdown_files

def check_translation_status(directory: str = '.') -> List[Tuple[str, str, str, bool]]:
    """检查翻译状态，返回需要更新的文件列表"""
    needs_update = []
    chinese_files = find_markdown_files(directory)
    
    for zh_file in chinese_files:
        zh_content = read_file_content(zh_file)
        if not zh_content:
            continue

        # 首先检查是否是双语文件
        is_bilingual = is_bilingual_file(zh_content)
        if is_bilingual:
            zh_version = extract_version(zh_content)
            if not zh_version:
                needs_update.append((zh_file, "", "双语文件缺少版本号", True))
            continue

        # 检查分离的英文文件
        en_files = get_english_file_paths(zh_file)
        en_file_exists = False
        
        for en_file in en_files:
            if check_file_exists(en_file):
                en_file_exists = True
                reason = ""
                
                # 获取最后提交日期
                zh_last_commit = get_git_last_commit_date(zh_file)
                en_last_commit = get_git_last_commit_date(en_file)

                if zh_last_commit and en_last_commit:
                    if zh_last_commit > en_last_commit:
                        reason = "中文版本有新更新"

                # 检查版本号
                en_content = read_file_content(en_file)
                if zh_content and en_content:
                    zh_version = extract_version(zh_content)
                    en_version = extract_version(en_content)

                    if zh_version and en_version:
                        if compare_versions(zh_version, en_version) > 0:
                            reason = f"版本号不一致 (中文: {zh_version}, 英文: {en_version})"
                    elif zh_version and not en_version:
                        reason = "英文版本缺少版本号"

                if reason:
                    needs_update.append((zh_file, en_file, reason, False))
                break

        if not en_file_exists:
            needs_update.append((zh_file, en_files[0], "英文版本不存在", False))

    return needs_update

def check_file(file_path: str) -> Optional[Dict]:
    """检查文件的翻译状态
    
    Returns:
        Optional[Dict]: {
            "file": str,
            "is_bilingual": bool,
            "version": str | None,
            "needs_update": bool,
            "update_reason": str | None,
            "update_type": str | None  # version, git, missing_file
        }
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否是双语文件
        chinese_content = bool(re.search(r'[\u4e00-\u9fff]', content))
        english_content = bool(re.search(r'[a-zA-Z]', content))
        is_bilingual = chinese_content and english_content and \
                      len(re.findall(r'[\u4e00-\u9fff]', content)) > 50 and \
                      len(re.findall(r'\b[a-zA-Z]+\b', content)) > 50
        
        # 检查版本号
        version = extract_version(content)
        
        # 确定是否需要更新和更新原因
        needs_update = False
        update_reason = None
        update_type = None
        
        if not version:
            needs_update = False
            update_reason = "缺少版本号标记"
            update_type = "version"
        elif not is_bilingual:
            # 检查对应的翻译文件
            base_path = os.path.splitext(file_path)[0]
            en_path = f"{base_path}_en.md"
            
            if not os.path.exists(en_path):
                needs_update = True
                update_reason = "缺少对应的英文翻译文件"
                update_type = "missing_file"
            else:
                # 检查git提交日期
                zh_last_commit = get_git_last_commit_date(file_path)
                en_last_commit = get_git_last_commit_date(en_path)
                
                if zh_last_commit and en_last_commit and zh_last_commit > en_last_commit:
                    needs_update = True
                    update_reason = f"中文版本有更新（中文：{zh_last_commit.strftime('%Y-%m-%d')}, 英文：{en_last_commit.strftime('%Y-%m-%d')}）"
                    update_type = "git"
                
                # 检查英文文件的版本号
                with open(en_path, 'r', encoding='utf-8') as f:
                    en_content = f.read()
                en_version = extract_version(en_content)
                
                if en_version and compare_versions(version, en_version) > 0:
                    needs_update = True
                    update_reason = f"版本号不一致（中文：{version}, 英文：{en_version}）"
                    update_type = "version"
            
        return {
            "file": file_path,
            "is_bilingual": is_bilingual,
            "version": version,
            "needs_update": needs_update,
            "update_reason": update_reason,
            "update_type": update_type
        }
            
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return None

def get_directory_stats(files_info: List[Tuple[str, str, List[str]]]) -> Dict:
    """获取目录统计信息"""
    stats = {}
    
    for file_path, file_type, issues in files_info:
        directory = os.path.dirname(file_path)
        if directory not in stats:
            stats[directory] = {
                "total_files": 0,
                "bilingual_files": 0,
                "separate_files": 0,
                "missing_version": 0,
                "missing_translation": 0,
                "needs_update": 0
            }
            
        stats[directory]["total_files"] += 1
        
        if file_type == "双语文件":
            stats[directory]["bilingual_files"] += 1
        else:
            stats[directory]["separate_files"] += 1
            
        if "缺少版本号" in issues:
            stats[directory]["missing_version"] += 1
        if "缺少翻译" in issues:
            stats[directory]["missing_translation"] += 1
        if issues:
            stats[directory]["needs_update"] += 1
            
    return stats

def print_directory_stats(stats: Dict[str, Dict[str, int]]):
    """打印目录统计信息"""
    print("\n目录统计信息:")
    print("=" * 120)
    print(f"{'目录':<40} {'总文件数':>8} {'双语文件':>8} {'分离文件':>8} {'缺版本号':>8} {'缺翻译':>8} {'需更新':>8}")
    print("-" * 120)
    
    # 计算总计
    totals = {
        "total": 0,
        "bilingual": 0,
        "separate": 0,
        "missing_version": 0,
        "missing_translation": 0,
        "needs_update": 0
    }
    
    # 按目录名称排序
    for dir_path, counts in sorted(stats.items()):
        print(f"{dir_path:<40} {counts['total_files']:>8} {counts['bilingual_files']:>8} {counts['separate_files']:>8} "
              f"{counts['missing_version']:>8} {counts['missing_translation']:>8} {counts['needs_update']:>8}")
        
        # 累加总计
        for key in totals:
            totals[key] += counts[key]
    
    print("-" * 120)
    print(f"{'总计':<40} {totals['total']:>8} {totals['bilingual']:>8} {totals['separate']:>8} "
          f"{totals['missing_version']:>8} {totals['missing_translation']:>8} {totals['needs_update']:>8}")
    print("=" * 120)

def main():
    files_info = []
    
    for root, dirs, files in os.walk("."):
        if ".git" in root:
            continue
            
        for file in files:
            if not file.endswith(".md"):
                continue
                
            file_path = os.path.join(root, file)
            file_info = check_file(file_path)
            
            if file_info:
                files_info.append(file_info)
    
    # 按文件路径排序
    files_info.sort(key=lambda x: x["file"])
    
    # 计算统计信息
    stats = {
        "total_files": len(files_info),
        "bilingual_files": sum(1 for f in files_info if f["is_bilingual"]),
        "files_with_version": sum(1 for f in files_info if f["version"]),
        "files_needing_update": sum(1 for f in files_info if f["needs_update"])
    }
    
    # 按更新原因和类型统计
    update_reasons = {}
    update_types = {
        "version": {"count": 0, "files": []},
        "git": {"count": 0, "files": []},
        "missing_file": {"count": 0, "files": []}
    }
    
    for f in files_info:
        if f["needs_update"] and f["update_reason"]:
            reason = f["update_reason"]
            if reason not in update_reasons:
                update_reasons[reason] = 0
            update_reasons[reason] += 1
            
            if f["update_type"]:
                update_types[f["update_type"]]["count"] += 1
                update_types[f["update_type"]]["files"].append(f["file"])
    
    # 输出JSON和统计信息
    print(json.dumps({
        "files": files_info,
        "statistics": stats,
        "update_reasons": update_reasons,
        "update_types": {
            "version_related": {
                "count": update_types["version"]["count"],
                "description": "由版本号问题导致的更新"
            },
            "git_related": {
                "count": update_types["git"]["count"],
                "description": "由git提交时间导致的更新"
            },
            "missing_file": {
                "count": update_types["missing_file"]["count"],
                "description": "由缺少对应文件导致的更新"
            }
        }
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 