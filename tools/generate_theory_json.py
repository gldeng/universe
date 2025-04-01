#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import glob
import sys

def extract_dimension_number(dimension):
    """从维度字符串中提取数字，用于排序"""
    if dimension == "无维度":
        return -999
    
    # 移除所有空格
    dimension = dimension.replace(" ", "")
    
    # 处理D∞或者D+∞的情况
    if "∞" in dimension:
        return float('inf')
    
    # 提取数字部分，支持负数
    match = re.search(r'D([+-]?\d+)', dimension)
    if match:
        return int(match.group(1))
    
    return -999

def extract_dimension(content):
    """从文件内容中提取维度信息"""
    # 支持更多格式的维度表示，包括负数
    dimension_patterns = [
        r'[（\(]维度\s*[：:]\s*D\s*([+-]?[0-9∞\+]+)[）\)]',  # (维度：D-1) 或 (维度：D1) 或 (维度:D1) 或 (维度：D∞)
        r'维度\s*[：:]\s*D\s*([+-]?[0-9∞\+]+)',             # 维度：D-1 或 维度：D1 或 维度:D1 或 维度：D∞
        r'[（\(]D\s*([+-]?[0-9∞\+]+)[）\)]',                # (D-1) 或 (D1) 或 (D∞)
        r'\bD\s*([+-]?[0-9∞\+]+)\s*维度',                   # D-1维度 或 D1维度 或 D∞维度
        r'维度\s*[：:]\s*([+-]?[0-9∞\+]+)',                 # 维度：-1 或 维度：1 或 维度:1
    ]
    
    for pattern in dimension_patterns:
        dimension_match = re.search(pattern, content)
        if dimension_match:
            dimension = dimension_match.group(1).strip()
            # 处理数字和维度之间可能的空格
            return f"D{dimension.replace(' ', '')}"
    
    return "无维度"

def extract_dependencies(content):
    """从文件内容中提取依赖的理论"""
    dependencies = []
    
    # 1. 首先尝试查找"本理论依赖的理论"章节
    dependency_section_patterns = [
        r'### 7\.1 本理论引用的其他理论(.*?)(?:###|$)',
        r'## 7\.1 本理论引用的其他理论(.*?)(?:##|$)',
        r'### 6\.1 本理论依赖的理论(.*?)(?:###|$)',
        r'## 6\.1 本理论依赖的理论(.*?)(?:##|$)',
        r'## 本理论依赖的理论(.*?)(?:##|$)',
        r'### 本理论依赖的理论(.*?)(?:###|$)',
        r'本理论(?:直接)?基于以下(?:形式化)?理论[：:](.*?)(?:##|\n\n|$)'
    ]
    
    for pattern in dependency_section_patterns:
        section_match = re.search(pattern, content, re.DOTALL)
        if section_match:
            section_content = section_match.group(1).strip()
            
            # 检查是否包含表格格式
            if '|' in section_content and '-|-' in section_content:
                # 处理表格格式，提取理论名称列
                table_rows = section_content.split('\n')
                # 过滤掉表头和分隔行
                data_rows = [row for row in table_rows if row.strip() and not row.strip().startswith('|-')]
                if len(data_rows) > 2:  # 至少有表头和一个数据行
                    # 从第二行开始是数据行
                    for row in data_rows[2:]:
                        # 分割行并清理空格
                        columns = [col.strip() for col in row.split('|') if col.strip()]
                        if columns and len(columns) >= 1:
                            # 第一列通常是理论名称
                            theory_name = columns[0]
                            # 检查是否包含链接
                            link_match = re.search(r'\[([^\]]+)\]', theory_name)
                            if link_match:
                                dependencies.append(link_match.group(1))
                            else:
                                dependencies.append(theory_name)
            
            # 尝试提取有序列表项
            if not dependencies:
                list_items = re.findall(r'\d+\.\s*\[([^\]]+)\]', section_content)
                if list_items:
                    dependencies.extend(list_items)
            
            # 尝试提取无序列表项中的链接
            if not dependencies:
                list_items = re.findall(r'[-*]\s*\[([^\]]+)\]', section_content)
                if list_items:
                    dependencies.extend(list_items)
            
            # 尝试提取普通链接
            if not dependencies:
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', section_content)
                if links:
                    dependencies.extend([link[0] for link in links])
            
            # 如果以上都没找到，尝试提取列表项（不带链接）
            if not dependencies:
                items = re.findall(r'[-*\d]\s*(.*?)(?:\n|$)', section_content)
                filtered_items = []
                for item in items:
                    item = item.strip()
                    # 忽略太短或无实质内容的项
                    if len(item) > 5 and not item.startswith('-') and not item.startswith('*'):
                        filtered_items.append(item)
                if filtered_items:
                    dependencies.extend(filtered_items)
            
            break  # 找到依赖章节后退出循环
    
    # 2. 如果没有找到依赖理论章节，尝试查找"理论引用关系分析"中的依赖部分
    if not dependencies:
        section_pattern = r'(## 6\. 理论引用关系分析|### 6\.2 理论依赖关系|## 理论引用关系分析|## 理论依赖关系)'
        section_match = re.search(section_pattern, content)
        
        if section_match:
            # 获取章节后的内容
            section_start = section_match.end()
            # 找下一个章节或文件结束
            next_section = re.search(r'##(?!#)', content[section_start:])
            if next_section:
                section_content = content[section_start:section_start + next_section.start()]
            else:
                section_content = content[section_start:]
            
            # 提取依赖关系
            # 1. 搜索直接依赖部分
            direct_deps_pattern = r'直接依赖.*?:(.*?)(?:(?:间接依赖|##|\Z))'
            direct_deps_match = re.search(direct_deps_pattern, section_content, re.DOTALL)
            
            if direct_deps_match:
                deps_text = direct_deps_match.group(1).strip()
                # 提取链接格式的依赖
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', deps_text)
                for link in links:
                    dependencies.append(link[0])
                
                # 如果没有找到链接，尝试从列表项中提取
                if not links:
                    list_items = re.findall(r'[-*]\s*\[?([^\]\n]+)(?:\]|$)', deps_text)
                    for item in list_items:
                        item = item.strip()
                        if item and not item.startswith('被依赖') and not item.startswith('[依赖关系'):  # 过滤掉不是依赖的行
                            dependencies.append(item)
    
    # 3. 如果上面方法没找到依赖，尝试其他模式
    if not dependencies:
        # 尝试多种可能的依赖声明模式
        patterns = [
            # 特定关键词后的依赖列表
            r'依赖理论\s*[：:]\s*(.+?)(?:\n\n|\Z)',
            r'理论依赖\s*[：:]\s*(.+?)(?:\n\n|\Z)',
            r'依赖\s*[：:]\s*(.+?)(?:\n\n|\Z)',
            r'理论基于(.+?)(?:理论|$)',
            r'引用理论\s*[：:]\s*(.+?)(?:\n\n|\Z)',
            # 依赖列表标记
            r'- 直接依赖\s*[：:]\s*(.+?)(?:\n\n|\Z)',
        ]
        
        for pattern in patterns:
            matches = re.search(pattern, content, re.DOTALL)
            if matches:
                text = matches.group(1).strip()
                # 提取markdown链接
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
                if links:
                    # 从链接中提取标题
                    dependencies.extend([link[0] for link in links])
                else:
                    # 尝试从列表项中提取
                    list_items = re.findall(r'[-*]\s*([^\n]+)', text)
                    if list_items:
                        dependencies.extend([item.strip() for item in list_items if item.strip()])
                    else:
                        # 如果没有找到链接格式，尝试直接使用文本中的理论名称
                        # 通过逗号、分号或换行符分割
                        items = re.split(r'[,，;；\n]', text)
                        dependencies.extend([item.strip() for item in items if item.strip()])
                
                if dependencies:  # 如果找到依赖，跳出循环
                    break
    
    # 过滤和清理依赖项
    cleaned_dependencies = []
    for dep in dependencies:
        # 移除版本号，如 [v36.0]
        dep = re.sub(r'\s*\[.*?\]', '', dep)
        # 移除依赖关系描述
        dep = re.sub(r'\s*\[依赖关系.*?\]', '', dep)
        # 清理可能的前导符号和空格
        dep = re.sub(r'^[-*•\d\.]\s*', '', dep)
        # 如果是形式为"理论名 - 描述"的形式，只保留理论名
        if ' - ' in dep:
            dep = dep.split(' - ')[0].strip()
        # 如果包含"提供"、"支持"等词汇，可能是描述部分，需要清理
        if re.search(r'提供|支持', dep):
            continue
        
        if dep.strip() and len(dep.strip()) > 3:  # 只保留长度大于3的依赖项
            # 检查是否已经有类似的依赖项
            is_duplicate = False
            for existing_dep in cleaned_dependencies:
                # 如果依赖项是已存在项的子字符串或反之，认为是重复
                if dep in existing_dep or existing_dep in dep:
                    is_duplicate = True
                    break
            if not is_duplicate:
                cleaned_dependencies.append(dep.strip())
    
    # 移除重复项
    return list(dict.fromkeys(cleaned_dependencies))

def analyze_theory_files(directory):
    """分析目录中的所有理论文件，获取维度和依赖关系"""
    files_data = []
    dependency_map = {}
    unresolved_deps = {}  # 用于记录无法解析的依赖
    
    # 获取目录中所有.md文件
    files = glob.glob(os.path.join(directory, "*.md"))
    
    # 创建标题到文件名的映射
    title_to_filename = {}
    filename_patterns = {}  # 用于存储文件名中的关键词和对应文件
    
    # 第一遍：收集所有文件信息和标题到文件名的映射
    for file_path in files:
        # 忽略英文版文件
        if file_path.endswith("_en.md"):
            continue
        
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            title_match = re.search(r'# (.+?) v', content)
            title = title_match.group(1) if title_match else filename
            
            dimension = extract_dimension(content)
            dependencies = extract_dependencies(content)
            
            # 保存文件信息
            file_info = {
                "文件名": filename,
                "标题": title,
                "维度": dimension,
                "依赖": dependencies,
                "需要重新生成": len(dependencies) == 0  # 没有依赖理论的标记为需要重新生成
            }
            
            files_data.append(file_info)
            
            # 添加到标题到文件名的映射
            title_to_filename[title] = filename
            
            # 添加标题的多种变体到映射
            # 1. 完整标题
            title_to_filename[title] = filename
            
            # 2. 去掉"的严格形式化描述"后的标题
            simple_title = re.sub(r'的严格形式化描述.*$', '', title).strip()
            title_to_filename[simple_title] = filename
            
            # 3. 更简短的标题变体（去掉一些常见后缀）
            shorter_title = re.sub(r'的.*$', '', simple_title).strip()
            if shorter_title != simple_title:
                title_to_filename[shorter_title] = filename
            
            # 4. 去掉"理论"这个词的变体
            no_theory_title = re.sub(r'理论$', '', simple_title).strip()
            if no_theory_title != simple_title:
                title_to_filename[no_theory_title] = filename
            
            # 5. 从文件名构建的变体
            base_filename = filename.replace("formal_theory_", "").replace(".md", "")
            # 把下划线转换为空格
            filename_based_title = base_filename.replace("_", " ")
            title_to_filename[filename_based_title] = filename
            
            # 6. 收集文件名中的关键词
            keywords = re.findall(r'[a-z]+', base_filename)
            for keyword in keywords:
                if len(keyword) > 3:  # 只考虑长度大于3的关键词
                    if keyword not in filename_patterns:
                        filename_patterns[keyword] = []
                    filename_patterns[keyword].append(filename)
            
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}", file=sys.stderr)
    
    # 按维度从高到低排序
    files_data.sort(key=lambda x: extract_dimension_number(x["维度"]), reverse=True)
    
    # 第二遍：构建依赖关系（使用文件名表示）
    for file_info in files_data:
        source_filename = file_info["文件名"]
        dependency_filenames = []
        unresolved = []
        
        # 将标题形式的依赖转换为文件名形式
        for dep_title in file_info["依赖"]:
            resolved = False
            
            # 1. 尝试直接匹配
            if dep_title in title_to_filename:
                dependency_filenames.append(title_to_filename[dep_title])
                resolved = True
            else:
                # 2. 尝试对依赖标题进行清理后匹配
                cleaned_dep = re.sub(r'的严格形式化描述.*$', '', dep_title).strip()
                if cleaned_dep in title_to_filename:
                    dependency_filenames.append(title_to_filename[cleaned_dep])
                    resolved = True
                else:
                    # 3. 尝试去掉"理论"这个词后匹配
                    no_theory_dep = re.sub(r'理论$', '', cleaned_dep).strip()
                    if no_theory_dep in title_to_filename:
                        dependency_filenames.append(title_to_filename[no_theory_dep])
                        resolved = True
                    else:
                        # 4. 使用更宽松的匹配
                        best_match = None
                        highest_similarity = 0
                        
                        for title, fname in title_to_filename.items():
                            # 如果依赖标题包含在已知标题中，或已知标题包含在依赖标题中
                            if dep_title in title or title in dep_title:
                                # 计算相似度（简单使用长度比例）
                                similarity = min(len(dep_title), len(title)) / max(len(dep_title), len(title))
                                if similarity > highest_similarity and similarity > 0.5:  # 设置一个相似度阈值
                                    highest_similarity = similarity
                                    best_match = fname
                        
                        if best_match:
                            dependency_filenames.append(best_match)
                            resolved = True
                        else:
                            # 5. 如果仍然无法解析，尝试基于文件名中的关键词匹配
                            dep_keywords = re.findall(r'[a-zA-Z]+', dep_title.lower())
                            matching_files = []
                            
                            for keyword in dep_keywords:
                                if len(keyword) > 3 and keyword in filename_patterns:  # 只考虑长度大于3的关键词
                                    matching_files.extend(filename_patterns[keyword])
                            
                            if matching_files:
                                # 统计每个文件的匹配次数
                                file_counts = {}
                                for f in matching_files:
                                    if f not in file_counts:
                                        file_counts[f] = 0
                                    file_counts[f] += 1
                                
                                # 选择匹配次数最多的文件
                                if file_counts:
                                    best_file = max(file_counts.items(), key=lambda x: x[1])[0]
                                    dependency_filenames.append(best_file)
                                    resolved = True
            
            if not resolved:
                unresolved.append(dep_title)
        
        # 如果有依赖项，添加到依赖映射
        if file_info["依赖"]:
            # 记录原始依赖、已解析依赖和未解析依赖
            dependency_map[source_filename] = {
                "original_deps": file_info["依赖"],
                "resolved_deps": dependency_filenames,
                "unresolved_deps": unresolved
            }
            
            # 更新未解析依赖的统计
            if unresolved:
                unresolved_deps[source_filename] = unresolved
    
    # 计算统计信息
    files_with_dimension = [f for f in files_data if f['维度'] != "无维度"]
    files_with_dependencies = [f for f in files_data if f['依赖']]
    files_need_regenerate = [f for f in files_data if f['需要重新生成']]
    
    return {
        "files": files_data,
        "dependencies": dependency_map,
        "unresolved_dependencies": unresolved_deps,  # 添加未解析依赖的信息
        "statistics": {
            "total_files": len(files_data),
            "files_with_dependencies": len(files_with_dependencies),
            "files_with_dimension": len(files_with_dimension),
            "files_need_regenerate": len(files_need_regenerate),
            "unresolved_dependencies_count": sum(len(deps) for deps in unresolved_deps.values())
        }
    }

if __name__ == "__main__":
    # 分析形式化理论目录
    directory = "formal_theory"
    result = analyze_theory_files(directory)
    
    # 直接输出JSON到控制台
    print(json.dumps(result, ensure_ascii=False, indent=2)) 