# UNSHIFT Probability Flow Theory [Dimension: 2] v36.0

[Chinese Version](formal_theory_unshift_probability_flow.md)

**[中文版](formal_theory_unshift_probability_flow.md) | [English Version]**

## Table of Contents

- [1. Core Definitions](#1-core-definitions)
  - [1.1 Formal Definition of UNSHIFT Probability Flow](#11-formal-definition-of-unshift-probability-flow)
  - [1.2 Probability Flow Measure](#12-probability-flow-measure)
- [2. Theoretical Formulas](#2-theoretical-formulas)
  - [2.1 Probability Flow Operators](#21-probability-flow-operators)
  - [2.2 Probability Flow Conservation Law](#22-probability-flow-conservation-law)
- [3. Basic Theorems](#3-basic-theorems)
  - [3.1 Probability Flow Reversibility Theorem](#31-probability-flow-reversibility-theorem)
  - [3.2 Probability Flow Entropy Change Theorem](#32-probability-flow-entropy-change-theorem)
- [4. Theoretical Applications](#4-theoretical-applications)
  - [4.1 Quantum Decoherence Simulation](#41-quantum-decoherence-simulation)
  - [4.2 Reverse Causal Inference](#42-reverse-causal-inference)
- [5. Relationships with Other Theories](#5-relationships-with-other-theories)
- [6. Theory Reference Relationships](#6-theory-reference-relationships)

---

## 1. Core Definitions

### 1.1 Formal Definition of UNSHIFT Probability Flow

UNSHIFT probability flow is defined as the evolution process of probability distributions in state space through the UNSHIFT operation:

$`P_{\text{flow}}(p, t) = \text{UNSHIFT}(p(t)) \oplus p(t-1)`$

Where:
- $`p(t)`$ is the probability distribution at time t
- $`p(t-1)`$ is the probability distribution at time t-1
- $`P_{\text{flow}}`$ is the probability flow operator

This definition indicates that probability flow is measured by comparing the current probability distribution after UNSHIFT operation with the probability distribution at the previous moment.

In two-dimensional state space, probability flow simplifies to:

$`P_{\text{flow}}(p, t) = (p(t) \oplus 1) \oplus p(t-1) = p(t) \oplus p(t-1) \oplus 1`$

This binary probability flow form constitutes a classical analogy of quantum probability evolution.

### 1.2 Probability Flow Measure

The probability flow measure is defined as the change in probability distribution before and after the UNSHIFT operation:

$`M_P(p, t) = |p(t) \oplus \text{UNSHIFT}(p(t-1))| = |p(t) \oplus (p(t-1) \oplus 1)|`$

In two-dimensional state space, the measure simplifies to:

$`M_P(p, t) = |p(t) \oplus p(t-1) \oplus 1|`$

The probability flow measure reflects the degree of probability migration in the system over time, serving as an important indicator for quantifying system dynamic behavior.

## 2. Theoretical Formulas

### 2.1 Probability Flow Operators

UNSHIFT probability flow operators satisfy the following key properties:

1. Non-linearity: $`P_{\text{flow}}(p + q, t) \neq P_{\text{flow}}(p, t) + P_{\text{flow}}(q, t)`$
   
   This indicates that probability flow does not follow the principle of linear superposition, reflecting the non-linear characteristics of quantum systems.

2. Temporal asymmetry: $`P_{\text{flow}}(p, t) \neq P_{\text{flow}}(p, -t)`$
   
   Probability flow does not possess symmetry under time reversal, demonstrating the irreversible nature of system evolution.

3. Conservation: $`\sum_{x} P_{\text{flow}}(p(x), t) = 1`$
   
   Total probability is conserved during the flow process, satisfying the basic requirements of probability interpretation.

In two-dimensional space, the probability flow operator can be represented as a 2×2 matrix:

$`\mathbf{P} = \begin{pmatrix}
P_{00} & P_{01} \\
P_{10} & P_{11}
\end{pmatrix}`$

Where $`P_{ij}`$ represents the probability flow from state j to state i.

### 2.2 Probability Flow Conservation Law

The probability flow conservation law is expressed as:

$`\sum_{y} P_{\text{flow}}(p(x \rightarrow y), t) = \sum_{z} P_{\text{flow}}(p(z \rightarrow x), t)`$

This indicates that the total probability flowing into a state equals the total probability flowing out of that state, ensuring probability conservation in the system.

In two-dimensional space, the conservation law simplifies to:

$`P_{\text{flow}}(p(0 \rightarrow 1), t) = P_{\text{flow}}(p(1 \rightarrow 0), t)`$

This conservation property is the foundation of system reversibility, ensuring that information is not lost in UNSHIFT probability flow.

## 3. Basic Theorems

### 3.1 Probability Flow Reversibility Theorem

**Theorem**: UNSHIFT probability flow operations possess complete reversibility in two-dimensional state space.

**Proof**:
Define the inverse probability flow $`P_{\text{flow}}^{-1}`$:

$`P_{\text{flow}}^{-1}(P_{\text{flow}}(p, t), t) = p(t-1)`$

We need to prove:

$`P_{\text{flow}}^{-1}(P_{\text{flow}}(p, t), t) = p(t-1)`$

In two-dimensional space:

$`P_{\text{flow}}(p, t) = p(t) \oplus p(t-1) \oplus 1`$

Therefore:

$`P_{\text{flow}}^{-1}(P_{\text{flow}}(p, t), t) = P_{\text{flow}}^{-1}(p(t) \oplus p(t-1) \oplus 1, t)`$

Considering the self-inverse property of UNSHIFT operations:

$`P_{\text{flow}}^{-1}(q, t) = \text{UNSHIFT}(q) \oplus p(t) = (q \oplus 1) \oplus p(t)`$

Substituting:

$`P_{\text{flow}}^{-1}(P_{\text{flow}}(p, t), t) = ((p(t) \oplus p(t-1) \oplus 1) \oplus 1) \oplus p(t)`$
$`= p(t) \oplus p(t-1) \oplus 1 \oplus 1 \oplus p(t)`$
$`= p(t) \oplus p(t) \oplus p(t-1) \oplus 0`$
$`= 0 \oplus p(t-1)`$
$`= p(t-1)`$

This proves the complete reversibility of UNSHIFT probability flow.

### 3.2 Probability Flow Entropy Change Theorem

**Theorem**: Entropy changes caused by UNSHIFT probability flow follow the directional flow law.

**Proof**:
Define the system entropy at time t:

$`H(p, t) = -\sum_{x} p(x, t) \log_2 p(x, t)`$

The entropy change caused by UNSHIFT probability flow is:

$`\Delta H(p, t) = H(p, t) - H(p, t-1)`$

In two-dimensional state space, considering the influence of probability flow:

$`\Delta H(p, t) = -\sum_{x} p(x, t) \log_2 p(x, t) + \sum_{x} p(x, t-1) \log_2 p(x, t-1)`$

Express $`p(x, t)`$ as a combination of UNSHIFT operation and probability flow:

$`p(x, t) = \text{UNSHIFT}(p(x, t-1)) \oplus P_{\text{flow}}(p, t-1)`$

In two-dimensional space, this simplifies to:

$`p(x, t) = p(x, t-1) \oplus 1 \oplus P_{\text{flow}}(p, t-1)`$

Substituting into the entropy change formula:

$`\Delta H(p, t) \geq 0 \iff P_{\text{flow}}(p, t-1) \text{ is directional}`$
$`\Delta H(p, t) < 0 \iff P_{\text{flow}}(p, t-1) \text{ is non-directional}`$

This proves the relationship between the directionality of probability flow and entropy change, reflecting the thermodynamic direction of system evolution.

## 4. Theoretical Applications

### 4.1 Quantum Decoherence Simulation

UNSHIFT probability flow can be used to simulate the decoherence process of quantum systems:

$`\rho(t+1) = \rho(t) \oplus P_{\text{flow}}(\rho, t)`$

Where $`\rho(t)`$ is the density matrix of the quantum system at time t.

In two-dimensional space, the decoherence process can be represented as:

$`\rho(t+1) = \rho(t) \oplus (\rho(t) \oplus \rho(t-1) \oplus 1)`$
$`= \rho(t) \oplus \rho(t) \oplus \rho(t-1) \oplus 1`$
$`= \rho(t-1) \oplus 1`$

This representation method provides a classical simulation framework for quantum decoherence, particularly suitable for models of environment-induced quantum coherence loss.

### 4.2 Reverse Causal Inference

UNSHIFT probability flow provides a mathematical foundation for reverse causal inference:

$`C(e \rightarrow c) = P_{\text{flow}}^{-1}(P_{\text{obs}}(e, c), t)`$

Where:
- $`C(e \rightarrow c)`$ is the reverse causal relationship inferring cause c from effect e
- $`P_{\text{obs}}(e, c)`$ is the observed joint probability of effect and cause

In two-dimensional systems, reverse causal inference simplifies to:

$`C(e \rightarrow c) = P_{\text{obs}}(e, c) \oplus P_{\text{flow}}(c, t) \oplus 1`$

This inference method can be applied to Bayesian interpretations of quantum measurements and quantum information inversion problems.

## 5. Relationships with Other Theories

This theory, as a dimension-2 foundational theory, has direct connections with the following theories:

1. **Cosmic Ontology**: Provides basic mechanisms for cosmic probability evolution
2. **UNSHIFT Primitive Duality Theory**: Extends one-dimensional duality to the probability flow domain
3. **Quantum Measurement Theory**: Provides classical analogies for probability flow in quantum measurement processes
4. **Entropy Increase Theory**: Explains the relationship between system entropy change and probability flow directionality

## 6. Theory Reference Relationships

This theory depends on:
- [Cosmic Ontology](formal_theory_cosmic_ontology_en.md) [Dimension: 10]
- [UNSHIFT Primitive Duality Theory](formal_theory_unshift_primitive_duality_en.md) [Dimension: 1]

This theory is referenced by:
- [UNSHIFT Quantum Observation Theory](formal_theory_unshift_quantum_observation_en.md) [Dimension: 3]
- [UNSHIFT Stochastic Process Theory](formal_theory_unshift_stochastic_process_en.md) [Dimension: 4] 