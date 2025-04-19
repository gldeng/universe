#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宇宙本论数据处理器 - 用于处理、分析和可视化宇宙本论相关数据
PHY-NAT-001论文配套代码

For PHY-NAT-001 publication: XOR-SHIFT Operations Unifying Quantum and Relativistic Frameworks
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import logging
from typing import Dict, List, Union, Optional, Tuple, Any

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('UniverseDataProcessor')

class UniverseDataProcessor:
    """宇宙本论数据处理器类，提供数据加载、处理、可视化和导出功能"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化宇宙本论数据处理器
        
        Args:
            config: 可选配置参数字典
        """
        self.data = None
        self.results = None
        self.xor_cache = {}  # XOR操作缓存
        
        # 默认配置
        self.config = {
            'default_dimensions': 11,
            'xor_factor': 0.618,  # 黄金分割率，优化维度转换的信息保存与创新
            'resonance_threshold': 0.5,
            'visualization': {
                'figsize': (12, 8),
                'dpi': 100,
                'cmap': 'viridis',
                'font_size': 12
            }
        }
        
        # 更新配置
        if config:
            self.config.update(config)
            
        logger.info("宇宙本论数据处理器初始化完成")
    
    def load_data(self, file_path: str) -> None:
        """
        从文件加载数据
        
        Args:
            file_path: 数据文件路径
        
        Raises:
            FileNotFoundError: 如果文件不存在
            ValueError: 如果文件格式不支持
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                logger.info(f"从JSON文件加载数据: {file_path}")
            
            elif file_ext == '.csv':
                self.data = pd.read_csv(file_path).to_dict('records')
                logger.info(f"从CSV文件加载数据: {file_path}")
            
            elif file_ext in ['.npy', '.npz']:
                self.data = np.load(file_path, allow_pickle=True)
                if file_ext == '.npz':
                    # 将npz文件转换为字典
                    self.data = {key: self.data[key] for key in self.data.files}
                logger.info(f"从NumPy文件加载数据: {file_path}")
            
            else:
                raise ValueError(f"不支持的文件格式: {file_ext}")
            
            logger.info(f"数据加载成功，样本量: {self._get_data_size()}")
            
        except Exception as e:
            logger.error(f"加载数据时出错: {str(e)}")
            raise
    
    def _get_data_size(self) -> int:
        """获取数据大小"""
        if isinstance(self.data, list):
            return len(self.data)
        elif isinstance(self.data, dict):
            return len(next(iter(self.data.values()))) if self.data else 0
        elif isinstance(self.data, np.ndarray):
            return self.data.shape[0]
        return 0
    
    def apply_xor_shift(self, data_array: np.ndarray, shift_factor: float = None) -> np.ndarray:
        """
        应用XOR-SHIFT变换到数据上
        
        理论基础:
        XOR-SHIFT操作是宇宙本论中的核心信息转换机制，对应于量子-经典转换方程:
        Ω_C = Ω_Q ⊕ SHIFT(Ω_Q)
        
        其中⊕表示XOR操作(信息差异)，SHIFT表示信息位移操作(状态转换)。
        在数学上，XOR-SHIFT实现了非线性信息保持变换，能在维度间转换时保留关键结构特征。
        
        黄金分割率(0.618)作为默认shift_factor具有特殊意义，它在信息保存与新信息生成之间
        提供最优平衡，对应于自然界中的最优信息处理比例。
        
        计算过程实现:
        1. 标准化 - 将数据映射到[0,1]区间，创建统一信息空间
        2. 二值化 - 使用shift_factor作为阈值，创建二进制信息状态
        3. XOR操作 - 计算相邻元素间的信息差异
        4. 连续化 - 将二进制结果与原始值按shift_factor权重混合
        5. 反标准化 - 返回到原始数据空间
        
        Args:
            data_array: 输入数据数组
            shift_factor: XOR位移因子，默认使用配置中的xor_factor
            
        Returns:
            应用XOR-SHIFT后的数据数组
        """
        if shift_factor is None:
            shift_factor = self.config['xor_factor']
            
        # 计算缓存键
        cache_key = (data_array.tobytes(), shift_factor)
        if cache_key in self.xor_cache:
            return self.xor_cache[cache_key]
            
        # 确保数据是浮点型
        data_array = data_array.astype(np.float64)
        
        # 应用XOR-SHIFT变换
        # 1. 标准化到[0,1]区间
        normalized = (data_array - np.min(data_array)) / (np.max(data_array) - np.min(data_array) + 1e-10)
        
        # 2. 转换为二进制表示
        binary_threshold = shift_factor
        binary_representation = (normalized > binary_threshold).astype(np.int32)
        
        # 3. 应用XOR操作
        shifted = np.zeros_like(binary_representation)
        shifted[1:] = binary_representation[:-1]
        xor_result = binary_representation ^ shifted
        
        # 4. 转换回连续值域
        continuous_result = normalized * (1 - shift_factor) + xor_result * shift_factor
        
        # 5. 反标准化
        result = continuous_result * (np.max(data_array) - np.min(data_array)) + np.min(data_array)
        
        # 存入缓存
        self.xor_cache[cache_key] = result
        return result
    
    def calculate_dimensional_resonance(self, dimension_data: np.ndarray) -> Tuple[float, np.ndarray]:
        """
        计算维度共振度
        
        理论基础:
        维度共振是宇宙本论中描述不同维度间信息相互作用的核心概念。
        在XOR-SHIFT框架下，共振表示维度的"活跃度"和对整体结构的贡献。
        
        数学上，共振度通过计算XOR-SHIFT后数据的自相关性来量化:
        R = E[XOR(Ω, SHIFT(Ω)) · XOR(Ω, SHIFT(Ω))]
        
        其中E表示期望值运算。高共振度表示该维度在整体结构中具有显著贡献。
        
        理论上，当维度数据包含高度结构化模式时，XOR-SHIFT操作会保留这种结构并在
        自相关分析中显示较高共振度。无结构(随机)数据则显示低共振度。
        
        当维度共振度超过阈值时，该维度被视为"活跃"，表明其在当前信息状态中有重要贡献。
        
        计算过程:
        1. 应用XOR-SHIFT变换提取维度的结构信息
        2. 计算自相关函数衡量内部结构性
        3. 归一化自相关确保跨维度可比性
        4. 计算平均自相关作为维度共振得分
        5. 生成共振向量表示该维度对整体的贡献
        
        Args:
            dimension_data: 维度数据数组
            
        Returns:
            共振度得分和共振向量
        """
        # 应用XOR-SHIFT
        shifted_data = self.apply_xor_shift(dimension_data)
        
        # 计算自相关性
        autocorr = np.correlate(shifted_data, shifted_data, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        # 归一化自相关
        autocorr = autocorr / autocorr[0]
        
        # 计算共振得分 (0-1之间)
        resonance_score = np.mean(autocorr[1:])
        
        # 生成共振向量
        resonance_vector = shifted_data * resonance_score
        
        return resonance_score, resonance_vector
        
    def process_dimensional_data(self, dimension_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        处理维度数据，应用XOR-SHIFT变换并计算维度共振度
        
        Args:
            dimension_params: 维度处理参数
            
        Returns:
            处理结果字典
        """
        if self.data is None:
            raise ValueError("请先加载数据")
        
        # 合并参数
        params = {
            'dimensions': self.config['default_dimensions'],
            'xor_factor': self.config['xor_factor'],
            'resonance_threshold': self.config['resonance_threshold']
        }
        if dimension_params:
            params.update(dimension_params)
        
        logger.info(f"处理维度数据: 维度数={params['dimensions']}, XOR因子={params['xor_factor']}")
        
        # 将数据转换为numpy数组
        if isinstance(self.data, list):
            data_array = np.array(self.data)
        elif isinstance(self.data, dict):
            # 尝试转换字典数据
            first_key = next(iter(self.data.keys()))
            data_array = np.array(self.data[first_key])
        else:
            data_array = self.data
            
        # 确保数据是2D数组
        if data_array.ndim == 1:
            data_array = data_array.reshape(-1, 1)
            
        # 根据维度要求调整数据
        n_samples, n_features = data_array.shape
        target_dimensions = params['dimensions']
        
        if n_features < target_dimensions:
            # 需要扩展维度
            expanded_data = np.zeros((n_samples, target_dimensions))
            expanded_data[:, :n_features] = data_array
            
            # 使用XOR-SHIFT生成其余维度
            for dim in range(n_features, target_dimensions):
                src_dim = (dim - n_features) % n_features
                expanded_data[:, dim] = self.apply_xor_shift(expanded_data[:, src_dim], 
                                                            params['xor_factor'] + dim*0.01)
            data_array = expanded_data
        elif n_features > target_dimensions:
            # 需要减少维度
            data_array = data_array[:, :target_dimensions]
            
        # 计算每个维度的共振度
        dimension_resonance = {}
        composite_resonance = np.zeros(n_samples)
        
        for dim in range(data_array.shape[1]):
            dim_name = f"维度_{dim+1}"
            res_score, res_vector = self.calculate_dimensional_resonance(data_array[:, dim])
            dimension_resonance[dim_name] = {
                'resonance_score': float(res_score),
                'active': res_score > params['resonance_threshold'],
                'values': res_vector.tolist()
            }
            composite_resonance += res_vector
            
        # 计算整体共振
        total_resonance = np.mean([d['resonance_score'] for d in dimension_resonance.values()])
        
        # 存储结果
        self.results = {
            'dimension_resonance': dimension_resonance,
            'total_resonance': float(total_resonance),
            'composite_resonance': composite_resonance.tolist(),
            'parameters': params,
            'sample_count': n_samples
        }
        
        logger.info(f"维度数据处理完成: 总共振度={total_resonance:.4f}")
        return self.results
    
    def visualize_results(self, save_path: str = None, show_plot: bool = True) -> plt.Figure:
        """
        可视化分析结果
        
        Args:
            save_path: 保存图片的路径，如不提供则不保存
            show_plot: 是否显示图表
            
        Returns:
            matplotlib图形对象
        """
        if self.results is None:
            raise ValueError("请先处理数据")
        
        # 设置中文字体
        try:
            font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
        except:
            font = None
            logger.warning("找不到中文字体，将使用默认字体")
        
        # 创建图表
        vis_config = self.config['visualization']
        fig, axes = plt.subplots(2, 1, figsize=vis_config['figsize'], dpi=vis_config['dpi'])
        
        # 绘制维度共振图
        dimension_names = list(self.results['dimension_resonance'].keys())
        resonance_scores = [d['resonance_score'] for d in self.results['dimension_resonance'].values()]
        active_status = [d['active'] for d in self.results['dimension_resonance'].values()]
        
        # 使用不同颜色区分活跃维度
        colors = ['#3498db' if active else '#95a5a6' for active in active_status]
        
        axes[0].bar(dimension_names, resonance_scores, color=colors)
        axes[0].axhline(y=self.results['parameters']['resonance_threshold'], 
                       linestyle='--', color='#e74c3c', label='共振阈值')
        axes[0].set_ylabel('共振度', fontproperties=font)
        axes[0].set_title('维度共振分析', fontproperties=font)
        axes[0].set_ylim(0, 1)
        axes[0].legend(prop=font)
        
        # 绘制聚合共振图
        x_indices = np.arange(min(100, len(self.results['composite_resonance'])))
        composite_data = np.array(self.results['composite_resonance'])[:len(x_indices)]
        
        axes[1].plot(x_indices, composite_data, '-', color='#2ecc71', linewidth=2)
        axes[1].fill_between(x_indices, 0, composite_data, color='#2ecc71', alpha=0.3)
        axes[1].set_xlabel('样本索引', fontproperties=font)
        axes[1].set_ylabel('综合共振强度', fontproperties=font)
        axes[1].set_title(f'综合共振模式 (总共振度: {self.results["total_resonance"]:.4f})', fontproperties=font)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图片
        if save_path:
            plt.savefig(save_path)
            logger.info(f"可视化结果已保存至: {save_path}")
        
        # 显示图表
        if show_plot:
            plt.show()
        
        return fig
    
    def export_results(self, output_path: str, format: str = None) -> None:
        """
        导出分析结果
        
        Args:
            output_path: 输出文件路径
            format: 输出格式，支持'json'和'csv'，默认根据文件扩展名判断
        """
        if self.results is None:
            raise ValueError("请先处理数据")
        
        if format is None:
            format = os.path.splitext(output_path)[1].lower().replace('.', '')
        
        if format == 'json' or output_path.endswith('.json'):
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            logger.info(f"结果已导出至JSON文件: {output_path}")
            
        elif format == 'csv' or output_path.endswith('.csv'):
            # 将嵌套字典扁平化为DataFrame
            flat_data = {}
            for dim, data in self.results['dimension_resonance'].items():
                flat_data[f"{dim}_共振度"] = data['resonance_score']
                flat_data[f"{dim}_活跃状态"] = data['active']
            
            flat_data['总共振度'] = self.results['total_resonance']
            
            df = pd.DataFrame([flat_data])
            df.to_csv(output_path, index=False, encoding='utf-8')
            logger.info(f"结果已导出至CSV文件: {output_path}")
            
        else:
            raise ValueError(f"不支持的导出格式: {format}")
    
    def generate_sample_data(self, n_samples: int = 100, n_dimensions: int = 5, 
                           noise_level: float = 0.1, save_path: str = None) -> np.ndarray:
        """
        生成示例数据用于测试
        
        Args:
            n_samples: 样本数量
            n_dimensions: 维度数量
            noise_level: 噪声水平
            save_path: 保存路径，如不提供则不保存
            
        Returns:
            生成的示例数据
        """
        logger.info(f"生成示例数据: {n_samples}个样本, {n_dimensions}个维度")
        
        # 基础模式生成
        t = np.linspace(0, 4*np.pi, n_samples)
        data = np.zeros((n_samples, n_dimensions))
        
        # 为每个维度生成不同的周期性模式
        for i in range(n_dimensions):
            freq = 0.5 + i * 0.5  # 不同频率
            phase = i * np.pi / n_dimensions  # 不同相位
            
            if i % 3 == 0:
                # 正弦模式
                data[:, i] = np.sin(freq * t + phase)
            elif i % 3 == 1:
                # 指数模式
                data[:, i] = np.tanh(np.sin(freq * t + phase))
            else:
                # 组合模式
                data[:, i] = np.sin(freq * t + phase) * np.cos(freq/2 * t)
        
        # 添加随机噪声
        if noise_level > 0:
            noise = np.random.normal(0, noise_level, data.shape)
            data += noise
        
        # 保存数据
        if save_path:
            file_ext = os.path.splitext(save_path)[1].lower()
            
            if file_ext == '.json':
                # 将数组转换为字典格式
                data_dict = {f'维度_{i+1}': data[:, i].tolist() for i in range(n_dimensions)}
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(data_dict, f, ensure_ascii=False, indent=2)
            
            elif file_ext == '.csv':
                df = pd.DataFrame(data, columns=[f'维度_{i+1}' for i in range(n_dimensions)])
                df.to_csv(save_path, index=False, encoding='utf-8')
            
            elif file_ext in ['.npy', '.npz']:
                if file_ext == '.npy':
                    np.save(save_path, data)
                else:
                    data_dict = {f'维度_{i+1}': data[:, i] for i in range(n_dimensions)}
                    np.savez(save_path, **data_dict)
            
            else:
                logger.warning(f"不支持的文件格式: {file_ext}，数据未保存")
            
            logger.info(f"示例数据已保存至: {save_path}")
        
        self.data = data
        return data
            

# 当作为脚本运行时的示例用法
if __name__ == "__main__":
    print("宇宙本论数据处理器示例")
    print("-" * 50)
    
    # 创建处理器实例
    processor = UniverseDataProcessor()
    
    # 生成示例数据
    sample_data_path = "sample_universe_data.json"
    processor.generate_sample_data(n_samples=200, n_dimensions=7, save_path=sample_data_path)
    
    # 加载数据 (可以跳过上面的步骤，直接加载现有数据)
    processor.load_data(sample_data_path)
    
    # 设置参数并处理数据
    dimension_params = {
        'dimensions': 11,         # 目标维度数
        'xor_factor': 0.33,       # XOR位移因子
        'resonance_threshold': 0.5 # 共振阈值
    }
    results = processor.process_dimensional_data(dimension_params)
    
    # 打印部分结果
    print(f"\n分析结果摘要:")
    print(f"总共振度: {results['total_resonance']:.4f}")
    print(f"活跃维度: {sum(d['active'] for d in results['dimension_resonance'].values())}/{len(results['dimension_resonance'])}")
    
    # 可视化结果
    processor.visualize_results(save_path="dimension_analysis.png")
    
    # 导出结果
    processor.export_results("analysis_results.json")
    
    print("\n数据处理完成!") 