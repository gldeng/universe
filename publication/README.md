# 宇宙本论出版管理系统

本目录包含与宇宙本论理论体系相关的出版计划、论文草稿、自动化跟踪系统和提交管理工具。

## 目录结构

- **publication_plan.md**: 总体出版计划与策略
- **top_papers/**: 优先发表的高影响力论文
  - `phy_nat_001_outline.md`: Nature Physics论文 (XOR-SHIFT统一框架)
  - [更多优先论文...]
- **tracking/**: 论文出版状态自动跟踪
  - `papers_status.md`: 所有论文的状态追踪表
- **status_updates/**: 各论文的自动状态更新
  - `phy_nat_001_status.md`: PHY-NAT-001论文状态
  - [更多状态更新...]
- **timeline/**: 出版时间线与自动规划
  - `phy_nat_001_timeline.md`: PHY-NAT-001提交时间线
  - [更多时间线...]
- **templates/**: 期刊格式自动模板和提交指南
- **figures/**: 跨论文共享的自动图表生成与可视化资源
- **references/**: 自动更新的参考文献库

## 当前优先论文

1. **PHY-NAT-001**: XOR-SHIFT Operations Unifying Quantum and Relativistic Frameworks
   - 目标期刊: Nature Physics
   - 当前状态: `PREP` (自动准备阶段)
   - 目标提交日期: 2025年6月15日
   - [详细状态](status_updates/phy_nat_001_status.md) | [时间线](timeline/phy_nat_001_timeline.md) | [论文草稿](top_papers/phy_nat_001_outline.md)

2. **PHY-PRL-002**: Micro-physics Verification Predictions of Universe Ontology
   - 目标期刊: Physical Review Letters
   - 当前状态: `PLAN` (计划阶段)
   - 目标提交日期: 待定

3. **PHY-SCI-003**: Information Ontology: Rewriting the Foundations of Physics
   - 目标期刊: Science
   - 当前状态: `PLAN` (计划阶段)
   - 目标提交日期: 待定

## 出版状态代码

- `PLAN`: 计划阶段 - 论文主题已确定但尚未开始写作
- `PREP`: 准备阶段 - 论文草稿自动生成中
- `SUBM`: 已提交 - 论文已自动提交至目标期刊
- `REVW`: 审稿中 - 论文正在经历同行评审
- `REVI`: 修改中 - 根据审稿人反馈进行自动修改
- `ACCP`: 已接受 - 论文已被接受但尚未发表
- `PUBL`: 已出版 - 论文已正式发表
- `REJT`: 被拒绝 - 论文被目标期刊拒绝，自动准备替代方案

## 使用指南

1. 论文草稿自动保存在`top_papers/`目录
2. 状态更新自动记录在`status_updates/`中对应的文件
3. 时间线规划自动生成在`timeline/`中对应的文件
4. 总体出版状态自动更新在`tracking/papers_status.md`中
5. 共享图表自动生成在`figures/`目录并通过相对路径引用

## 自动化工具

- [GitHub自动化工作流](https://github.com/loning/universe/projects/publications)
- [Overleaf自动集成](https://www.overleaf.com/project/universe-ontology)
- [Zotero自动文献管理](https://www.zotero.org/groups/universe-ontology)

*最后更新: 2025-04-18* 