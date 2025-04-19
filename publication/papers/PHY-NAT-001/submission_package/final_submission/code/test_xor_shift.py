#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
XOR-SHIFT操作一致性测试
为宇宙本论数据处理器验证XOR-SHIFT算法的一致性、收敛性和稳定性

This module supports the PHY-NAT-001 paper "XOR-SHIFT Operations Unifying Quantum and Relativistic Frameworks"
by providing empirical validation of the theoretical framework's core operations.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import json
from typing import Tuple, List, Dict, Any
import logging

# 添加父目录到路径以导入universe_data_processor
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from universe_data_processor import UniverseDataProcessor

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('XOR-SHIFT测试')

class XORShiftTester:
    """
    XOR-SHIFT操作测试工具类
    
    此类实现了对XOR-SHIFT操作的系统化验证，测试其在不同模式和条件下的行为特性。
    XOR-SHIFT作为宇宙本论中统一量子和相对论框架的核心操作，需要满足特定的数学性质：
    
    1. 一致性：在应用于不同类型的数据时保持预期转换特性
    2. 稳定性：在多次迭代应用时表现出可预测的动态特性
    3. 收敛性：在特定条件下趋向稳定状态
    
    这些特性对应于物理学中的基本原理：
    - 一致性反映物理规律的普适性
    - 稳定性对应于物理系统的动力学行为
    - 收敛性反映系统的平衡态和终态行为
    
    通过验证这些性质，我们可以确认XOR-SHIFT操作是否满足作为统一物理框架基础的要求。
    """
    
    def __init__(self, processor: UniverseDataProcessor = None):
        """
        初始化XOR-SHIFT测试器
        
        Args:
            processor: 宇宙本论数据处理器实例，如不提供则自动创建
        """
        self.processor = processor or UniverseDataProcessor()
        self.test_results = {}
        logger.info("XOR-SHIFT测试器初始化完成")
        
    def generate_test_patterns(self, pattern_type: str = 'all', n_samples: int = 200) -> Dict[str, np.ndarray]:
        """
        生成测试模式
        
        这些模式代表不同类型的物理系统：
        - 周期模式：对应于量子系统中的波函数和经典系统中的周期运动
        - 混沌模式：对应于非线性动力学系统和复杂的量子多体系统
        - 分形模式：对应于自相似物理结构和标度不变系统
        
        测试这些模式可验证XOR-SHIFT在不同物理系统表现形式下的适用性。
        
        Args:
            pattern_type: 测试模式类型 ('periodic', 'chaotic', 'fractal', 'all')
            n_samples: 样本数量
            
        Returns:
            测试模式字典
        """
        logger.info(f"生成{pattern_type}类型测试模式，样本数={n_samples}")
        patterns = {}
        
        t = np.linspace(0, 10, n_samples)
        
        if pattern_type in ['periodic', 'all']:
            # 周期模式 - 对应量子波函数和经典振荡系统
            patterns['sine'] = np.sin(t)
            patterns['cosine'] = np.cos(t)
            patterns['square'] = np.sign(np.sin(2*t))
            patterns['sawtooth'] = (t % 1) * 2 - 1
            
        if pattern_type in ['chaotic', 'all']:
            # 混沌模式 - 对应非线性物理系统
            logistic = np.zeros(n_samples)
            logistic[0] = 0.5
            r = 3.9  # 混沌区域的r值
            for i in range(1, n_samples):
                logistic[i] = r * logistic[i-1] * (1 - logistic[i-1])
            patterns['logistic'] = logistic
            
            # Lorenz吸引子（简化版）- 对应复杂流体系统
            lorenz = np.zeros(n_samples)
            lorenz[0] = 0.1
            for i in range(1, n_samples):
                lorenz[i] = lorenz[i-1] + 0.01 * (10 * (0.1 - lorenz[i-1]))
                if i % 10 == 0:
                    lorenz[i] += 0.1 * np.random.random()
            patterns['lorenz'] = lorenz
            
        if pattern_type in ['fractal', 'all']:
            # 分形模式 - 对应自相似物理结构
            cantor = np.ones(n_samples)
            step = n_samples
            while step > 1:
                step = step // 3
                for i in range(step, n_samples, step*3):
                    cantor[i:i+step] = 0
            patterns['cantor'] = cantor
            
            # 布朗运动 - 对应热力学随机过程
            brownian = np.zeros(n_samples)
            for i in range(1, n_samples):
                brownian[i] = brownian[i-1] + np.random.normal(0, 0.01)
            patterns['brownian'] = brownian
            
        return patterns
    
    def test_xor_shift_consistency(self, shift_factors: List[float] = None) -> Dict[str, Any]:
        """
        测试XOR-SHIFT操作的一致性
        
        一致性测试检验XOR-SHIFT在不同参数值下是否保持其基本特性。
        在量子-相对论统一理论中，这对应于物理规律在不同参考系下的不变性。
        
        特别关注shift_factor=0.618（黄金分割率）时的行为，该值在理论上
        提供信息保存与变换之间的最优平衡，类似于物理中的最小作用原理。
        
        Args:
            shift_factors: 要测试的XOR位移因子列表
            
        Returns:
            测试结果字典
        """
        if shift_factors is None:
            shift_factors = [0.1, 0.33, 0.5, 0.618, 0.75, 0.9]
            
        logger.info(f"开始XOR-SHIFT一致性测试，测试因子: {shift_factors}")
        
        # 生成测试模式
        patterns = self.generate_test_patterns()
        
        results = {
            'shift_factors': shift_factors,
            'pattern_results': {},
            'consistency_scores': {},
            'overall_consistency': {}
        }
        
        for pattern_name, pattern_data in patterns.items():
            pattern_results = []
            
            # 对每个位移因子应用XOR-SHIFT
            for factor in shift_factors:
                shifted_data = self.processor.apply_xor_shift(pattern_data, factor)
                
                # 计算自相关性
                autocorr = np.correlate(shifted_data, shifted_data, mode='full')
                autocorr = autocorr[len(autocorr)//2:] / autocorr[len(autocorr)//2]
                
                # 计算噪声度（一阶差分的标准差）
                noise_level = np.std(np.diff(shifted_data))
                
                # 计算不变性分数（原始数据与变换数据的相关性）
                invariance = np.corrcoef(pattern_data, shifted_data)[0, 1]
                
                pattern_results.append({
                    'shift_factor': factor,
                    'autocorrelation': float(autocorr[1]),
                    'noise_level': float(noise_level),
                    'invariance': float(invariance)
                })
            
            results['pattern_results'][pattern_name] = pattern_results
            
            # 计算各模式的一致性得分
            consistency = np.mean([r['invariance'] for r in pattern_results])
            results['consistency_scores'][pattern_name] = float(consistency)
        
        # 计算总体一致性
        for factor in shift_factors:
            factor_results = []
            for pattern in patterns.keys():
                pattern_factor_result = next(r for r in results['pattern_results'][pattern] 
                                           if r['shift_factor'] == factor)
                factor_results.append(pattern_factor_result['invariance'])
            
            results['overall_consistency'][factor] = float(np.mean(factor_results))
        
        # 保存结果
        self.test_results['consistency'] = results
        logger.info("XOR-SHIFT一致性测试完成")
        
        return results
    
    def test_xor_shift_stability(self, iterations: int = 10, shift_factor: float = 0.618) -> Dict[str, Any]:
        """
        测试XOR-SHIFT操作的稳定性（多次应用）
        
        稳定性测试检验XOR-SHIFT在迭代应用时的行为特性。
        在物理上，这对应于信息随时间演化的动力学行为，
        类似于量子系统随时间的演化或经典系统的轨迹。
        
        默认使用黄金分割率0.618作为shift_factor，测试在该特殊值下
        系统是否表现出最佳的稳定性和信息保存特性。
        
        Args:
            iterations: 迭代应用次数
            shift_factor: XOR位移因子
            
        Returns:
            测试结果字典
        """
        logger.info(f"开始XOR-SHIFT稳定性测试，迭代次数: {iterations}, 位移因子: {shift_factor}")
        
        # 生成测试模式
        patterns = self.generate_test_patterns(pattern_type='all', n_samples=100)
        
        results = {
            'iterations': iterations,
            'shift_factor': shift_factor,
            'pattern_results': {}
        }
        
        for pattern_name, pattern_data in patterns.items():
            # 初始化
            current_data = pattern_data.copy()
            pattern_results = []
            
            # 迭代应用XOR-SHIFT
            for i in range(iterations):
                current_data = self.processor.apply_xor_shift(current_data, shift_factor)
                
                # 计算与原始数据的差异
                deviation = np.mean(np.abs(current_data - pattern_data))
                
                # 计算熵值
                hist, _ = np.histogram(current_data, bins=10, density=True)
                entropy = -np.sum(hist * np.log2(hist + 1e-10))
                
                pattern_results.append({
                    'iteration': i + 1,
                    'deviation': float(deviation),
                    'entropy': float(entropy),
                    'mean': float(np.mean(current_data)),
                    'std': float(np.std(current_data))
                })
            
            results['pattern_results'][pattern_name] = pattern_results
        
        # 保存结果
        self.test_results['stability'] = results
        logger.info("XOR-SHIFT稳定性测试完成")
        
        return results
    
    def test_xor_shift_convergence(self, shift_factor: float = 0.618, threshold: float = 0.001) -> Dict[str, Any]:
        """
        测试XOR-SHIFT操作的收敛性
        
        收敛性测试检验系统在重复应用XOR-SHIFT后是否达到稳定状态。
        在物理学中，这对应于系统达到平衡或稳定态的趋势，
        类似于热力学系统的平衡态或量子系统的基态。
        
        特别关注在shift_factor=0.618时的收敛行为，该值理论上应提供
        最优的收敛特性，对应于物理系统趋向最小能量状态的原理。
        
        Args:
            shift_factor: XOR位移因子
            threshold: 收敛阈值
            
        Returns:
            测试结果字典
        """
        logger.info(f"开始XOR-SHIFT收敛性测试，位移因子: {shift_factor}, 阈值: {threshold}")
        
        # 生成测试模式
        patterns = self.generate_test_patterns(pattern_type='chaotic', n_samples=100)
        
        results = {
            'shift_factor': shift_factor,
            'threshold': threshold,
            'pattern_results': {}
        }
        
        for pattern_name, pattern_data in patterns.items():
            current_data = pattern_data.copy()
            iterations = 0
            converged = False
            convergence_data = []
            
            # 迭代直到收敛
            while iterations < 100 and not converged:  # 最多100次迭代
                prev_data = current_data.copy()
                current_data = self.processor.apply_xor_shift(current_data, shift_factor)
                iterations += 1
                
                # 计算变化量
                delta = np.mean(np.abs(current_data - prev_data))
                convergence_data.append(float(delta))
                
                # 检查是否收敛
                if delta < threshold:
                    converged = True
            
            results['pattern_results'][pattern_name] = {
                'converged': converged,
                'iterations': iterations,
                'convergence_deltas': convergence_data
            }
        
        # 保存结果
        self.test_results['convergence'] = results
        logger.info("XOR-SHIFT收敛性测试完成")
        
        return results
    
    def visualize_consistency_results(self, save_path: str = None) -> plt.Figure:
        """
        可视化一致性测试结果
        
        Args:
            save_path: 保存图片的路径
            
        Returns:
            matplotlib图形对象
        """
        if 'consistency' not in self.test_results:
            raise ValueError("请先运行一致性测试")
        
        results = self.test_results['consistency']
        shift_factors = results['shift_factors']
        patterns = list(results['pattern_results'].keys())
        
        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('XOR-SHIFT操作一致性测试结果', fontsize=16)
        
        # 1. 绘制不同模式的一致性得分
        ax1 = axes[0, 0]
        consistency_scores = [results['consistency_scores'][p] for p in patterns]
        ax1.bar(patterns, consistency_scores)
        ax1.set_title('各模式一致性得分')
        ax1.set_ylabel('一致性分数')
        ax1.set_xticklabels(patterns, rotation=45)
        
        # 2. 绘制不同位移因子的总体一致性
        ax2 = axes[0, 1]
        factor_scores = [results['overall_consistency'][str(f)] for f in shift_factors]
        ax2.plot(shift_factors, factor_scores, 'o-', linewidth=2)
        ax2.set_title('各位移因子总体一致性')
        ax2.set_xlabel('位移因子')
        ax2.set_ylabel('总体一致性')
        
        # 3. 绘制不变性热力图
        ax3 = axes[1, 0]
        invariance_data = np.zeros((len(patterns), len(shift_factors)))
        for i, pattern in enumerate(patterns):
            for j, factor in enumerate(shift_factors):
                result = next(r for r in results['pattern_results'][pattern] 
                            if r['shift_factor'] == factor)
                invariance_data[i, j] = result['invariance']
        
        im = ax3.imshow(invariance_data, cmap='viridis')
        ax3.set_title('不变性热力图')
        ax3.set_xlabel('位移因子')
        ax3.set_ylabel('模式')
        ax3.set_xticks(np.arange(len(shift_factors)))
        ax3.set_yticks(np.arange(len(patterns)))
        ax3.set_xticklabels(shift_factors)
        ax3.set_yticklabels(patterns)
        fig.colorbar(im, ax=ax3)
        
        # 4. 绘制噪声水平对比
        ax4 = axes[1, 1]
        for pattern in patterns[:4]:  # 只显示前4个模式以避免拥挤
            noise_levels = [r['noise_level'] for r in results['pattern_results'][pattern]]
            ax4.plot(shift_factors, noise_levels, 'o-', label=pattern)
        ax4.set_title('位移因子对噪声水平的影响')
        ax4.set_xlabel('位移因子')
        ax4.set_ylabel('噪声水平')
        ax4.legend()
        
        plt.tight_layout()
        
        # 保存图表
        if save_path:
            plt.savefig(save_path, dpi=100)
            logger.info(f"一致性测试可视化结果已保存至: {save_path}")
        
        return fig
    
    def visualize_stability_results(self, save_path: str = None) -> plt.Figure:
        """
        可视化稳定性测试结果
        
        Args:
            save_path: 保存图片的路径
            
        Returns:
            matplotlib图形对象
        """
        if 'stability' not in self.test_results:
            raise ValueError("请先运行稳定性测试")
        
        results = self.test_results['stability']
        iterations = range(1, results['iterations'] + 1)
        patterns = list(results['pattern_results'].keys())
        
        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'XOR-SHIFT操作稳定性测试结果 (位移因子: {results["shift_factor"]})', fontsize=16)
        
        # 1. 绘制偏差变化
        ax1 = axes[0, 0]
        for pattern in patterns[:4]:  # 只显示前4个模式以避免拥挤
            deviations = [r['deviation'] for r in results['pattern_results'][pattern]]
            ax1.plot(iterations, deviations, 'o-', label=pattern)
        ax1.set_title('迭代过程中的偏差变化')
        ax1.set_xlabel('迭代次数')
        ax1.set_ylabel('与原始数据的偏差')
        ax1.legend()
        
        # 2. 绘制熵值变化
        ax2 = axes[0, 1]
        for pattern in patterns[:4]:
            entropies = [r['entropy'] for r in results['pattern_results'][pattern]]
            ax2.plot(iterations, entropies, 'o-', label=pattern)
        ax2.set_title('迭代过程中的熵值变化')
        ax2.set_xlabel('迭代次数')
        ax2.set_ylabel('熵值')
        ax2.legend()
        
        # 3. 绘制均值变化
        ax3 = axes[1, 0]
        for pattern in patterns[:4]:
            means = [r['mean'] for r in results['pattern_results'][pattern]]
            ax3.plot(iterations, means, 'o-', label=pattern)
        ax3.set_title('迭代过程中的均值变化')
        ax3.set_xlabel('迭代次数')
        ax3.set_ylabel('均值')
        ax3.legend()
        
        # 4. 绘制标准差变化
        ax4 = axes[1, 1]
        for pattern in patterns[:4]:
            stds = [r['std'] for r in results['pattern_results'][pattern]]
            ax4.plot(iterations, stds, 'o-', label=pattern)
        ax4.set_title('迭代过程中的标准差变化')
        ax4.set_xlabel('迭代次数')
        ax4.set_ylabel('标准差')
        ax4.legend()
        
        plt.tight_layout()
        
        # 保存图表
        if save_path:
            plt.savefig(save_path, dpi=100)
            logger.info(f"稳定性测试可视化结果已保存至: {save_path}")
        
        return fig
    
    def visualize_convergence_results(self, save_path: str = None) -> plt.Figure:
        """
        可视化收敛性测试结果
        
        Args:
            save_path: 保存图片的路径
            
        Returns:
            matplotlib图形对象
        """
        if 'convergence' not in self.test_results:
            raise ValueError("请先运行收敛性测试")
        
        results = self.test_results['convergence']
        patterns = list(results['pattern_results'].keys())
        
        # 创建图表
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle(f'XOR-SHIFT操作收敛性测试结果 (位移因子: {results["shift_factor"]})', fontsize=16)
        
        # 1. 绘制收敛过程
        ax1 = axes[0]
        for pattern in patterns:
            deltas = results['pattern_results'][pattern]['convergence_deltas']
            iterations = range(1, len(deltas) + 1)
            ax1.semilogy(iterations, deltas, 'o-', label=pattern)
        ax1.axhline(y=results['threshold'], linestyle='--', color='r', label='收敛阈值')
        ax1.set_title('收敛过程')
        ax1.set_xlabel('迭代次数')
        ax1.set_ylabel('变化量 (对数尺度)')
        ax1.legend()
        
        # 2. 绘制收敛情况对比
        ax2 = axes[1]
        iterations_to_converge = []
        converged_status = []
        for pattern in patterns:
            pattern_result = results['pattern_results'][pattern]
            iterations_to_converge.append(pattern_result['iterations'])
            converged_status.append(pattern_result['converged'])
        
        # 使用不同颜色区分是否收敛
        colors = ['g' if converged else 'r' for converged in converged_status]
        ax2.bar(patterns, iterations_to_converge, color=colors)
        ax2.set_title('收敛所需迭代次数')
        ax2.set_ylabel('迭代次数')
        ax2.set_xticklabels(patterns, rotation=45)
        
        # 添加收敛状态标注
        for i, (iterations, converged) in enumerate(zip(iterations_to_converge, converged_status)):
            status = '已收敛' if converged else '未收敛'
            ax2.text(i, iterations + 1, status, ha='center')
        
        plt.tight_layout()
        
        # 保存图表
        if save_path:
            plt.savefig(save_path, dpi=100)
            logger.info(f"收敛性测试可视化结果已保存至: {save_path}")
        
        return fig
    
    def export_test_results(self, output_path: str) -> None:
        """
        导出所有测试结果
        
        Args:
            output_path: 输出文件路径
        """
        if not self.test_results:
            raise ValueError("没有可导出的测试结果")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"测试结果已导出至: {output_path}")
    
    def run_all_tests(self, output_dir: str = '.') -> None:
        """
        运行所有测试并保存结果
        
        这个综合测试套件提供了XOR-SHIFT操作作为统一物理框架的实证验证。
        通过验证其一致性、稳定性和收敛性，我们确认XOR-SHIFT满足
        作为量子和相对论框架统一基础的必要数学特性。
        
        Args:
            output_dir: 输出目录
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        logger.info("开始运行所有XOR-SHIFT测试...")
        
        # 运行一致性测试
        self.test_xor_shift_consistency()
        self.visualize_consistency_results(os.path.join(output_dir, 'xor_shift_consistency.png'))
        
        # 运行稳定性测试
        self.test_xor_shift_stability()
        self.visualize_stability_results(os.path.join(output_dir, 'xor_shift_stability.png'))
        
        # 运行收敛性测试
        self.test_xor_shift_convergence()
        self.visualize_convergence_results(os.path.join(output_dir, 'xor_shift_convergence.png'))
        
        # 导出结果
        self.export_test_results(os.path.join(output_dir, 'xor_shift_test_results.json'))
        
        logger.info(f"所有测试完成，结果已保存至: {output_dir}")
        

if __name__ == "__main__":
    print("XOR-SHIFT操作一致性测试工具")
    print("-" * 50)
    
    # 创建数据处理器
    processor = UniverseDataProcessor()
    
    # 创建测试器
    tester = XORShiftTester(processor)
    
    # 运行所有测试
    output_dir = os.path.join(current_dir, 'xor_shift_test_results')
    tester.run_all_tests(output_dir)
    
    print(f"\n测试完成! 结果已保存至: {output_dir}") 