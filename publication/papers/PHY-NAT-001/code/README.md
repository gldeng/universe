# 宇宙本论数据处理器

本项目为PHY-NAT-001论文提供支持性代码实现，用于处理、分析和可视化宇宙本论相关数据。

## 功能概述

- 支持多种格式数据加载（JSON, CSV, NumPy格式）
- 维度数据分析与处理
- XOR-SHIFT转换与计算
- 结果可视化
- 数据导出（JSON, CSV格式）

## 环境要求

- Python 3.6+
- NumPy
- Pandas
- Matplotlib

## 安装依赖

```bash
pip install numpy pandas matplotlib
```

## 使用方法

基本使用示例：

```python
from universe_data_processor import UniverseDataProcessor

# 创建处理器实例
processor = UniverseDataProcessor()

# 加载数据
processor.load_data("your_data_file.json")

# 处理数据
results = processor.process_dimensional_data()

# 可视化结果
processor.visualize_results(save_path="dimension_analysis.png")

# 导出结果
processor.export_results("analysis_results.json")
```

## 维度参数设置

可以通过`dimension_params`参数来自定义维度分析参数：

```python
custom_params = {
    'dimensions': 11,      # 总维度数
    'xor_factor': 0.33,    # XOR因子
    'resonance_threshold': 0.75  # 共振阈值
}

processor.process_dimensional_data(dimension_params=custom_params)
```

## 示例输出

数据处理后将生成以下文件：

1. `dimension_analysis.png` - 维度分析可视化图表
2. `analysis_results.json` - 分析结果JSON文件

## 注意事项

- 本工具专为宇宙本论研究设计，基于XOR-SHIFT原理进行数据转换
- 推荐使用结构化数据，确保包含维度相关信息
- 可视化结果默认使用中文标签

## 许可证

MIT 