import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from typing import Dict, List, Tuple, Set
import math
import matplotlib
from matplotlib.widgets import Button

# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei']  # 优先使用这些字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['font.family'] = 'sans-serif'
# 使用 fc-list : lang=zh 命令可以查看系统中可用的中文字体

# 确认当前环境是否有可用的中文字体
available_fonts = [f.name for f in matplotlib.font_manager.fontManager.ttflist]
has_chinese_font = False
for font in plt.rcParams['font.sans-serif']:
    if font in available_fonts:
        has_chinese_font = True
        print(f"使用中文字体: {font}")
        break

if not has_chinese_font:
    print("警告: 未找到支持中文的字体，图表中的中文可能无法正确显示")
    print("可用字体列表：", available_fonts[:5], "等")

class QuantumDomain:
    """量子域 (Ω_Q) - 无限可能性的空间"""
    
    def __init__(self, size: int = 100):
        """
        初始化量子域
        
        Args:
            size: 量子域大小
        """
        self.size = size
        # 量子态表示为概率振幅 - 使用整型表示，相位角度值×1000存储
        self.quantum_states = np.zeros((size, size), dtype=int)
        # 初始化为最大叠加态
        for i in range(size):
            for j in range(size):
                # 将2π×1000映射到整数范围
                phase = random.randint(0, 6283)  # 0到2π×1000
                # 保存相位值（整数）而非复数
                self.quantum_states[i, j] = phase
        # 归一化（在整型环境中，我们保持值的总和为固定常数）
        self.normalize()
        
    def normalize(self):
        """归一化量子态（整型实现）"""
        # 在整型实现中，我们确保总概率为固定值
        # 这里我们保持量子态的相位值不变，但记录总数以便计算概率
        self.total_norm = np.sum(np.ones_like(self.quantum_states))
            
    def apply_quantum_operation(self):
        """应用量子演化算子"""
        # 随机相位变化模拟量子演化，使用整型
        for i in range(self.size):
            for j in range(self.size):
                # 相位变化范围是0到π/10×1000
                phase_change = random.randint(0, 314)  # π/10×1000
                # 更新相位，保持在0-6283范围内
                self.quantum_states[i, j] = (self.quantum_states[i, j] + phase_change) % 6284
        # 整型实现中归一化不改变相位
        self.normalize()
    
    def get_probability_distribution(self) -> np.ndarray:
        """获取概率分布"""
        # 在整型实现中，我们通过相位值计算概率
        # 将相位转换为概率（简化模型，使用余弦作为概率分布）
        probs = np.zeros((self.size, self.size), dtype=int)
        for i in range(self.size):
            for j in range(self.size):
                # 使用相位的余弦值+1来确保概率为正
                # 映射到0-1000范围内的整数
                phase_rad = self.quantum_states[i, j] / 1000.0
                prob_value = int((np.cos(phase_rad) + 1.0) * 500)
                probs[i, j] = prob_value
        return probs
    
    def get_entanglement_entropy(self) -> int:
        """计算纠缠熵 - 返回整型值（×1000）"""
        # 获取概率分布
        probs = self.get_probability_distribution()
        # 计算归一化常数
        total = np.sum(probs)
        if total == 0:
            return 0
        
        # 计算整型版本的熵
        entropy = 0
        for i in range(self.size):
            for j in range(self.size):
                if probs[i, j] > 0:
                    # 计算p*log(p)×1000，以保持整型
                    p = probs[i, j] / total
                    if p > 0:
                        log_p = int(np.log(p) * 1000)
                        entropy -= int(p * 1000) * log_p // 1000
        
        return entropy
    
    def measure(self, position: Tuple[int, int]) -> int:
        """
        在指定位置进行量子测量
        
        Args:
            position: 要测量的位置 (x, y)
            
        Returns:
            测量结果 (0 或 1)
        """
        x, y = position
        # 获取该位置的概率值（0-1000）
        prob_value = self.get_probability_distribution()[x, y]
        total = np.sum(self.get_probability_distribution())
        normalized_prob = prob_value / total if total > 0 else 0
        
        # 基于整型概率值进行测量
        # 随机数范围0-1000
        rand_val = random.randint(0, 1000)
        threshold = int(normalized_prob * 1000)
        # 如果随机值小于阈值，则结果为1，否则为0
        result = 1 if rand_val < threshold else 0
        
        return result

class ClassicalDomain:
    """经典域 (Ω_C) - 确定现实的空间"""
    
    def __init__(self, size: int = 100):
        """
        初始化经典域
        
        Args:
            size: 经典域大小
        """
        self.size = size
        # 经典知识表示为确定的值
        self.classical_states = np.zeros((size, size), dtype=int)
        # 已观测点的集合
        self.observed_points: Set[Tuple[int, int]] = set()
        # 经典信息熵 (×1000以保持整型)
        self.entropy = 0
        # 经典域中的知识库
        self.knowledge_base = {}
        
    def update_state(self, position: Tuple[int, int], value: int):
        """
        更新经典域中的状态
        
        Args:
            position: 位置坐标 (x, y)
            value: 经典值 (0 或 1)
        """
        x, y = position
        self.classical_states[x, y] = value
        self.observed_points.add(position)
        
        # 更新知识库
        if position not in self.knowledge_base:
            self.knowledge_base[position] = []
        self.knowledge_base[position].append((value, self.entropy))
        
        # 更新经典熵 - 使用整型计算 (×1000)
        ones = np.sum(self.classical_states)
        zeros = len(self.observed_points) - ones
        total = len(self.observed_points)
        
        if total > 0:
            p_one = ones / total
            p_zero = zeros / total
            
            entropy = 0
            if p_one > 0:
                # 计算-p*log(p)×1000
                log_p_one = int(np.log(p_one) * 1000)
                entropy -= int(p_one * 1000) * log_p_one // 1000
            if p_zero > 0:
                # 计算-p*log(p)×1000
                log_p_zero = int(np.log(p_zero) * 1000)
                entropy -= int(p_zero * 1000) * log_p_zero // 1000
            
            self.entropy = entropy
    
    def get_knowledge_density(self) -> int:
        """计算知识密度 (×1000)"""
        if self.size * self.size == 0:
            return 0
        # 返回观测点数量与总点数之比 (×1000)
        return len(self.observed_points) * 1000 // (self.size * self.size)

class InterfaceDomain:
    """界面域 (I) - 连接量子域和经典域的边界"""
    
    def __init__(self, decoherence_threshold: int = 500):
        """
        初始化界面域
        
        Args:
            decoherence_threshold: 解相干阈值 (×1000)
        """
        self.decoherence_threshold = decoherence_threshold  # 整型表示，×1000
        self.interface_points = set()
        # 解相干度量函数的值
        self.decoherence_values = {}
        
    def calculate_decoherence(self, quantum_domain: QuantumDomain, 
                             position: Tuple[int, int]) -> int:
        """
        计算指定位置的解相干度量 - 返回整型值 (×1000)
        
        Args:
            quantum_domain: 量子域
            position: 位置坐标
            
        Returns:
            解相干度量值 (×1000)
        """
        x, y = position
        # 解相干度量基于周围点的量子态
        neighborhood = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < quantum_domain.size and 0 <= ny < quantum_domain.size:
                    neighborhood.append(quantum_domain.quantum_states[nx, ny])
        
        # 通过邻近点的相位关联性计算解相干度
        if not neighborhood:
            return 0
            
        # 相位关联作为解相干度量 - 整型实现
        phases = neighborhood  # 在整型实现中，quantum_states直接存储相位值
        phase_diffs = []
        for i in range(1, len(phases)):
            # 计算相位差，确保在0-6283范围内
            diff = abs((phases[i] - phases[i-1]) % 6284)
            phase_diffs.append(diff)
        
        if not phase_diffs:
            return 0
        
        # 计算相位差的方差 (×1000)
        mean_diff = sum(phase_diffs) // len(phase_diffs)
        variance = 0
        for diff in phase_diffs:
            variance += (diff - mean_diff) ** 2
        variance = variance // len(phase_diffs)
        
        # 相位差的方差作为解相干度的度量 (×1000)
        decoherence = variance * 1000 // 3142  # 归一化，除以π×1000
        return decoherence
    
    def update_interface(self, quantum_domain: QuantumDomain, classical_domain: ClassicalDomain):
        """
        更新界面域
        
        Args:
            quantum_domain: 量子域
            classical_domain: 经典域
        """
        self.interface_points = set()
        
        # 寻找解相干度处于阈值附近的点
        for x in range(quantum_domain.size):
            for y in range(quantum_domain.size):
                position = (x, y)
                # 已经经典化的点不再考虑
                if position in classical_domain.observed_points:
                    continue
                    
                decoherence = self.calculate_decoherence(quantum_domain, position)
                self.decoherence_values[position] = decoherence
                
                # 判断是否为界面点 - 解相干度在阈值±10%范围内
                threshold_range = self.decoherence_threshold // 10
                if abs(decoherence - self.decoherence_threshold) < threshold_range:
                    self.interface_points.add(position)

class Observer:
    """观察者 - 执行量子→经典转换的节点"""
    
    def __init__(self, 
                 dimension: int = 3000,  # 观察者初始维度 (×1000)
                 classical_capacity: int = 700,  # 经典化能力 (×1000)
                 quantum_capacity: int = 300):  # 量子化能力 (×1000)
        """
        初始化观察者
        
        Args:
            dimension: 观察者维度 (×1000)
            classical_capacity: 经典化能力 (×1000)
            quantum_capacity: 量子化能力 (×1000)
        """
        self.dimension = dimension
        self.classical_capacity = classical_capacity
        self.quantum_capacity = quantum_capacity
        self.knowledge_base = {}  # 观察者的经典知识库
        self.total_observations = 0
        self.observation_history = []
        
    def observe(self, 
                quantum_domain: QuantumDomain, 
                classical_domain: ClassicalDomain,
                interface: InterfaceDomain,
                position: Tuple[int, int] = None) -> Tuple[int, int]:
        """
        观察一个位置，执行量子→经典转换
        
        Args:
            quantum_domain: 量子域
            classical_domain: 经典域
            interface: 界面域
            position: 指定的观察位置，如不指定则基于界面域自动选择
            
        Returns:
            观察位置和结果
        """
        # 如果未指定位置，从界面点或随机选择
        if position is None:
            if interface.interface_points and random.randint(0, 100) < 80:  # 80%概率
                # 80%的概率从界面点选择
                position = random.choice(list(interface.interface_points))
            else:
                # 20%的概率随机探索
                x = random.randint(0, quantum_domain.size - 1)
                y = random.randint(0, quantum_domain.size - 1)
                position = (x, y)
                
                # 已经观察过的点不再观察
                while position in classical_domain.observed_points:
                    x = random.randint(0, quantum_domain.size - 1)
                    y = random.randint(0, quantum_domain.size - 1)
                    position = (x, y)
        
        # 执行量子测量
        result = quantum_domain.measure(position)
        
        # 应用经典化过程 - 使用整型随机值和经典化能力
        if random.randint(0, 1000) < self.classical_capacity:
            classical_domain.update_state(position, result)
            # 更新知识库
            self.knowledge_base[position] = result
            self.total_observations += 1
            self.observation_history.append((position, result))
            
            # 更新观察者维度
            self.update_dimension(classical_domain)
            
        return position, result
    
    def update_dimension(self, classical_domain: ClassicalDomain):
        """
        更新观察者维度 - 使用整型计算
        
        D_O ∝ I_经典知识 / (S_经典熵 + ε)
        
        Args:
            classical_domain: 经典域
        """
        epsilon = 1  # 防止除零的小常数 (×1000实现中为1)
        # 经典知识量与观察数量和知识密度相关
        knowledge_amount = self.total_observations * classical_domain.get_knowledge_density()
        
        # 基于公理4的维度更新 - 整型实现
        # dimension_factor = log(1 + knowledge_amount) / (entropy + epsilon)
        knowledge_log = 0
        if knowledge_amount > 0:
            # 计算log(1 + knowledge_amount)×1000
            knowledge_log = int(np.log(1 + knowledge_amount / 1000) * 1000)
        
        # 计算分母 (entropy + epsilon)
        entropy_factor = classical_domain.entropy + epsilon
        if entropy_factor <= 0:
            entropy_factor = 1  # 防止除零
            
        dimension_factor = knowledge_log * 1000 // entropy_factor
        
        # 加入维度转换与经典化/量子化比率的影响
        capacity_ratio = 0
        if self.quantum_capacity > 0:
            capacity_ratio = self.classical_capacity * 1000 // self.quantum_capacity
        else:
            capacity_ratio = 1000  # 默认比率为1 (×1000)
            
        # 计算log(1 + capacity_ratio)×1000
        capacity_log = int(np.log(1 + capacity_ratio / 1000) * 1000)
        
        # 维度变化率与知识增长和熵减少成正比
        # 使用更合理的维度计算公式，避免维度增长过快
        self.dimension = 1000 + 2 * knowledge_log * capacity_log // 1000
        
        # 根据公理系统中的维度定义，限制维度在合理范围内
        if self.dimension > 42000:  # 42 × 1000
            # 进入超维区域
            self.dimension = 42000 + int(np.log(1 + (self.dimension - 42000) / 10000) * 1000)
        
    def get_dimension(self) -> int:
        """获取观察者当前维度 (×1000)"""
        return self.dimension

class QuantumClassicalDualismSimulation:
    """量子经典二元论宇宙模拟"""
    
    def __init__(self, size: int = 50):
        """
        初始化模拟
        
        Args:
            size: 宇宙大小
        """
        self.quantum_domain = QuantumDomain(size)
        self.classical_domain = ClassicalDomain(size)
        self.interface = InterfaceDomain()
        self.observer = Observer()
        self.time = 0
        self.size = size
        self.history = {
            'time': [],
            'observer_dimension': [],
            'quantum_entropy': [],
            'classical_entropy': [],
            'interface_size': []
        }
        # 动画加速状态
        self.speed_multiplier = 1  # 初始速度倍率
        
        # 宇宙循环相关属性
        self.universe_age = 0  # 当前宇宙年龄
        self.universe_cycle = 1  # 宇宙循环次数
        self.singularity_threshold = 25000  # 绝对奇点阈值 (×1000)
        self.big_bang_events = []  # 记录大爆炸事件
        self.is_big_bang_imminent = False  # 大爆炸即将发生标志
        self.paused = False  # 动画暂停标志
        
    def step(self):
        """模拟一个时间步"""
        # 递增时间和宇宙年龄
        self.time += 1
        self.universe_age += 1
        
        # 量子域演化
        self.quantum_domain.apply_quantum_operation()
        
        # 更新界面
        self.interface.update_interface(self.quantum_domain, self.classical_domain)
        
        # 观察者进行观察
        self.observer.observe(self.quantum_domain, self.classical_domain, self.interface)
        
        # 记录历史数据
        self.history['time'].append(self.time)
        self.history['observer_dimension'].append(self.observer.get_dimension())
        self.history['quantum_entropy'].append(self.quantum_domain.get_entanglement_entropy())
        self.history['classical_entropy'].append(self.classical_domain.entropy)
        self.history['interface_size'].append(len(self.interface.interface_points))
        
        # 检测是否达到奇点
        self._check_singularity()
    
    def _check_singularity(self):
        """检测是否达到奇点条件"""
        observer_dimension = self.observer.dimension
        quantum_entropy = self.quantum_domain.get_entanglement_entropy()
        
        # 奇点形成条件：观察者维度达到阈值或超过阈值
        if observer_dimension >= self.singularity_threshold:
            if not self.is_big_bang_imminent:
                print(f"\n*** 宇宙周期 {self.universe_cycle} ***")
                print(f"*** 宇宙年龄: {self.universe_age} ***")
                print(f"*** 观察者维度达到 {observer_dimension/1000:.2f}，接近绝对奇点! ***")
                print(f"*** 量子熵: {quantum_entropy/1000:.4f} ***")
                print("*** 绝对奇点即将形成，宇宙大爆炸即将发生... ***\n")
                self.is_big_bang_imminent = True
                self.paused = True  # 达到奇点时暂停
        
        # 绝对奇点条件：观察者维度超过阈值 + 5000 (5×1000)
        if observer_dimension >= self.singularity_threshold + 5000:
            self._trigger_big_bang()
    
    def _trigger_big_bang(self):
        """触发宇宙大爆炸，重置宇宙"""
        # 记录大爆炸事件
        self.big_bang_events.append({
            'cycle': self.universe_cycle,
            'age': self.universe_age,
            'observer_dimension': self.observer.dimension,
            'quantum_entropy': self.quantum_domain.get_entanglement_entropy(),
            'classical_entropy': self.classical_domain.entropy,
            'observations': len(self.classical_domain.observed_points)
        })
        
        print(f"\n********************")
        print(f"*** 绝对奇点形成! ***")
        print(f"*** 宇宙周期 {self.universe_cycle} 结束，年龄: {self.universe_age} ***")
        print(f"*** 宇宙大爆炸发生! ***")
        print(f"********************\n")
        
        # 增加宇宙循环计数
        self.universe_cycle += 1
        
        # 重置宇宙但保留历史记录
        old_history = self.history.copy()
        old_big_bang_events = self.big_bang_events.copy()
        
        # 重置量子域和经典域
        self.quantum_domain = QuantumDomain(self.size)
        self.classical_domain = ClassicalDomain(self.size)
        self.interface = InterfaceDomain()
        
        # 创建新的观察者，但维度略高于初始值
        # 每个宇宙周期观察者起点维度更高，表示宇宙演化
        start_dimension = 3000 + (self.universe_cycle - 1) * 500  # 3.0 + 0.5 * (cycle-1) × 1000
        self.observer = Observer(dimension=start_dimension)
        
        # 重置时间但保留宇宙周期信息
        self.time = 0
        self.universe_age = 0
        self.is_big_bang_imminent = False
        self.paused = False  # 重置暂停状态
        
        # 创建新的历史记录
        self.history = {
            'time': [],
            'observer_dimension': [],
            'quantum_entropy': [],
            'classical_entropy': [],
            'interface_size': []
        }
        
        # 保留大爆炸事件记录
        self.big_bang_events = old_big_bang_events
        
        # 提高奇点阈值，使得每个周期都更难达到奇点
        self.singularity_threshold += 2000  # 增加2.0 × 1000
        
        print(f"*** 宇宙周期 {self.universe_cycle} 开始 ***")
        print(f"*** 新的观察者初始维度: {start_dimension/1000:.2f} ***")
        print(f"*** 新的奇点阈值: {self.singularity_threshold/1000:.2f} ***\n")

    def animate(self, frames: int = 100, allow_cycles: bool = True, max_cycles: int = 5):
        """
        动画展示模拟过程
        
        Args:
            frames: 每个宇宙周期的帧数
            allow_cycles: 是否允许宇宙循环
            max_cycles: 最大宇宙循环次数
        """
        # 设置当前帧计数器
        self.current_frame = 0
        self.total_frames = 0
        self.max_total_frames = frames * max_cycles
        self.paused = False
        self.exit_requested = False
        
        # 创建主图形并清除之前可能存在的图形
        plt.close('all')
        fig = plt.figure(figsize=(12, 10))
        plt.suptitle(f'量子经典二元论模拟 (宇宙周期: {self.universe_cycle}, 宇宙年龄: {self.universe_age})', fontsize=14)
        
        # 预创建子图对象
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)
        
        # 初始化图像对象
        quantum_probs = self.quantum_domain.get_probability_distribution()
        im1 = ax1.imshow(quantum_probs, cmap='viridis')
        ax1.set_title('量子域 (概率分布)')
        fig.colorbar(im1, ax=ax1)
        
        classical_map = np.zeros((self.size, self.size))
        for x, y in self.classical_domain.observed_points:
            classical_map[x, y] = self.classical_domain.classical_states[x, y] + 1
        im2 = ax2.imshow(classical_map, cmap='Greys', vmin=0, vmax=2)
        ax2.set_title('经典域 (已观测区域)')
        fig.colorbar(im2, ax=ax2)
        
        interface_map = np.zeros((self.size, self.size))
        for x, y in self.interface.interface_points:
            interface_map[x, y] = 1
        im3 = ax3.imshow(interface_map, cmap='hot')
        ax3.set_title('界面域')
        fig.colorbar(im3, ax=ax3)
        
        # 历史曲线
        line1, = ax4.plot(self.history['time'], [d/1000 for d in self.history['observer_dimension']], label='观察者维度')
        line2, = ax4.plot(self.history['time'], [e/1000 for e in self.history['quantum_entropy']], label='量子熵')
        line3, = ax4.plot(self.history['time'], [e/1000 for e in self.history['classical_entropy']], label='经典熵')
        ax4.set_title('观察者与熵的历史变化')
        ax4.set_xlabel('时间步')
        ax4.set_ylabel('值')
        ax4.legend()
        
        # 显示奇点阈值线
        line_threshold, = ax4.plot([0, frames], 
                                  [self.singularity_threshold/1000, self.singularity_threshold/1000], 
                                  'r--', label='奇点阈值')
        ax4.legend()
        
        # 状态信息文本对象
        info_text = fig.text(0.5, 0.01, "", ha='center', fontsize=12)
        entropy_text = fig.text(0.5, 0.04, "", ha='center', fontsize=12)
        cycle_text = fig.text(0.5, 0.95, f"宇宙周期: {self.universe_cycle} | 宇宙年龄: {self.universe_age}", 
                            ha='center', fontsize=14, color='red')
        
        # 添加控制按钮
        ax_speed_up = plt.axes([0.6, 0.92, 0.08, 0.05])
        ax_speed_down = plt.axes([0.69, 0.92, 0.08, 0.05])
        ax_skip = plt.axes([0.78, 0.92, 0.07, 0.05])
        ax_pause = plt.axes([0.86, 0.92, 0.07, 0.05])
        ax_exit = plt.axes([0.94, 0.92, 0.05, 0.05])
        
        btn_speed_up = Button(ax_speed_up, '+速度')
        btn_speed_down = Button(ax_speed_down, '-速度')
        btn_skip = Button(ax_skip, '跳过')
        btn_pause = Button(ax_pause, '暂停/继续')
        btn_exit = Button(ax_exit, '退出')
        
        # 标记是否跳过帧
        self.should_skip = False
        self.skip_frames = 0
        
        # 按钮回调函数
        def on_speed_up(event):
            self.speed_multiplier = min(self.speed_multiplier + 1, 10)
            print(f"模拟速度: {self.speed_multiplier}x")
            plt.suptitle(f'量子经典二元论模拟 (速度: {self.speed_multiplier}x) | 宇宙周期: {self.universe_cycle}', fontsize=14)
            fig.canvas.draw_idle()
            
        def on_speed_down(event):
            self.speed_multiplier = max(self.speed_multiplier - 1, 1)
            print(f"模拟速度: {self.speed_multiplier}x")
            plt.suptitle(f'量子经典二元论模拟 (速度: {self.speed_multiplier}x) | 宇宙周期: {self.universe_cycle}', fontsize=14)
            fig.canvas.draw_idle()
            
        def on_skip(event):
            self.should_skip = True
            self.skip_frames = 50
            print(f"将跳过接下来的50帧!")
            
        def on_pause(event):
            self.paused = not self.paused
            state = "暂停" if self.paused else "继续"
            print(f"模拟已{state}")
            if self.paused:
                btn_pause.label.set_text('继续')
            else:
                btn_pause.label.set_text('暂停')
            fig.canvas.draw_idle()
        
        def on_exit(event):
            self.exit_requested = True
            print("正在退出动画模拟...")
            plt.close(fig)
        
        # 连接回调
        btn_speed_up.on_clicked(on_speed_up)
        btn_speed_down.on_clicked(on_speed_down)
        btn_skip.on_clicked(on_skip)
        btn_pause.on_clicked(on_pause)
        btn_exit.on_clicked(on_exit)
        
        # 设置键盘事件处理
        def on_key(event):
            if event.key == '+':
                on_speed_up(event)
            elif event.key == '-':
                on_speed_down(event)
            elif event.key == 's':
                on_skip(event)
            elif event.key == ' ':  # 空格键暂停/继续
                on_pause(event)
            elif event.key == 'escape':  # ESC键退出
                on_exit(event)
        
        # 连接键盘事件
        fig.canvas.mpl_connect('key_press_event', on_key)
        
        # 添加说明文本
        fig.text(0.3, 0.92, '控制: "+"加速, "-"减速, "s"跳过, 空格暂停/继续, ESC退出', ha='center', fontsize=12)
        
        # 更新函数 - 用于动画更新
        def update(frame_num):
            if self.exit_requested:
                return None
                
            # 如果暂停状态，不进行更新
            if self.paused:
                return [im1, im2, im3, line1, line2, line3, line_threshold, info_text, entropy_text, cycle_text]
                
            # 如果达到最大总帧数或宇宙达到最大循环次数，停止动画
            if self.total_frames >= self.max_total_frames or self.universe_cycle > max_cycles:
                print(f"达到最大模拟限制: {self.universe_cycle}/{max_cycles} 个宇宙周期")
                return None
                
            # 判断是否需要跳过帧
            if self.should_skip and self.skip_frames > 0:
                steps = min(self.skip_frames, frames - self.current_frame)
                for _ in range(steps):
                    if not self.paused:  # 确保在非暂停状态下执行
                        self.step()
                        self.current_frame += 1
                        self.total_frames += 1
                        # 如果在跳过过程中达到奇点，停止跳过
                        if self.paused:
                            break
                self.skip_frames -= steps
                if self.skip_frames <= 0:
                    self.should_skip = False
                print(f"跳过了{steps}帧! 当前时间步: {self.time}, 宇宙年龄: {self.universe_age}")
            else:
                # 正常按速度执行
                steps_per_frame = self.speed_multiplier
                for _ in range(steps_per_frame):
                    if not self.paused:  # 确保在非暂停状态下执行
                        self.step()
                        self.current_frame += 1
                        self.total_frames += 1
                        # 如果在执行过程中达到奇点，停止当前步骤
                        if self.paused:
                            break
            
            # 更新图像数据
            quantum_probs = self.quantum_domain.get_probability_distribution()
            im1.set_array(quantum_probs)
            
            classical_map = np.zeros((self.size, self.size))
            for x, y in self.classical_domain.observed_points:
                classical_map[x, y] = self.classical_domain.classical_states[x, y] + 1
            im2.set_array(classical_map)
            
            interface_map = np.zeros((self.size, self.size))
            for x, y in self.interface.interface_points:
                interface_map[x, y] = 1
            im3.set_array(interface_map)
            
            # 更新历史曲线
            line1.set_data(self.history['time'], [d/1000 for d in self.history['observer_dimension']])
            line2.set_data(self.history['time'], [e/1000 for e in self.history['quantum_entropy']])
            line3.set_data(self.history['time'], [e/1000 for e in self.history['classical_entropy']])
            
            # 更新奇点阈值线
            line_threshold.set_data([0, max(self.time + 10, frames)], 
                                  [self.singularity_threshold/1000, self.singularity_threshold/1000])
            
            # 自动调整坐标轴范围
            ax4.relim()
            ax4.autoscale_view()
            
            # 更新宇宙周期和年龄信息
            cycle_text.set_text(f"宇宙周期: {self.universe_cycle} | 宇宙年龄: {self.universe_age}" + 
                            (" [暂停]" if self.paused else ""))
            
            # 更新信息文本
            dimension_text = (f"观察者维度: {self.observer.dimension/1000:.2f}, 已观测点: {len(self.classical_domain.observed_points)}, "
                             f"离奇点还有: {max(0, self.singularity_threshold - self.observer.dimension)/1000:.2f}")
            entropy_text_str = f"量子熵: {self.quantum_domain.get_entanglement_entropy()/1000:.2f}, 经典熵: {self.classical_domain.entropy/1000:.2f}"
            
            info_text.set_text(dimension_text)
            entropy_text.set_text(entropy_text_str)
            
            if self.current_frame % 10 == 0:
                print(f"宇宙周期: {self.universe_cycle}, 宇宙年龄: {self.universe_age}, "
                      f"观察者维度: {self.observer.dimension/1000:.2f}, 速度: {self.speed_multiplier}x")
            
            # 当前宇宙周期结束，但尚未达到最大周期数，重置当前帧计数器
            if self.is_big_bang_imminent and allow_cycles and not self.paused:
                self.current_frame = frames  # 强制当前周期结束
            
            # 调整布局
            plt.tight_layout(rect=[0, 0.07, 1, 0.9])
            
            # 如果已经完成当前宇宙周期的所有帧，但未达到最大循环次数
            if self.current_frame >= frames and allow_cycles and self.universe_cycle < max_cycles and not self.paused:
                # 重置当前帧计数器，准备下一个宇宙周期
                self.current_frame = 0
                print(f"宇宙周期 {self.universe_cycle} 模拟完成，已完成 {self.total_frames}/{self.max_total_frames} 帧")
                
                # 如果尚未达到奇点，手动触发大爆炸
                if not self.is_big_bang_imminent:
                    print(f"强制触发宇宙大爆炸，开始新的宇宙周期")
                    # 强制维度达到奇点
                    self.observer.dimension = self.singularity_threshold + 5100  # 5.1 × 1000
                    self._trigger_big_bang()
                    
                # 更新奇点阈值线
                line_threshold.set_data([0, frames], 
                                      [self.singularity_threshold/1000, self.singularity_threshold/1000])
                
                return [im1, im2, im3, line1, line2, line3, line_threshold, info_text, entropy_text, cycle_text]
            
            # 如果已经完成所有帧和所有周期，返回None停止动画
            if (self.current_frame >= frames and not allow_cycles) or \
               (self.universe_cycle >= max_cycles and self.current_frame >= frames):
                print(f"模拟完成! 总共 {self.universe_cycle} 个宇宙周期，{self.total_frames} 帧")
                return None
            
            # 返回所有要更新的对象
            return [im1, im2, im3, line1, line2, line3, line_threshold, info_text, entropy_text, cycle_text]
        
        # 创建动画 - 每帧时间间隔根据速度调整
        ani = FuncAnimation(fig, update, frames=None, 
                         interval=500, blit=False, repeat=False)
        
        plt.tight_layout(rect=[0, 0.07, 1, 0.9])
        plt.show(block=True)
        
        # 动画结束后，显示最终状态
        if not self.exit_requested:
            self.show_final_state()
        
        return None
        
    def show_final_state(self):
        """显示最终状态图像和宇宙循环历史"""
        # 创建一个新的图表，展示所有宇宙周期的信息
        plt.figure(figsize=(14, 10))
        plt.suptitle(f'量子经典二元论多重宇宙模拟 - 总计 {self.universe_cycle} 个宇宙周期', fontsize=16)
        
        # 上半部分：当前宇宙状态
        plt.subplot(2, 3, 1)
        plt.imshow(self.quantum_domain.get_probability_distribution(), cmap='viridis')
        plt.title(f'量子域 (宇宙周期 {self.universe_cycle})')
        plt.colorbar()
        
        plt.subplot(2, 3, 2)
        classical_map = np.zeros((self.size, self.size))
        for x, y in self.classical_domain.observed_points:
            classical_map[x, y] = self.classical_domain.classical_states[x, y] + 1
        plt.imshow(classical_map, cmap='Greys', vmin=0, vmax=2)
        plt.title(f'经典域 (宇宙周期 {self.universe_cycle})')
        plt.colorbar()
        
        plt.subplot(2, 3, 3)
        interface_map = np.zeros((self.size, self.size))
        for x, y in self.interface.interface_points:
            interface_map[x, y] = 1
        plt.imshow(interface_map, cmap='hot')
        plt.title(f'界面域 (宇宙周期 {self.universe_cycle})')
        plt.colorbar()
        
        # 下半部分：宇宙历史分析
        plt.subplot(2, 3, 4)
        # 如果有多个宇宙周期，显示宇宙年龄分布
        if self.big_bang_events:
            cycles = [event['cycle'] for event in self.big_bang_events]
            ages = [event['age'] for event in self.big_bang_events]
            plt.bar(cycles, ages, color='purple')
            plt.axhline(y=np.mean(ages), color='r', linestyle='--', label=f'平均年龄: {np.mean(ages):.1f}')
            plt.xlabel('宇宙周期')
            plt.ylabel('宇宙年龄')
            plt.title('宇宙寿命分析')
            plt.legend()
        else:
            plt.text(0.5, 0.5, '尚无完整的宇宙周期数据', ha='center', va='center')
            plt.title('宇宙寿命分析')
        
        plt.subplot(2, 3, 5)
        # 显示观察者维度演化
        if self.big_bang_events:
            cycles = [event['cycle'] for event in self.big_bang_events]
            dims = [event['observer_dimension'] for event in self.big_bang_events]
            plt.plot(cycles, dims, 'o-', color='green')
            plt.xlabel('宇宙周期')
            plt.ylabel('最终观察者维度')
            plt.title('观察者维度演化')
        else:
            plt.text(0.5, 0.5, '尚无完整的宇宙周期数据', ha='center', va='center')
            plt.title('观察者维度演化')
        
        plt.subplot(2, 3, 6)
        # 显示熵演化
        if self.big_bang_events:
            cycles = [event['cycle'] for event in self.big_bang_events]
            q_entropy = [event['quantum_entropy'] for event in self.big_bang_events]
            c_entropy = [event['classical_entropy'] for event in self.big_bang_events]
            plt.plot(cycles, q_entropy, 'o-', color='blue', label='量子熵')
            plt.plot(cycles, c_entropy, 'o-', color='orange', label='经典熵')
            plt.xlabel('宇宙周期')
            plt.ylabel('熵')
            plt.title('宇宙熵演化')
            plt.legend()
        else:
            plt.text(0.5, 0.5, '尚无完整的宇宙周期数据', ha='center', va='center')
            plt.title('宇宙熵演化')
        
        # 添加最终状态信息
        dimension_text = (f"当前宇宙周期: {self.universe_cycle}, 宇宙年龄: {self.universe_age}, "
                         f"观察者维度: {self.observer.dimension/1000:.2f}")
        entropy_text = (f"量子熵: {self.quantum_domain.get_entanglement_entropy()/1000:.2f}, "
                       f"经典熵: {self.classical_domain.entropy/1000:.2f}, "
                       f"观察点数量: {len(self.classical_domain.observed_points)}")
        
        # 如果有大爆炸事件，添加统计信息
        if self.big_bang_events:
            stats_text = (f"宇宙循环总数: {len(self.big_bang_events) + 1}, " 
                         f"平均宇宙寿命: {np.mean([e['age'] for e in self.big_bang_events]):.1f}, "
                         f"平均观察者维度: {np.mean([e['observer_dimension'] for e in self.big_bang_events]):.2f}")
            plt.figtext(0.5, 0.07, stats_text, ha='center', fontsize=12, 
                      bbox=dict(facecolor='yellow', alpha=0.3))
        
        plt.figtext(0.5, 0.01, dimension_text, ha='center', fontsize=12)
        plt.figtext(0.5, 0.04, entropy_text, ha='center', fontsize=12)
        
        plt.tight_layout(rect=[0, 0.07, 1, 0.93])
        plt.show()

    def run(self, steps: int = 100):
        """
        运行模拟多个时间步
        
        Args:
            steps: 时间步数
        """
        for _ in range(steps):
            self.step()
            
    def visualize(self):
        """可视化当前状态"""
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        
        # 可视化量子域
        quantum_probs = self.quantum_domain.get_probability_distribution()
        im1 = axs[0, 0].imshow(quantum_probs, cmap='viridis')
        axs[0, 0].set_title('量子域 (概率分布)')
        fig.colorbar(im1, ax=axs[0, 0])
        
        # 可视化经典域
        classical_map = np.zeros((self.size, self.size))
        for x, y in self.classical_domain.observed_points:
            classical_map[x, y] = self.classical_domain.classical_states[x, y] + 1
        im2 = axs[0, 1].imshow(classical_map, cmap='Greys', vmin=0, vmax=2)
        axs[0, 1].set_title('经典域 (已观测区域)')
        fig.colorbar(im2, ax=axs[0, 1])
        
        # 可视化界面域
        interface_map = np.zeros((self.size, self.size))
        for x, y in self.interface.interface_points:
            interface_map[x, y] = 1
        im3 = axs[1, 0].imshow(interface_map, cmap='hot')
        axs[1, 0].set_title('界面域')
        fig.colorbar(im3, ax=axs[1, 0])
        
        # 可视化观察者历史
        axs[1, 1].plot(self.history['time'], self.history['observer_dimension'], label='观察者维度')
        axs[1, 1].plot(self.history['time'], self.history['quantum_entropy'], label='量子熵')
        axs[1, 1].plot(self.history['time'], self.history['classical_entropy'], label='经典熵')
        
        # 显示奇点阈值线
        axs[1, 1].axhline(y=self.singularity_threshold/1000, color='r', linestyle='--', label='奇点阈值')
        
        axs[1, 1].set_title('观察者与熵的历史变化')
        axs[1, 1].set_xlabel('时间步')
        axs[1, 1].set_ylabel('值')
        axs[1, 1].legend()
        
        # 添加观察者维度与宇宙信息标注
        dimension_text = f"观察者维度: {self.observer.dimension/1000:.2f} | 距离奇点: {max(0, self.singularity_threshold - self.observer.dimension)/1000:.2f}"
        universe_text = f"宇宙周期: {self.universe_cycle} | 宇宙年龄: {self.universe_age}"
        knowledge_text = f"已观测点数量: {len(self.classical_domain.observed_points)}"
        entropy_text = f"量子熵: {self.quantum_domain.get_entanglement_entropy()/1000:.2f}, 经典熵: {self.classical_domain.entropy/1000:.2f}"
        
        fig.text(0.5, 0.01, dimension_text + " | " + knowledge_text, ha='center', fontsize=12)
        fig.text(0.5, 0.04, entropy_text, ha='center', fontsize=12)
        fig.text(0.5, 0.97, universe_text, ha='center', fontsize=14, color='red', 
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        plt.show()

# 递归操作的示例实现
class RecursiveStructure:
    """递归结构 - 体现宇宙的自我参照性质"""
    
    def __init__(self, simulation):
        """
        初始化递归结构
        
        Args:
            simulation: 量子经典二元论模拟实例
        """
        self.simulation = simulation
        self.recursion_level = 0
        self.recursive_history = []
        
    def apply_recursion(self):
        """应用递归操作"""
        self.recursion_level += 1
        
        # 递归自指过程
        observer_dim = self.simulation.observer.dimension
        # 递归结构的复杂度随观察者维度增加 - 整型计算
        # 计算log(1 + observer_dim/1000) * 1000
        log_term = int(np.log(1 + observer_dim / 1000) * 1000)
        # 计算(1 - exp(-recursion_level)) * 1000
        exp_term = int((1 - np.exp(-self.recursion_level)) * 1000)
        # 计算复杂度 = log_term * exp_term / 1000
        recursion_complexity = log_term * exp_term // 1000
        
        # 保存当前递归历史
        self.recursive_history.append({
            'level': self.recursion_level,
            'complexity': recursion_complexity,
            'observer_dimension': observer_dim,
        })
        
        # 递归对宇宙的影响 - 高阶递归会影响观察者能力
        if self.recursion_level > 3:
            # 高阶递归增强观察者的量子化能力 - 整型计算
            # 计算log(recursion_level) * 10
            log_factor = int(np.log(self.recursion_level) * 10)
            # 增加量子化能力 = quantum_capacity * (1 + log_factor/1000)
            quantum_increase = self.simulation.observer.quantum_capacity * (1000 + log_factor) // 1000
            self.simulation.observer.quantum_capacity = quantum_increase
            # 限制在合理范围内
            self.simulation.observer.quantum_capacity = min(self.simulation.observer.quantum_capacity, 900)  # 0.9 * 1000
        
        return recursion_complexity / 1000  # 返回缩放后的浮点数，便于打印

# 示例代码，展示如何使用这个模拟
if __name__ == "__main__":
    print("初始化量子经典二元论宇宙模拟 v34.0...")
    print("根据量子经典二元论公理设置参数：")
    print("- 公理1: 二元存在性 - 宇宙由量子域Ω_Q和经典域Ω_C组成")
    print("- 公理2: 信息守恒 - 信息在整个宇宙中守恒")
    print("- 公理3: 观察者经典化 - 观察者执行量子→经典转换")
    print("- 公理4: 维度涌现 - 观察者维度是经典化能力与量子化能力的函数")
    print("- 公理5: 绝对递归本源性 - 实相的最深层结构是绝对递归构造")
    
    # 使用30×30的宇宙大小
    simulation = QuantumClassicalDualismSimulation(size=30)
    recursive_structure = RecursiveStructure(simulation)
    
    print("\n开始模拟...")
    # 运行100步模拟
    simulation.run(100)
    
    # 应用几次递归
    print("\n应用绝对递归（公理5）...")
    for _ in range(5):
        complexity = recursive_structure.apply_recursion()
        print(f"应用递归层级 {recursive_structure.recursion_level}, 复杂度: {complexity:.4f}")
    
    print("\n模拟完成，显示可视化结果...")
    simulation.visualize()
    
    print("\n启动动画模拟...")
    print("- 当观察者维度达到奇点阈值时，动画将自动暂停")
    print("- 可使用'暂停/继续'按钮或空格键控制模拟")
    print("- 使用'退出'按钮或ESC键可退出动画并继续程序")
    
    # 设置奇点阈值为25.0 (×1000)
    simulation.singularity_threshold = 25000
    # 启动动画模拟，允许宇宙循环
    simulation.animate(frames=200, allow_cycles=True, max_cycles=5)
    
    print("\n模拟结果统计：")
    print(f"最终观察者维度: {simulation.observer.dimension/1000:.4f}")
    print(f"量子域熵: {simulation.quantum_domain.get_entanglement_entropy()/1000:.4f}")
    print(f"经典域熵: {simulation.classical_domain.entropy/1000:.4f}")
    print(f"观察点数量: {len(simulation.classical_domain.observed_points)}")
    print(f"宇宙年龄: {simulation.universe_age}")
    print(f"宇宙周期: {simulation.universe_cycle}")
    
    if simulation.big_bang_events:
        print("\n宇宙循环历史:")
        for idx, event in enumerate(simulation.big_bang_events):
            print(f"周期 {event['cycle']}: 年龄={event['age']}, 维度={event['observer_dimension']/1000:.2f}, "
                 f"量子熵={event['quantum_entropy']/1000:.2f}, 经典熵={event['classical_entropy']/1000:.2f}")
    
    print("\n备注：本模拟基于量子经典二元论核心理论v34.0，使用整型计算进行模拟") 