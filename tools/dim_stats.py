import json
with open('test_verification.json') as f:
    data = json.load(f)

dimensions = {}
for k, v in data['_meta']['dimensions'].items():
    if not k.startswith('_'):
        dimensions[v] = dimensions.get(v, 0) + 1

print('维度分布:')
for dim in sorted(dimensions.keys()):
    print(f'  维度 {dim}: {dimensions[dim]} 个理论')
