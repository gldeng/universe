import json
import random

with open('test_verification.json') as f:
    data = json.load(f)

# 随机选取一个理论来检查其内容
theory_id = random.choice([k for k in data.keys() if not k.startswith('_')])
theory = data[theory_id]

print(f'随机选取理论: {theory_id}')
print(f'标题: {theory["title"]}')
print(f'维度: {theory["metadata"]["dimension"]}')
print(f'版本: {theory["metadata"]["version"]}')
print(f'章节数: {len(theory["sections"])}')

# 显示章节标题
print('
章节列表:')
for i, section_name in enumerate(theory["sections"].keys()):
    print(f'{i+1}. {section_name}')

# 选择一个章节查看其内容结构
if theory["sections"]:
    section_name = list(theory["sections"].keys())[0]
    section = theory["sections"][section_name]
    print(f'
第一章节 "{section_name}" 的内容:')
    print(f'  子章节数: {len(section["subsections"])}')
    print(f'  公式数: {len(section["formulas"])}')
    print(f'  定理数: {len(section["theorems"])}')
    print(f'  证明数: {len(section["proofs"])}')
    
    # 显示子章节
    if section["subsections"]:
        print('
  子章节列表:')
        for i, subsection_name in enumerate(section["subsections"].keys()):
            print(f'  {i+1}. {subsection_name}')

# 检查引用关系
print(f'
引用关系:')
if theory["references"]:
    for ref_name, ref_link in theory["references"].items():
        print(f'  {ref_name} -> {ref_link}')
else:
    print('  无引用关系')

# 检查英文版本
print(f'
英文版本: {\'有\' if theory["english_version"] else \'无\'}')

