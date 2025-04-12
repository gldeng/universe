# 宇宙本论工具集

本目录包含用于处理和管理宇宙本论形式化理论文档的工具脚本。

## 工具列表

### 主要工具

- **universe_automation.py** - 宇宙本论项目自动化工作流
  ```
  python universe_automation.py --all
  ```

- **theory_to_json.py** - 将形式化理论文档转换为结构化JSON数据
  ```
  python theory_to_json.py --dir ../formal_theory --output formal_theories.json --verification
  ```

- **theory_generator.py** - 从宇宙本论自动推导出其他维度的理论
  ```
  python theory_generator.py --ontology ../formal_theory/formal_theory_cosmic_ontology.md --output generated_theories --dimension 15 --english
  ```

- **generate_maintenance_report.py** - 生成理论体系维护报告
  ```
  python generate_maintenance_report.py --output maintenance_report.md
  ```

- **generate_theory_graph.py** - 生成理论依赖关系图
  ```
  python generate_theory_graph.py --output theory_graph.html --format html
  ```

- **share_tool_generator.py** - 生成社交媒体分享工具
  ```
  python share_tool_generator.py --input ../formal_theory/formal_theory_xxx.md --platform weixin
  ```

### 辅助工具

- **check_md_links.py** - 检查文档中的Markdown链接是否有效
- **check_updates.py** - 检查文档更新情况
- **check_unindexed_files.py** - 检查未被索引的文件并生成报告
  ```
  python check_unindexed_files.py --dir ../formal_theory --output unindexed_files.json
  ```
- **math_expr_converter.py** - 转换数学表达式格式
- **fix_math.py** - 修复数学表达式语法
- **update_dimensions.py** - 更新理论维度标记
- **verify_ordering.py** - 验证理论的维度排序
- **reorder_theories.py** - 重新排序理论文档
- **test_dimension_extract.py** - 测试维度提取功能
- **generate_theory_json.py** - 从形式化理论生成JSON数据
- **fix_critical_links.py** - 修复中英文文档之间的链接

## theory_to_json.py 使用说明

### 功能特点

- 解析所有 `formal_theory_*.md` 文件（排除英文版本的 `*_en.md` 文件）
- 提取理论的元数据（标题、维度、版本等）
- 解析文档结构（章节、子章节）
- 提取数学公式、定理和证明
- 识别理论之间的引用关系
- 生成理论依赖关系图
- 提供验证数据（检查维度一致性、引用有效性等）

### 基本用法

```bash
python theory_to_json.py
```

### 高级选项

```bash
python theory_to_json.py --dir <理论文件目录> --output <输出JSON文件> --verification
```

参数说明：
- `--dir`：指定理论文件所在的目录，默认为 `formal_theory`
- `--output`：指定输出 JSON 文件的路径，默认为 `formal_theories.json`
- `--verification`：包含验证数据，用于检查理论的完整性和一致性

### 输出数据结构

生成的 JSON 文件包含以下主要结构：

```json
{
  "formal_theory_xxx": {
    "filename": "formal_theory_xxx",
    "title": "理论标题",
    "metadata": {
      "version": "版本号",
      "dimension": "维度",
      "title": "完整标题"
    },
    "sections": {
      "章节名": {
        "content": "章节内容",
        "subsections": {
          "子章节名": {
            "content": "子章节内容",
            "formulas": ["公式1", "公式2", ...],
            "theorems": ["定理1", "定理2", ...],
            "proofs": ["证明1", "证明2", ...]
          }
        },
        "formulas": ["公式1", "公式2", ...],
        "theorems": ["定理1", "定理2", ...],
        "proofs": ["证明1", "证明2", ...]
      }
    },
    "references": {
      "引用名": "引用链接"
    },
    "reference_dimensions": {
      "理论名": "维度"
    },
    "english_version": "formal_theory_xxx_en.md"
  },
  "_meta": {
    "dependencies": {
      "formal_theory_xxx": ["依赖的理论1", "依赖的理论2", ...]
    },
    "dimensions": {
      "formal_theory_xxx": "维度"
    },
    "theory_count": 数量
  },
  "_verification": {
    "formal_theory_xxx": {
      "formula_count": 公式数量,
      "theorem_count": 定理数量,
      "dimension_consistent": true/false,
      "reference_validity": true/false,
      "formal_verification": {
        "is_complete": true/false,
        "has_proofs": true/false
      }
    }
  }
}
```

### 应用场景

1. **AI辅助理论完善**：AI系统可以通过分析JSON数据，发现理论中的漏洞或不一致之处
2. **理论关系可视化**：基于依赖数据创建理论关系图
3. **自动生成理论内容**：根据现有理论结构自动生成或扩展理论
4. **理论验证**：检查理论的形式化完整性和一致性
5. **跨语言理论同步**：确保中英文版本的理论内容一致

## generate_maintenance_report.py 使用说明

### 功能特点

- 统计理论文件数量和维度分布
- 检查未被索引的文件
- 检查链接完整性
- 检查中英文文件同步情况
- 检查版本一致性
- 生成维护建议

### 基本用法

```bash
python generate_maintenance_report.py
```

### 高级选项

```bash
python generate_maintenance_report.py --theory_dir <理论文件目录> --output <输出报告文件> --index <中文索引文件> --index_en <英文索引文件>
```

参数说明：
- `--theory_dir`：理论文件目录，默认为 `../formal_theory`
- `--output`：输出报告文件名，默认为 `maintenance_report.md`
- `--index`：中文索引文件，默认为 `../formal_theory.md`
- `--index_en`：英文索引文件，默认为 `../formal_theory_en.md`

### 报告内容

生成的维护报告包含以下主要内容：

1. **统计信息**：文件数量、中英文文件数、版本号等
2. **维度分布**：按维度统计理论数量
3. **版本一致性检查**：检查理论文件版本是否一致
4. **未索引文件检查**：检查未被索引的中英文文件
5. **中英文同步检查**：检查缺少对应语言版本的文件
6. **链接完整性检查**：检查损坏的链接
7. **维护建议**：基于检查结果的维护建议

## generate_theory_graph.py 使用说明

### 功能特点

- 分析理论之间的依赖关系
- 生成可视化的依赖关系图
- 支持多种输出格式：DOT、PNG和HTML
- 提供交互式HTML图表，支持过滤和布局调整
- 可按维度或特定理论过滤

### 基本用法

```bash
python generate_theory_graph.py
```

### 高级选项

```bash
python generate_theory_graph.py --theory_dir <理论文件目录> --output <输出文件名> --format <输出格式> --filter_dimension <维度过滤> --filter_theory <理论过滤> --layout <布局算法>
```

参数说明：
- `--theory_dir`：理论文件目录，默认为 `../formal_theory`
- `--output`：输出文件名（不含扩展名），默认为 `theory_graph`
- `--format`：输出格式，可选值为 `dot`、`png`、`html` 或 `all`，默认为 `dot`
- `--filter_dimension`：按维度过滤理论（仅包含大于等于指定维度的理论）
- `--filter_theory`：按理论名过滤（只显示与指定理论相关的理论）
- `--json_input`：使用JSON文件作为输入，而不是直接分析理论文件
- `--layout`：图布局算法，可选值为 `dot`、`neato`、`fdp`、`sfdp`、`twopi` 或 `circo`，默认为 `dot`

### HTML交互功能

生成的HTML图表提供以下交互功能：

1. **维度过滤**：按维度范围过滤显示的理论
2. **布局切换**：在力导向、放射状和层次结构布局之间切换
3. **缩放和平移**：通过鼠标操作缩放和平移视图
4. **重置视图**：一键重置视图到初始状态
5. **显示/隐藏标签**：切换显示或隐藏节点标签
6. **悬停提示**：鼠标悬停在节点上显示详细信息

## theory_generator.py 使用说明

### 功能特点

- 从宇宙本论（维度10）自动推导出其他维度的理论
- 生成符合宇宙本论框架的理论文档，遵循FLIP、XOR、SHIFT操作系统
- 根据维度自动调整理论的复杂度、公式和内容
- 生成理论之间的引用关系
- 可选生成英文版本

### 基本用法

```bash
python theory_generator.py --ontology ../formal_theory/formal_theory_cosmic_ontology.md --output generated_theories
```

### 高级选项

```bash
python theory_generator.py --ontology <宇宙本论文件路径> --output <输出目录> --dimension <维度> --english
```

参数说明：
- `--ontology`：宇宙本论文件路径，默认为 `../formal_theory/formal_theory_cosmic_ontology.md`
- `--output`：生成理论的输出目录，默认为 `generated_theories`
- `--dimension`：指定生成特定维度的理论，不指定则生成所有维度理论
- `--english`：是否同时生成英文版本

### 理论维度谱系

工具支持生成从 -3 到 ∞ 维度的理论，包括：

- **低维理论**（-3到5维）：如元前奇点理论、前奇点理论、原始奇点理论等
- **中维理论**（6到19维）：如宇宙本论、信息场理论、时空理论等
- **高维理论**（20维以上）：如宇宙维度理论、多宇宙理论、元理论等

### 生成内容特点

1. **维度相关的内容**：理论内容根据维度自动调整复杂度
2. **基于宇宙本论的操作**：所有理论都基于FLIP、XOR、SHIFT操作
3. **理论引用关系**：高维理论自动引用低维理论
4. **形式化表达**：包含公理、定理、操作定义和证明
5. **双语支持**：可同时生成中英文版本
6. **维度标记文件名**：生成的文件名包含维度标记，如 `formal_theory_逻辑多维拓扑理论_d15.md` 