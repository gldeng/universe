#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
宇宙本论社交媒体分享工具生成器

此工具用于从理论文档中生成适合社交媒体分享的简化版本内容，包括：
1. 生成核心概念的简短说明（50-100字）
2. 为微信/微博/知乎/小红书等平台提取关键金句
3. 创建分享卡片的HTML/图片模板
4. 添加适合不同平台的标签

使用方法：
python share_tool_generator.py --input ../formal_theory/formal_theory_xxx.md --platform weixin
"""

import os
import re
import sys
import argparse
import json
import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def parse_args():
    parser = argparse.ArgumentParser(description="宇宙本论社交媒体分享工具生成器")
    parser.add_argument("--input", required=True, help="输入理论文件")
    parser.add_argument("--output-dir", default="../output/share", help="输出目录")
    parser.add_argument("--platform", default="all", 
                        choices=["all", "weixin", "weibo", "zhihu", "xiaohongshu", "douyin"], 
                        help="社交媒体平台")
    parser.add_argument("--lang", default="zh", choices=["zh", "en"], help="语言")
    parser.add_argument("--template", default="default", help="模板样式")
    return parser.parse_args()

def extract_theory_info(file_path):
    """从理论文件中提取基本信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'# ([^\[]+)', content)
        title = title_match.group(1).strip() if title_match else "未知理论"
        
        # 提取维度
        dimension_match = re.search(r'\[维度[:：]\s*(\d+|∞)\]', content)
        dimension = dimension_match.group(1) if dimension_match else "未知"
        
        # 提取版本
        version_match = re.search(r'版本：宇宙本论v(\d+\.\d+)', content)
        version = version_match.group(1) if version_match else "未知"
        
        # 提取摘要/简介
        abstract = ""
        abstract_section = re.search(r'## 理论摘要\n\n(.*?)(?=\n\n##|\Z)', content, re.DOTALL)
        if abstract_section:
            abstract = abstract_section.group(1).strip()
        
        # 如果没有摘要，尝试提取第一段
        if not abstract:
            first_para = re.search(r'\n\n([^#\n][^\n]+)', content)
            if first_para:
                abstract = first_para.group(1).strip()
        
        # 提取关键金句
        key_sentences = []
        quote_matches = re.findall(r'>(.*?)\n', content)
        for quote in quote_matches:
            quote = quote.strip()
            if 8 < len(quote) < 100 and '：' not in quote and ':' not in quote:
                key_sentences.append(quote)
        
        # 如果没有提取到金句，尝试从摘要中提取短句
        if not key_sentences and abstract:
            sentences = re.split(r'[。！？\.!?]', abstract)
            key_sentences = [s.strip() for s in sentences if 10 < len(s.strip()) < 80]
        
        # 提取公式（如果有）
        formulas = []
        formula_matches = re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL)
        if formula_matches:
            formulas = [f.strip() for f in formula_matches if len(f.strip()) > 0]
        
        return {
            "title": title,
            "dimension": dimension,
            "version": version,
            "abstract": abstract,
            "key_sentences": key_sentences[:5],  # 最多取5个金句
            "formulas": formulas[:2]  # 最多取2个公式
        }
        
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return None

def generate_share_text(theory_info, platform):
    """生成适合不同平台的分享文本"""
    if platform == "weixin":
        # 微信公众号文章标题格式
        title = f"【宇宙本论】{theory_info['title']}：透视宇宙奥秘的新视角"
        
        # 微信分享格式：标题 + 简介 + 金句 + 公式亮点 + 标签
        text = f"{title}\n\n"
        
        if theory_info['abstract']:
            # 确保摘要不超过200字
            abstract = theory_info['abstract']
            if len(abstract) > 200:
                abstract = abstract[:197] + "..."
            text += f"{abstract}\n\n"
        
        if theory_info['key_sentences']:
            text += "【核心洞见】\n"
            for i, sentence in enumerate(theory_info['key_sentences'], 1):
                text += f"{i}. {sentence}\n"
            text += "\n"
        
        if theory_info['formulas']:
            text += "【数学之美】\n"
            for formula in theory_info['formulas']:
                text += f"$${formula}$$\n\n"
        
        # 添加标签和版本信息
        text += f"\n#宇宙本论 #理论物理 #哲学 #维度{theory_info['dimension']} #v{theory_info['version']}"
        
    elif platform == "weibo":
        # 微博字数有限，需要更简洁
        title = f"【宇宙本论】{theory_info['title']} [维度:{theory_info['dimension']}]"
        
        text = f"{title}\n\n"
        
        # 选取最吸引人的一句金句
        if theory_info['key_sentences']:
            text += f"{theory_info['key_sentences'][0]}\n\n"
        
        # 摘要需要非常简短
        if theory_info['abstract']:
            short_abstract = theory_info['abstract'][:100]
            if len(theory_info['abstract']) > 100:
                short_abstract += "..."
            text += f"{short_abstract}\n\n"
        
        # 添加标签
        text += f"#宇宙本论# #理论物理# #哲学# #科学革命# #维度理论#"
        
    elif platform == "zhihu":
        # 知乎回答/专栏文章格式
        title = f"{theory_info['title']}：宇宙本论的第{theory_info['dimension']}维度视角"
        
        text = f"# {title}\n\n"
        
        if theory_info['abstract']:
            text += f"{theory_info['abstract']}\n\n"
        
        if theory_info['key_sentences']:
            text += "## 核心思想\n\n"
            for sentence in theory_info['key_sentences']:
                text += f"> {sentence}\n\n"
        
        if theory_info['formulas']:
            text += "## 数学表达\n\n"
            for formula in theory_info['formulas']:
                text += f"$${formula}$$\n\n"
        
        # 添加尾注
        text += f"---\n本文基于宇宙本论v{theory_info['version']}，通过两个基本操作XOR与SHIFT构建起对宇宙的全新理解框架。"
        
    elif platform == "xiaohongshu":
        # 小红书标题需要有吸引力
        title = f"震惊！用两个数学符号解释整个宇宙的奥秘！| {theory_info['title']}"
        
        text = f"{title}\n\n"
        
        # 小红书喜欢分点
        text += "🌟 今天给大家分享一个颠覆传统物理学的惊人理论 🌟\n\n"
        
        if theory_info['abstract']:
            short_abstract = theory_info['abstract'][:120]
            if len(theory_info['abstract']) > 120:
                short_abstract += "..."
            text += f"{short_abstract}\n\n"
        
        if theory_info['key_sentences']:
            text += "✨ 核心金句：\n\n"
            for sentence in theory_info['key_sentences'][:3]:  # 小红书最好不超过3点
                text += f"📌 {sentence}\n\n"
        
        # 小红书标签很重要
        text += f"#宇宙本论 #物理学 #思维模型 #知识分享官 #宇宙奥秘 #科学解密"
        
    elif platform == "douyin":
        # 抖音视频标题和描述
        title = f"两个符号解释宇宙！{theory_info['title']}震撼科学界"
        
        # 抖音描述需要非常简短，引发好奇
        text = f"{title}\n\n"
        
        if theory_info['key_sentences']:
            # 只取一句最吸引人的
            text += f"{theory_info['key_sentences'][0]}\n\n"
        
        # 抖音标签
        text += f"#宇宙理论 #科普 #物理学 #知识分享 #维度理论 #科学大揭秘"
    
    else:  # default or "all"
        # 通用格式
        title = f"宇宙本论 | {theory_info['title']} [维度:{theory_info['dimension']}]"
        
        text = f"{title}\n\n"
        
        if theory_info['abstract']:
            text += f"{theory_info['abstract']}\n\n"
        
        if theory_info['key_sentences']:
            text += "核心洞见：\n"
            for sentence in theory_info['key_sentences']:
                text += f"• {sentence}\n"
            text += "\n"
        
        if theory_info['formulas']:
            text += "数学表达：\n"
            for formula in theory_info['formulas']:
                text += f"$${formula}$$\n\n"
        
        text += f"版本：v{theory_info['version']}"
    
    return text

def generate_share_image(theory_info, output_path, template="default"):
    """生成分享图片"""
    # 图片基本设置
    width, height = 1080, 1920  # 常见社交媒体图片比例
    
    # 创建画布
    img = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    try:
        # 尝试加载字体
        title_font = ImageFont.truetype("SimHei", 60)
        subtitle_font = ImageFont.truetype("SimSun", 40)
        body_font = ImageFont.truetype("SimSun", 30)
    except:
        # 如果找不到指定字体，使用默认字体
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # 绘制标题
    title = f"{theory_info['title']} [维度:{theory_info['dimension']}]"
    draw.text((width/2, 150), title, font=title_font, fill=(0, 0, 0), anchor="mm")
    
    # 绘制副标题
    subtitle = "宇宙本论核心概念"
    draw.text((width/2, 250), subtitle, font=subtitle_font, fill=(100, 100, 100), anchor="mm")
    
    # 绘制分隔线
    draw.line([(100, 300), (width-100, 300)], fill=(200, 200, 200), width=3)
    
    # 绘制摘要
    if theory_info['abstract']:
        # 文本换行处理
        abstract = theory_info['abstract']
        if len(abstract) > 400:
            abstract = abstract[:397] + "..."
        
        # 简单的文本换行
        lines = []
        line = ""
        for char in abstract:
            line += char
            if len(line) >= 25:  # 每行大约25个字
                lines.append(line)
                line = ""
        if line:
            lines.append(line)
        
        y_pos = 350
        for line in lines:
            draw.text((width/2, y_pos), line, font=body_font, fill=(50, 50, 50), anchor="mm")
            y_pos += 40
    
    # 绘制金句
    if theory_info['key_sentences']:
        y_pos += 50
        draw.text((width/2, y_pos), "核心洞见", font=subtitle_font, fill=(100, 100, 100), anchor="mm")
        y_pos += 50
        
        for sentence in theory_info['key_sentences']:
            # 简单的文本换行
            words = []
            line = ""
            for char in sentence:
                line += char
                if len(line) >= 25:  # 每行大约25个字
                    words.append(line)
                    line = ""
            if line:
                words.append(line)
            
            for word in words:
                draw.text((width/2, y_pos), word, font=body_font, fill=(50, 50, 50), anchor="mm")
                y_pos += 40
            
            y_pos += 20  # 句子之间的间隔
    
    # 绘制底部版权信息
    footer_text = f"宇宙本论 v{theory_info['version']} | XOR·SHIFT 统一理论"
    draw.text((width/2, height-100), footer_text, font=body_font, fill=(150, 150, 150), anchor="mm")
    
    # 保存图片
    img.save(output_path)
    print(f"分享图片已生成: {output_path}")

def generate_share_html(theory_info, output_path):
    """生成分享HTML页面"""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{theory_info['title']} - 宇宙本论分享页</title>
    <style>
        body {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
            margin-top: 20px;
        }}
        h1 {{
            color: #1a1a1a;
            margin-bottom: 5px;
            font-size: 28px;
        }}
        .dimension {{
            color: #666;
            font-size: 18px;
            margin-bottom: 30px;
        }}
        .abstract {{
            font-size: 16px;
            line-height: 1.7;
            margin-bottom: 30px;
            color: #444;
            border-left: 4px solid #ddd;
            padding-left: 20px;
        }}
        .key-sentence {{
            background-color: #f5f5f5;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
            font-size: 17px;
            font-weight: 300;
            color: #333;
        }}
        .formula {{
            background-color: #eef;
            padding: 10px;
            text-align: center;
            border-radius: 5px;
            margin: 20px 0;
            overflow-x: auto;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 14px;
            color: #999;
        }}
        .share-buttons {{
            display: flex;
            justify-content: center;
            margin: 30px 0;
        }}
        .share-button {{
            display: inline-block;
            padding: 10px 15px;
            background-color: #4267B2;
            color: white;
            border-radius: 4px;
            margin: 0 10px;
            text-decoration: none;
            font-size: 14px;
        }}
        .weibo {{
            background-color: #E6162D;
        }}
        .weixin {{
            background-color: #07C160;
        }}
        .zhihu {{
            background-color: #0066FF;
        }}
        .qrcode {{
            text-align: center;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{theory_info['title']}</h1>
        <div class="dimension">维度: {theory_info['dimension']} | 宇宙本论 v{theory_info['version']}</div>
        
        <div class="abstract">
            {theory_info['abstract']}
        </div>
        
        <h2>核心洞见</h2>
"""
    
    # 添加金句
    if theory_info['key_sentences']:
        for sentence in theory_info['key_sentences']:
            html += f'        <div class="key-sentence">{sentence}</div>\n'
    
    # 添加公式
    if theory_info['formulas']:
        html += """
        <h2>数学表达</h2>
"""
        for formula in theory_info['formulas']:
            html += f'        <div class="formula">${formula}$</div>\n'
    
    # 添加分享按钮和页脚
    html += """
        <div class="share-buttons">
            <a href="#" class="share-button weibo">分享到微博</a>
            <a href="#" class="share-button weixin">分享到微信</a>
            <a href="#" class="share-button zhihu">分享到知乎</a>
        </div>
        
        <div class="qrcode">
            <p>扫描二维码，了解更多宇宙本论</p>
            <!-- 这里可以放置一个二维码图片 -->
            <div style="width:150px;height:150px;background-color:#eee;margin:0 auto;display:flex;align-items:center;justify-content:center;">
                二维码图片
            </div>
        </div>
        
        <div class="footer">
            &copy; 2023 宇宙本论 | XOR·SHIFT 理论体系 | 版权所有
        </div>
    </div>
</body>
</html>
"""
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"分享HTML页面已生成: {output_path}")

def main():
    args = parse_args()
    
    # 检查输入文件是否存在
    if not os.path.exists(args.input):
        print(f"错误: 输入文件 {args.input} 不存在")
        sys.exit(1)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 提取理论信息
    theory_info = extract_theory_info(args.input)
    if not theory_info:
        print("无法从文件中提取有效信息")
        sys.exit(1)
    
    # 获取文件名（不含扩展名）作为基础输出名
    base_name = os.path.splitext(os.path.basename(args.input))[0]
    
    # 处理所有平台还是特定平台
    platforms = ["weixin", "weibo", "zhihu", "xiaohongshu", "douyin"] if args.platform == "all" else [args.platform]
    
    # 生成分享内容
    for platform in platforms:
        # 生成文本内容
        text = generate_share_text(theory_info, platform)
        text_output = os.path.join(args.output_dir, f"{base_name}_{platform}.txt")
        with open(text_output, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"已生成{platform}平台分享文本: {text_output}")
    
    # 生成分享图片
    image_output = os.path.join(args.output_dir, f"{base_name}_share.png")
    generate_share_image(theory_info, image_output, args.template)
    
    # 生成分享HTML页面
    html_output = os.path.join(args.output_dir, f"{base_name}_share.html")
    generate_share_html(theory_info, html_output)
    
    # 生成分享工具信息摘要
    summary = {
        "title": theory_info['title'],
        "dimension": theory_info['dimension'],
        "version": theory_info['version'],
        "platforms": platforms,
        "outputs": {
            "texts": [f"{base_name}_{platform}.txt" for platform in platforms],
            "image": f"{base_name}_share.png",
            "html": f"{base_name}_share.html"
        },
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    summary_output = os.path.join(args.output_dir, f"{base_name}_share_summary.json")
    with open(summary_output, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n分享工具生成完成！所有文件已保存到 {args.output_dir} 目录")
    print(f"摘要信息: {summary_output}")

if __name__ == "__main__":
    main() 