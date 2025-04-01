import json
import matplotlib.pyplot as plt

with open('test_verification.json') as f:
    data = json.load(f)

formula_counts = []
theorem_counts = []

for theory_id, theory_verification in data['_verification'].items():
    formula_counts.append(theory_verification['formula_count'])
    theorem_counts.append(theory_verification['theorem_count'])

print(f'公式数量统计:')
print(f'  总数: {sum(formula_counts)}')
print(f'  平均每篇理论: {sum(formula_counts) / len(formula_counts):.2f}')
print(f'  最多: {max(formula_counts)}')
print(f'  最少: {min(formula_counts)}')
print(f'定理数量统计:')
print(f'  总数: {sum(theorem_counts)}')
print(f'  平均每篇理论: {sum(theorem_counts) / len(theorem_counts):.2f}')
print(f'  最多: {max(theorem_counts)}')
print(f'  最少: {min(theorem_counts)}') 

