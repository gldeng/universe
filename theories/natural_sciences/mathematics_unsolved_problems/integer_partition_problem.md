# 整数分拆问题的量子经典二元论证明
# Quantum-Classical Dualism Proof of the Integer Partition Problem

**[核心理论版本号29.0]**

[整数分拆问题](#整数分拆问题的量子经典二元论证明) | [Integer Partition Problem](#quantum-classical-dualism-proof-of-the-integer-partition-problem)
[问题描述](#问题描述--problem-description) | [Problem Description](#问题描述--problem-description)
[量子经典视角](#量子经典视角--quantum-classical-perspective) | [Quantum-Classical Perspective](#量子经典视角--quantum-classical-perspective)
[形式化描述](#形式化描述--formal-description) | [Formal Description](#形式化描述--formal-description)
[ZFC公理系统下的严格证明](#zfc公理系统下的严格证明--strict-proof-under-zfc-axiom-system) | [Strict Proof Under ZFC Axiom System](#zfc公理系统下的严格证明--strict-proof-under-zfc-axiom-system)
[量子经典二元论分析](#量子经典二元论分析--quantum-classical-dualism-analysis) | [Quantum-Classical Dualism Analysis](#量子经典二元论分析--quantum-classical-dualism-analysis)
[结论与预测](#结论与预测--conclusion-and-predictions) | [Conclusion and Predictions](#结论与预测--conclusion-and-predictions)
[参考文献](#参考文献--references) | [References](#参考文献--references)

## 问题描述 | Problem Description

整数分拆问题研究将正整数表示为若干正整数之和的不同方式。例如，数字4有以下5种分拆方式：
- 4
- 3 + 1
- 2 + 2
- 2 + 1 + 1
- 1 + 1 + 1 + 1

分拆数 $p(n)$ 表示正整数 $n$ 的不同分拆方式的数量。整数分拆问题的核心是研究 $p(n)$ 的性质、增长率和生成函数，以及分拆满足特定条件的计数问题。

这一问题由欧拉系统研究，拉马努金和哈代在20世纪初取得突破性进展，揭示了分拆函数的惊人性质和渐近公式。

The integer partition problem studies the different ways a positive integer can be represented as a sum of positive integers. For example, the number 4 has the following 5 partition methods:
- 4
- 3 + 1
- 2 + 2
- 2 + 1 + 1
- 1 + 1 + 1 + 1

The partition number $p(n)$ represents the number of different partition methods for the positive integer $n$. The core of the integer partition problem is to study the properties, growth rate, and generating functions of $p(n)$, as well as counting problems for partitions satisfying specific conditions.

This problem was systematically studied by Euler, with breakthrough progress made by Ramanujan and Hardy in the early 20th century, revealing astonishing properties and asymptotic formulas of the partition function.

## 量子经典视角 | Quantum-Classical Perspective

从量子经典二元论视角，整数分拆反映了量子叠加态（混沌）经典化为多种可能路径的组合计数。每一种分拆方式代表了量子信息向经典表达转化的一种可能途径，分拆数则对应了信息经典化的熵状态总数。

特别地，整数 $n$ 可视为一个量子能量系统，分拆则表示该系统经典化为不同能级配置的方式。分拆函数 $p(n)$ 的复杂性和快速增长反映了量子-经典转换过程中信息熵的爆炸性增长。

From the quantum-classical dualism perspective, integer partitioning reflects the combinatorial counting of quantum superposition states (chaos) classicalized into multiple possible paths. Each partition method represents a possible path for quantum information to transform into classical expression, and the partition number corresponds to the total number of entropy states of information classicalization.

Specifically, the integer $n$ can be viewed as a quantum energy system, and the partitions represent the ways this system classicalizes into different energy level configurations. The complexity and rapid growth of the partition function $p(n)$ reflect the explosive growth of information entropy in the quantum-classical transformation process.

## 形式化描述 | Formal Description

整数 $n$ 的一个分拆是将 $n$ 表示为正整数之和的一种方式：

$$
n = \lambda_1 + \lambda_2 + \cdots + \lambda_k, \text{ 其中 } \lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_k \geq 1
$$

分拆数 $p(n)$ 是 $n$ 的不同分拆的总数。

分拆函数的生成函数为：

$$
\sum_{n=0}^{\infty} p(n)q^n = \prod_{m=1}^{\infty} \frac{1}{1-q^m}
$$

A partition of an integer $n$ is a way to represent $n$ as a sum of positive integers:

$$
n = \lambda_1 + \lambda_2 + \cdots + \lambda_k, \text{ where } \lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_k \geq 1
$$

The partition number $p(n)$ is the total number of different partitions of $n$.

The generating function of the partition function is:

$$
\sum_{n=0}^{\infty} p(n)q^n = \prod_{m=1}^{\infty} \frac{1}{1-q^m}
$$

## ZFC公理系统下的严格证明 | Strict Proof Under ZFC Axiom System

以下是基于ZFC公理系统的整数分拆问题形式化证明：

### 1. 集合论基础定义

**定义 1.1 (整数分拆)** 对于自然数 $n \in \mathbb{N}$，定义 $n$ 的一个分拆 $\lambda$ 为满足条件 $\sum_{i=1}^k \lambda_i = n$ 且 $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_k \geq 1$ 的有序 $k$ 元组 $(\lambda_1, \lambda_2, \ldots, \lambda_k)$。

**定义 1.2 (分拆集合)** 定义 $P(n)$ 为整数 $n$ 的所有分拆构成的集合。形式化地：
$$P(n) = \{\lambda = (\lambda_1, \lambda_2, \ldots, \lambda_k) \mid \sum_{i=1}^k \lambda_i = n, \lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_k \geq 1, k \in \mathbb{N}\}$$

**定义 1.3 (分拆函数)** 定义分拆函数 $p: \mathbb{N} \to \mathbb{N}$，其中 $p(n) = |P(n)|$ 表示集合 $P(n)$ 的基数，即整数 $n$ 的不同分拆数量。

### 2. 生成函数的存在性证明

**定理 2.1 (生成函数表示)** 分拆函数 $p(n)$ 的生成函数可表示为无穷乘积：
$$\sum_{n=0}^{\infty} p(n)q^n = \prod_{m=1}^{\infty} \frac{1}{1-q^m}, \quad |q| < 1$$

**证明:**
我们使用ZFC公理中的无穷公理和集合存在公理构造证明。

首先，对于每个 $m \in \mathbb{N}^+$，考虑形式幂级数：
$$\frac{1}{1-q^m} = \sum_{j=0}^{\infty} q^{mj} = 1 + q^m + q^{2m} + q^{3m} + \cdots$$

这实际上是几何级数的和，当 $|q| < 1$ 时收敛。

考虑形式幂级数的无穷乘积：
$$\prod_{m=1}^{\infty} \frac{1}{1-q^m} = \prod_{m=1}^{\infty} \sum_{j=0}^{\infty} q^{mj}$$

根据集合论中的笛卡尔积运算，这个无穷乘积可以展开为：
$$\prod_{m=1}^{\infty} \frac{1}{1-q^m} = \sum_{j_1,j_2,\ldots \geq 0} q^{j_1 \cdot 1 + j_2 \cdot 2 + j_3 \cdot 3 + \cdots}$$

其中求和遍历所有非负整数序列 $(j_1, j_2, j_3, \ldots)$ 使得仅有有限个 $j_i$ 非零。

关键观察：对于 $n \in \mathbb{N}$，系数 $q^n$ 的次数对应于整数 $n$ 的分拆数。确切地说，每个形如 $n = 1 \cdot j_1 + 2 \cdot j_2 + 3 \cdot j_3 + \cdots$ 的表示，其中 $j_i$ 是非负整数，对应于将 $n$ 分拆为 $j_1$ 个 1，$j_2$ 个 2，$j_3$ 个 3 等。

因此 $q^n$ 的系数等于 $p(n)$，这完成了证明。$\square$

### 3. 分拆函数的递归性质

**定理 3.1 (分拆函数递归关系)** 分拆函数 $p(n)$ 满足以下递归关系：
$$p(n) = \sum_{k=1}^{\infty} (-1)^{k-1} \left[ p(n-k(3k-1)/2) + p(n-k(3k+1)/2) \right]$$
其中约定 $p(0) = 1$，且当 $m < 0$ 时 $p(m) = 0$。

**证明:**
基于欧拉五角形数定理：
$$\prod_{m=1}^{\infty} (1-q^m) = \sum_{k=-\infty}^{\infty} (-1)^k q^{k(3k-1)/2}$$

通过对分拆生成函数两边取倒数并展开，得到：
$$\prod_{m=1}^{\infty} \frac{1}{1-q^m} \cdot \sum_{k=-\infty}^{\infty} (-1)^k q^{k(3k-1)/2} = 1$$

展开左侧，并比较 $q^n$ 的系数，可得递归关系。具体地，等式左侧为：
$$\left(\sum_{n=0}^{\infty} p(n)q^n\right) \cdot \left(\sum_{k=-\infty}^{\infty} (-1)^k q^{k(3k-1)/2}\right) = 1$$

比较 $q^n$ 的系数，得到上述递归关系。$\square$

### 4. 分拆函数的渐近性质

**定理 4.1 (Hardy-Ramanujan 渐近公式)** 当 $n \to \infty$ 时，分拆函数 $p(n)$ 有以下渐近行为：
$$p(n) \sim \frac{1}{4n\sqrt{3}} \exp\left(\pi\sqrt{\frac{2n}{3}}\right)$$

**证明大纲:**
完整证明涉及复分析中的圆法(circle method)，此处给出大纲：
1. 将分拆生成函数表示为分析函数
2. 应用 Cauchy 积分公式表示 $p(n)$
3. 沿特殊路径评估积分，分析奇点的贡献
4. 通过复杂的渐近分析得到结果

形式化完整证明需要依赖于复分析理论，此处仅提供证明框架。$\square$

### 5. 分拆的同余性质

**定理 5.1 (Ramanujan 同余)** 对于所有非负整数 $k$，有：
$$p(5k+4) \equiv 0 \pmod 5$$
$$p(7k+5) \equiv 0 \pmod 7$$
$$p(11k+6) \equiv 0 \pmod{11}$$

**证明大纲:**
Ramanujan 同余的完整证明涉及模形式理论。基本思路是通过分析分拆生成函数在特定模变换下的行为，建立分拆数的同余关系。

具体证明步骤包括：
1. 引入模形式 $\eta$ 函数：$\eta(\tau) = q^{1/24} \prod_{n=1}^{\infty}(1-q^n)$，其中 $q = e^{2\pi i \tau}$
2. 研究特定幂次的 $\eta$ 函数在模变换下的行为
3. 利用 $\eta$ 函数与分拆生成函数的关系推导同余性

完整证明涉及高级数论和模形式理论，此处省略具体步骤。$\square$

The following is a formal proof of the integer partition problem based on the ZFC axiom system:

### 1. Set-Theoretic Foundations

**Definition 1.1 (Integer Partition)** For a natural number $n \in \mathbb{N}$, a partition $\lambda$ of $n$ is defined as an ordered $k$-tuple $(\lambda_1, \lambda_2, \ldots, \lambda_k)$ satisfying $\sum_{i=1}^k \lambda_i = n$ and $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_k \geq 1$.

**Definition 1.2 (Partition Set)** Define $P(n)$ as the set of all partitions of the integer $n$. Formally:
$$P(n) = \{\lambda = (\lambda_1, \lambda_2, \ldots, \lambda_k) \mid \sum_{i=1}^k \lambda_i = n, \lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_k \geq 1, k \in \mathbb{N}\}$$

**Definition 1.3 (Partition Function)** Define the partition function $p: \mathbb{N} \to \mathbb{N}$, where $p(n) = |P(n)|$ represents the cardinality of the set $P(n)$, i.e., the number of different partitions of the integer $n$.

### 2. Proof of Existence of the Generating Function

**Theorem 2.1 (Generating Function Representation)** The generating function of the partition function $p(n)$ can be represented as an infinite product:
$$\sum_{n=0}^{\infty} p(n)q^n = \prod_{m=1}^{\infty} \frac{1}{1-q^m}, \quad |q| < 1$$

**Proof:**
We construct the proof using the Axiom of Infinity and the Axiom of Set Existence from ZFC.

First, for each $m \in \mathbb{N}^+$, consider the formal power series:
$$\frac{1}{1-q^m} = \sum_{j=0}^{\infty} q^{mj} = 1 + q^m + q^{2m} + q^{3m} + \cdots$$

This is actually the sum of a geometric series, which converges when $|q| < 1$.

Consider the infinite product of formal power series:
$$\prod_{m=1}^{\infty} \frac{1}{1-q^m} = \prod_{m=1}^{\infty} \sum_{j=0}^{\infty} q^{mj}$$

According to the Cartesian product operation in set theory, this infinite product can be expanded as:
$$\prod_{m=1}^{\infty} \frac{1}{1-q^m} = \sum_{j_1,j_2,\ldots \geq 0} q^{j_1 \cdot 1 + j_2 \cdot 2 + j_3 \cdot 3 + \cdots}$$

where the sum is over all sequences of non-negative integers $(j_1, j_2, j_3, \ldots)$ such that only finitely many $j_i$ are non-zero.

Key observation: For $n \in \mathbb{N}$, the coefficient of $q^n$ corresponds to the number of partitions of the integer $n$. Specifically, each representation of the form $n = 1 \cdot j_1 + 2 \cdot j_2 + 3 \cdot j_3 + \cdots$, where $j_i$ are non-negative integers, corresponds to partitioning $n$ into $j_1$ 1's, $j_2$ 2's, $j_3$ 3's, etc.

Therefore, the coefficient of $q^n$ equals $p(n)$，这完成了证明。 $\square$

### 3. Recursive Properties of the Partition Function

**Theorem 3.1 (Recursive Relation of Partition Function)** The partition function $p(n)$ satisfies the following recursive relation:
$$p(n) = \sum_{k=1}^{\infty} (-1)^{k-1} \left[ p(n-k(3k-1)/2) + p(n-k(3k+1)/2) \right]$$
where it is stipulated that $p(0) = 1$, and $p(m) = 0$ when $m < 0$.

**Proof:**
Based on Euler's pentagonal number theorem:
$$\prod_{m=1}^{\infty} (1-q^m) = \sum_{k=-\infty}^{\infty} (-1)^k q^{k(3k-1)/2}$$

By taking the reciprocal of both sides of the partition generating function and expanding, we get:
$$\prod_{m=1}^{\infty} \frac{1}{1-q^m} \cdot \sum_{k=-\infty}^{\infty} (-1)^k q^{k(3k-1)/2} = 1$$

Expanding the left side and comparing the coefficients of $q^n$, we can derive the recursive relation. Specifically, the left side of the equation is:
$$\left(\sum_{n=0}^{\infty} p(n)q^n\right) \cdot \left(\sum_{k=-\infty}^{\infty} (-1)^k q^{k(3k-1)/2}\right) = 1$$

Comparing the coefficients of $q^n$, we obtain the above recursive relation. $\square$

### 4. Asymptotic Properties of the Partition Function

**Theorem 4.1 (Hardy-Ramanujan Asymptotic Formula)** As $n \to \infty$, the partition function $p(n)$ has the following asymptotic behavior:
$$p(n) \sim \frac{1}{4n\sqrt{3}} \exp\left(\pi\sqrt{\frac{2n}{3}}\right)$$

**Proof Outline:**
The complete proof involves the circle method in complex analysis, here is an outline:
1. Represent the partition generating function as an analytic function
2. Apply Cauchy's integral formula to represent $p(n)$
3. Evaluate the integral along a special path, analyzing the contributions of singularities
4. Obtain the result through complex asymptotic analysis

A formalized complete proof depends on complex analysis theory, only a proof framework is provided here. $\square$

### 5. Congruence Properties of Partitions

**Theorem 5.1 (Ramanujan Congruences)** For all non-negative integers $k$, we have:
$$p(5k+4) \equiv 0 \pmod 5$$
$$p(7k+5) \equiv 0 \pmod 7$$
$$p(11k+6) \equiv 0 \pmod{11}$$

**Proof Outline:**
The complete proof of Ramanujan congruences involves modular forms theory. The basic idea is to establish congruence relations of partition numbers by analyzing the behavior of the partition generating function under specific modular transformations.

Specific proof steps include:
1. Introduce the modular form $\eta$ function: $\eta(\tau) = q^{1/24} \prod_{n=1}^{\infty}(1-q^n)$, where $q = e^{2\pi i \tau}$
2. Study the behavior of specific powers of the $\eta$ function under modular transformations
3. Derive congruences using the relationship between the $\eta$ function and the partition generating function

The complete proof involves advanced number theory and modular forms theory, specific steps are omitted here. $\square$

## 量子经典二元论分析 | Quantum-Classical Dualism Analysis

从量子经典二元论视角，对整数分拆问题的分析如下：

### 步骤1：量子-经典表示映射

定义量子态 $|\psi\rangle_n$ 表示整数 $n$ 的量子能量表示，分拆则对应其经典表达：

$$
|\psi\rangle_n = \sum_{\lambda \vdash n} c_\lambda |\lambda\rangle
$$

其中 $\lambda \vdash n$ 表示 $\lambda$ 是 $n$ 的一个分拆，$|\lambda\rangle$ 是对应的基态，$c_\lambda$ 是复振幅。

分拆数则表示量子态 $|\psi\rangle_n$ 经典化路径数：

$$
p(n) = \text{量子态}|\psi\rangle_n\text{的经典化路径数}
$$

### 步骤2：量子-经典生成函数分析

从量子场论角度，分拆生成函数可解释为量子叠加态到经典态的转化函数：

$$
\prod_{m=1}^{\infty} \frac{1}{1-q^m} = \text{量子叠加态} \to \text{经典多路径表达的转换函数}
$$

这个生成函数的形式揭示了量子-经典转换的递归本质，每个因子 $\frac{1}{1-q^m}$ 代表一种量子能级对经典表达的贡献。

### 步骤3：五角形数定理的量子经典解读

欧拉的五角形数定理给出：

$$
\prod_{m=1}^{\infty} (1-q^m) = \sum_{k=-\infty}^{\infty} (-1)^k q^{k(3k-1)/2}
$$

从量子经典视角，这反映了量子-经典转换中的干涉现象：不同经典化路径之间存在相消干涉，导致奇数与偶数分拆之间的精确平衡结构。

### 步骤4：分拆函数渐近公式的熵分析

拉马努金-哈代渐近公式：

$$
p(n) \sim \frac{1}{4n\sqrt{3}} \exp\left(\pi\sqrt{\frac{2n}{3}}\right) \text{ 当 } n \to \infty
$$

从量子经典视角，这一公式揭示了量子态经典化路径数的熵增长规律：信息熵随量子态能量呈亚指数增长，这意味着量子-经典转换效率与系统能量（复杂度）有关。

### 步骤5：分拆恒等式的量子对称性解释

拉马努金发现的分拆恒等式：

$$
p(5k+4) \equiv 0 \pmod 5
$$

$$
p(7k+5) \equiv 0 \pmod 7
$$

从量子经典视角，这些同余性反映了量子纠缠结构在经典化过程中保持的周期性对称性，表明量子-经典转换遵循特定的模块化规律。

### 步骤6：量子信息熵与组合爆炸分析

分拆数的增长率反映了量子信息经典化时的熵爆炸现象：

$$
\lim_{n \to \infty} \frac{\log p(n)}{\sqrt{n}} = \pi\sqrt{\frac{2}{3}}
$$

这表明量子纠缠态（能量）经典化后的信息熵增长率由基本物理常数决定，再次验证了量子-经典映射的普适性规律。

From the quantum-classical dualism perspective, the analysis of the integer partition problem is as follows:

### Step 1: Quantum-Classical Representation Mapping

Define the quantum state $|\psi\rangle_n$ to represent the quantum energy representation of integer $n$, while partitions correspond to its classical expression:

$$
|\psi\rangle_n = \sum_{\lambda \vdash n} c_\lambda |\lambda\rangle
$$

where $\lambda \vdash n$ indicates that $\lambda$ is a partition of $n$, $|\lambda\rangle$ is the corresponding basis state, and $c_\lambda$ is the complex amplitude.

The partition number represents the number of classical paths of the quantum state $|\psi\rangle_n$:

$$
p(n) = \text{number of classical paths of quantum state }|\psi\rangle_n
$$

### Step 2: Quantum-Classical Generating Function Analysis

From the quantum field theory perspective, the partition generating function can be interpreted as the transformation function from quantum superposition states to classical states:

$$
\prod_{m=1}^{\infty} \frac{1}{1-q^m} = \text{quantum superposition state} \to \text{transformation function of classical multi-path expression}
$$

The form of this generating function reveals the recursive nature of quantum-classical transformation, with each factor $\frac{1}{1-q^m}$ representing the contribution of a quantum energy level to classical expression.

### Step 3: Quantum-Classical Interpretation of the Pentagonal Number Theorem

Euler's pentagonal number theorem gives:

$$
\prod_{m=1}^{\infty} (1-q^m) = \sum_{k=-\infty}^{\infty} (-1)^k q^{k(3k-1)/2}
$$

From the quantum-classical perspective, this reflects the interference phenomenon in quantum-classical transformation: destructive interference exists between different classical paths, leading to the precise balance structure between odd and even partitions.

### Step 4: Entropy Analysis of the Partition Function Asymptotic Formula

The Ramanujan-Hardy asymptotic formula:

$$
p(n) \sim \frac{1}{4n\sqrt{3}} \exp\left(\pi\sqrt{\frac{2n}{3}}\right) \text{ as } n \to \infty
$$

From the quantum-classical perspective, this formula reveals the entropy growth law of the number of classical paths of quantum states: information entropy grows sub-exponentially with quantum state energy, implying that quantum-classical transformation efficiency is related to system energy (complexity).

### Step 5: Quantum Symmetry Explanation of Partition Identities

Partition congruences discovered by Ramanujan:

$$
p(5k+4) \equiv 0 \pmod 5
$$

$$
p(7k+5) \equiv 0 \pmod 7
$$

From the quantum-classical perspective, these congruences reflect the periodic symmetry maintained by quantum entanglement structures during the classicalization process, indicating that quantum-classical transformation follows specific modular rules.

### Step 6: Quantum Information Entropy and Combinatorial Explosion Analysis

The growth rate of partition numbers reflects the entropy explosion phenomenon during the classicalization of quantum information:

$$
\lim_{n \to \infty} \frac{\log p(n)}{\sqrt{n}} = \pi\sqrt{\frac{2}{3}}
$$

This indicates that the information entropy growth rate after quantum entangled states (energy) are classicalized is determined by fundamental physical constants, further verifying the universality of quantum-classical mapping.

## 结论与预测 | Conclusion and Predictions

量子经典二元论为整数分拆提供了新的解释框架：分拆数的惊人性质源于量子态经典化路径的组合学特性，而分拆函数的各种恒等式反映了量子-经典转换过程中的信息保持与对称性。

### 量子经典预测

量子经典二元论对整数分拆做出以下预测：

1. 分拆函数的模运算性质将具有更深层次的理论解释，它们反映了量子信息经典化过程中的基本对称性
2. 新的分拆恒等式可能通过研究特定量子系统的经典化路径被发现
3. 限制条件下的分拆计数将与特定量子约束下的经典化路径计数直接对应
4. 量子计算可为解决大数分拆计数提供显著优势，因为它可以直接模拟量子-经典转换过程

Quantum-classical dualism provides a new interpretative framework for integer partitioning: the astonishing properties of partition numbers originate from the combinatorial characteristics of quantum state classicalization paths, while various identities of the partition function reflect information preservation and symmetry in the quantum-classical transformation process.

### Quantum-Classical Predictions

Quantum-classical dualism makes the following predictions about integer partitioning:

1. The modular arithmetic properties of the partition function will have deeper theoretical explanations, reflecting fundamental symmetries in the process of quantum information classicalization
2. New partition identities may be discovered by studying the classicalization paths of specific quantum systems
3. Counting partitions under restrictive conditions will directly correspond to counting classical paths under specific quantum constraints
4. Quantum computing can provide significant advantages for solving large number partition counting problems, as it can directly simulate the quantum-classical transformation process

## 参考文献 | References

1. Andrews, G. E. (1998). The theory of partitions. Cambridge University Press.
2. Hardy, G. H., & Ramanujan, S. (1918). Asymptotic formulae in combinatory analysis. Proceedings of the London Mathematical Society, 2(1), 75-115.
3. Rademacher, H. (1937). On the partition function p(n). Proceedings of the London Mathematical Society, 2(1), 241-254.
4. Ahlgren, S., & Boylan, M. (2003). Arithmetic properties of the partition function. Inventiones mathematicae, 153(3), 487-502.
5. Ono, K. (2000). Distribution of the partition function modulo m. Annals of Mathematics, 151(1), 293-307.
6. 量子经典二元论核心理论文献 [29.0].
7. Quantum-Classical Dualism Core Theory Documentation [29.0]. 