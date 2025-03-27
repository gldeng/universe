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
        # 量子态表示为概率振幅
        self.quantum_states = np.zeros((size, size), dtype=complex)
        # 初始化为最大叠加态
        for i in range(size):
            for j in range(size):
                phase = 2 * np.pi * random.random()
                self.quantum_states[i, j] = np.exp(1j * phase)
        # 归一化
        self.normalize()
        
    def normalize(self):
        """归一化量子态"""
        norm = np.sqrt(np.sum(np.abs(self.quantum_states)**2))
        if norm > 0:
            self.quantum_states /= norm
            
    def apply_quantum_operation(self):
        """应用量子演化算子"""
        # 随机相位变化模拟量子演化
        for i in range(self.size):
            for j in range(self.size):
                phase = 0.1 * np.pi * random.random()
                self.quantum_states[i, j] *= np.exp(1j * phase)
        self.normalize()
    
    def get_probability_distribution(self) -> np.ndarray:
        """获取概率分布"""
        return np.abs(self.quantum_states)**2
    
    def get_entanglement_entropy(self) -> float:
        """计算纠缠熵"""
        probs = self.get_probability_distribution().flatten()
        probs = probs[probs > 0]  # 避免log(0)
        return -np.sum(probs * np.log(probs))
    
    def measure(self, position: Tuple[int, int]) -> int:
        """
        在指定位置进行量子测量
        
        Args:
            position: 要测量的位置 (x, y)
            
        Returns:
            测量结果 (0 或 1)
        """
        x, y = position
        prob = np.abs(self.quantum_states[x, y])**2
        # 基于概率振幅的平方进行测量
        result = 1 if random.random() < prob else 0
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
        # 经典信息熵
        self.entropy = 0.0
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
        
        # 更新经典熵
        ones = np.sum(self.classical_states)
        zeros = len(self.observed_points) - ones
        total = len(self.observed_points)
        
        if total > 0:
            p_one = ones / total
            p_zero = zeros / total
            
            entropy = 0
            if p_one > 0:
                entropy -= p_one * np.log(p_one)
            if p_zero > 0:
                entropy -= p_zero * np.log(p_zero)
            
            self.entropy = entropy
    
    def get_knowledge_density(self) -> float:
        """计算知识密度"""
        if self.size * self.size == 0:
            return 0
        return len(self.observed_points) / (self.size * self.size)

class InterfaceDomain:
    """界面域 (I) - 连接量子域和经典域的边界"""
    
    def __init__(self, decoherence_threshold: float = 0.5):
        """
        初始化界面域
        
        Args:
            decoherence_threshold: 解相干阈值
        """
        self.decoherence_threshold = decoherence_threshold
        self.interface_points = set()
        # 解相干度量函数的值
        self.decoherence_values = {}
        
    def calculate_decoherence(self, quantum_domain: QuantumDomain, 
                             position: Tuple[int, int]) -> float:
        """
        计算指定位置的解相干度量
        
        Args:
            quantum_domain: 量子域
            position: 位置坐标
            
        Returns:
            解相干度量值
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
            
        # 相位关联作为解相干度量
        phases = [np.angle(val) for val in neighborhood]
        phase_diffs = [abs((phases[i] - phases[i-1]) % (2*np.pi)) 
                      for i in range(1, len(phases))]
        
        if not phase_diffs:
            return 0
        
        # 相位差的方差作为解相干度的度量
        decoherence = np.var(phase_diffs) / np.pi
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
                
                # 判断是否为界面点
                if abs(decoherence - self.decoherence_threshold) < 0.1:
                    self.interface_points.add(position)

class Observer:
    """观察者 - 执行量子→经典转换的节点"""
    
    def __init__(self, 
                 dimension: float = 3.0,
                 classical_capacity: float = 0.7, 
                 quantum_capacity: float = 0.3):
        """
        初始化观察者
        
        Args:
            dimension: 观察者维度
            classical_capacity: 经典化能力 (Cₒ)
            quantum_capacity: 量子化能力 (Qₒ)
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
            if interface.interface_points and random.random() < 0.8:
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
        
        # 应用经典化过程
        if random.random() < self.classical_capacity:
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
        更新观察者维度
        
        D_O ∝ I_经典知识 / (S_经典熵 + ε)
        
        Args:
            classical_domain: 经典域
        """
        epsilon = 0.001  # 防止除零
        # 经典知识量与观察数量和知识密度相关
        knowledge_amount = self.total_observations * classical_domain.get_knowledge_density()
        
        # 基于公理4的维度更新
        dimension_factor = math.log(1 + knowledge_amount) / (classical_domain.entropy + epsilon)
        # 加入维度转换与经典化/量子化比率的影响
        capacity_ratio = self.classical_capacity / self.quantum_capacity if self.quantum_capacity > 0 else 1
        
        # 维度变化率与知识增长和熵减少成正比
        # 使用更合理的维度计算公式，避免维度增长过快
        self.dimension = 1 + 2 * math.log(1 + dimension_factor) * math.log(1 + capacity_ratio)
        
        # 根据公理系统中的维度定义，限制维度在合理范围内
        if self.dimension > 42:
            # 进入超维区域
            self.dimension = 42 + math.log(1 + (self.dimension - 42) / 10)
        
    def get_dimension(self) -> float:
        """获取观察者当前维度"""
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
        
    def step(self):
        """模拟一个时间步"""
        # 递增时间
        self.time += 1
        
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
        axs[1, 1].set_title('观察者与熵的历史变化')
        axs[1, 1].set_xlabel('时间步')
        axs[1, 1].set_ylabel('值')
        axs[1, 1].legend()
        
        # 添加观察者维度的当前值标注
        dimension_text = f"当前观察者维度: {self.observer.dimension:.2f}"
        knowledge_text = f"已观测点数量: {len(self.classical_domain.observed_points)}"
        entropy_text = f"量子熵: {self.quantum_domain.get_entanglement_entropy():.2f}, 经典熵: {self.classical_domain.entropy:.2f}"
        
        fig.text(0.5, 0.01, dimension_text + " | " + knowledge_text, ha='center', fontsize=12)
        fig.text(0.5, 0.04, entropy_text, ha='center', fontsize=12)
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        plt.show()
    
    def animate(self, frames: int = 100):
        """
        动画展示模拟过程
        
        Args:
            frames: 帧数
        """
        # 设置当前帧计数器
        self.current_frame = 0
        
        # 创建主图形并清除之前可能存在的图形
        plt.close('all')
        fig = plt.figure(figsize=(12, 10))
        plt.suptitle('量子经典二元论模拟 (按键盘上的"+"加速, "-"减速, "s"跳过50帧)', fontsize=14)
        
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
        line1, = ax4.plot(self.history['time'], self.history['observer_dimension'], label='观察者维度')
        line2, = ax4.plot(self.history['time'], self.history['quantum_entropy'], label='量子熵')
        line3, = ax4.plot(self.history['time'], self.history['classical_entropy'], label='经典熵')
        ax4.set_title('观察者与熵的历史变化')
        ax4.set_xlabel('时间步')
        ax4.set_ylabel('值')
        ax4.legend()
        
        # 状态信息文本对象
        info_text = fig.text(0.5, 0.01, "", ha='center', fontsize=12)
        entropy_text = fig.text(0.5, 0.04, "", ha='center', fontsize=12)
        
        # 添加控制按钮
        ax_speed_up = plt.axes([0.7, 0.92, 0.1, 0.05])
        ax_speed_down = plt.axes([0.81, 0.92, 0.1, 0.05])
        ax_skip = plt.axes([0.92, 0.92, 0.07, 0.05])
        
        btn_speed_up = Button(ax_speed_up, '+速度')
        btn_speed_down = Button(ax_speed_down, '-速度')
        btn_skip = Button(ax_skip, '跳过')
        
        # 标记是否跳过帧
        self.should_skip = False
        self.skip_frames = 0
        
        # 按钮回调函数
        def on_speed_up(event):
            self.speed_multiplier = min(self.speed_multiplier + 1, 10)
            print(f"模拟速度: {self.speed_multiplier}x")
            plt.suptitle(f'量子经典二元论模拟 (当前速度: {self.speed_multiplier}x)', fontsize=14)
            fig.canvas.draw_idle()
            
        def on_speed_down(event):
            self.speed_multiplier = max(self.speed_multiplier - 1, 1)
            print(f"模拟速度: {self.speed_multiplier}x")
            plt.suptitle(f'量子经典二元论模拟 (当前速度: {self.speed_multiplier}x)', fontsize=14)
            fig.canvas.draw_idle()
            
        def on_skip(event):
            self.should_skip = True
            self.skip_frames = 50
            print(f"将跳过接下来的50帧!")
        
        # 连接回调
        btn_speed_up.on_clicked(on_speed_up)
        btn_speed_down.on_clicked(on_speed_down)
        btn_skip.on_clicked(on_skip)
        
        # 设置键盘事件处理
        def on_key(event):
            if event.key == '+':
                on_speed_up(event)
            elif event.key == '-':
                on_speed_down(event)
            elif event.key == 's':
                on_skip(event)
        
        # 连接键盘事件
        fig.canvas.mpl_connect('key_press_event', on_key)
        
        # 添加说明文本
        fig.text(0.3, 0.96, '使用键盘或按钮控制: "+"加速, "-"减速, "s"跳过50帧', ha='center', fontsize=12)
        
        # 更新函数 - 用于动画更新
        def update(frame_num):
            # 判断是否需要跳过帧
            if self.should_skip and self.skip_frames > 0:
                steps = min(self.skip_frames, frames - self.current_frame)
                for _ in range(steps):
                    if self.current_frame < frames:
                        self.step()
                        self.current_frame += 1
                    else:
                        break
                self.skip_frames -= steps
                if self.skip_frames <= 0:
                    self.should_skip = False
                print(f"跳过了{steps}帧! 当前时间步: {self.time}")
            else:
                # 正常按速度执行
                steps_per_frame = self.speed_multiplier
                for _ in range(steps_per_frame):
                    if self.current_frame < frames:
                        self.step()
                        self.current_frame += 1
                    else:
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
            line1.set_data(self.history['time'], self.history['observer_dimension'])
            line2.set_data(self.history['time'], self.history['quantum_entropy'])
            line3.set_data(self.history['time'], self.history['classical_entropy'])
            
            # 自动调整坐标轴范围
            ax4.relim()
            ax4.autoscale_view()
            
            # 更新信息文本
            dimension_text = f"时间步: {self.time}, 观察者维度: {self.observer.dimension:.2f}, 已观测点: {len(self.classical_domain.observed_points)}"
            entropy_text_str = f"量子熵: {self.quantum_domain.get_entanglement_entropy():.2f}, 经典熵: {self.classical_domain.entropy:.2f}"
            
            info_text.set_text(dimension_text)
            entropy_text.set_text(entropy_text_str)
            
            if self.current_frame % 10 == 0 or self.current_frame == frames - 1:
                print(f"时间步: {self.time}, 观察者维度: {self.observer.dimension:.2f}, 速度: {self.speed_multiplier}x")
            
            # 调整布局
            plt.tight_layout(rect=[0, 0.07, 1, 0.9])
            
            # 如果已经完成所有帧，返回None停止动画
            if self.current_frame >= frames:
                print("动画完成！")
                return None
            
            return [im1, im2, im3, line1, line2, line3, info_text, entropy_text]
        
        # 创建动画 - 每帧时间间隔根据速度调整
        ani = FuncAnimation(fig, update, frames=None, 
                         interval=500, blit=False, repeat=False)
        
        plt.tight_layout(rect=[0, 0.07, 1, 0.9])
        plt.show(block=True)
        
        # 动画结束后，显示最终状态
        self.show_final_state()
        
        return None
        
    def show_final_state(self):
        """显示最终状态图像"""
        plt.figure(figsize=(12, 10))
        plt.suptitle('量子经典二元论模拟 (最终状态)', fontsize=14)
        
        plt.subplot(2, 2, 1)
        plt.imshow(self.quantum_domain.get_probability_distribution(), cmap='viridis')
        plt.title('量子域 (最终状态)')
        plt.colorbar()
        
        plt.subplot(2, 2, 2)
        classical_map = np.zeros((self.size, self.size))
        for x, y in self.classical_domain.observed_points:
            classical_map[x, y] = self.classical_domain.classical_states[x, y] + 1
        plt.imshow(classical_map, cmap='Greys', vmin=0, vmax=2)
        plt.title('经典域 (最终状态)')
        plt.colorbar()
        
        plt.subplot(2, 2, 3)
        interface_map = np.zeros((self.size, self.size))
        for x, y in self.interface.interface_points:
            interface_map[x, y] = 1
        plt.imshow(interface_map, cmap='hot')
        plt.title('界面域 (最终状态)')
        plt.colorbar()
        
        plt.subplot(2, 2, 4)
        plt.plot(self.history['time'], self.history['observer_dimension'], label='观察者维度')
        plt.plot(self.history['time'], self.history['quantum_entropy'], label='量子熵')
        plt.plot(self.history['time'], self.history['classical_entropy'], label='经典熵')
        plt.title('历史变化 (最终状态)')
        plt.xlabel('时间步')
        plt.ylabel('值')
        plt.legend()
        
        # 添加最终状态信息
        dimension_text = f"观察者最终维度: {self.observer.dimension:.2f}, 观察点数量: {len(self.classical_domain.observed_points)}"
        entropy_text = f"量子熵: {self.quantum_domain.get_entanglement_entropy():.2f}, 经典熵: {self.classical_domain.entropy:.2f}"
        plt.figtext(0.5, 0.01, dimension_text, ha='center', fontsize=12)
        plt.figtext(0.5, 0.04, entropy_text, ha='center', fontsize=12)
        
        plt.tight_layout(rect=[0, 0.07, 1, 0.93])
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
        # 递归结构的复杂度随观察者维度增加
        recursion_complexity = math.log(1 + observer_dim) * (1 - math.exp(-self.recursion_level))
        
        # 保存当前递归历史
        self.recursive_history.append({
            'level': self.recursion_level,
            'complexity': recursion_complexity,
            'observer_dimension': observer_dim,
        })
        
        # 递归对宇宙的影响 - 高阶递归会影响观察者能力
        if self.recursion_level > 3:
            # 高阶递归增强观察者的量子化能力
            self.simulation.observer.quantum_capacity *= (1 + 0.01 * math.log(self.recursion_level))
            # 限制在合理范围内
            self.simulation.observer.quantum_capacity = min(self.simulation.observer.quantum_capacity, 0.9)
        
        return recursion_complexity

# 示例代码，展示如何使用这个模拟
if __name__ == "__main__":
    print("初始化量子经典二元论宇宙模拟...")
    simulation = QuantumClassicalDualismSimulation(size=30)
    recursive_structure = RecursiveStructure(simulation)
    
    print("开始模拟...")
    # 运行100步模拟
    simulation.run(100)
    
    # 应用几次递归
    for _ in range(5):
        complexity = recursive_structure.apply_recursion()
        print(f"应用递归层级 {recursive_structure.recursion_level}, 复杂度: {complexity:.4f}")
    
    print("模拟完成，显示可视化结果...")
    simulation.visualize()
    
    print("启动动画模拟...")
    # 动画模拟会继续从当前状态运行
    simulation.animate(50)
    
    print(f"最终观察者维度: {simulation.observer.dimension:.4f}")
    print(f"量子域熵: {simulation.quantum_domain.get_entanglement_entropy():.4f}")
    print(f"经典域熵: {simulation.classical_domain.entropy:.4f}")
    print(f"观察点数量: {len(simulation.classical_domain.observed_points)}") 