#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quantum Interference Simulation for XOR-SHIFT Paper
===================================================

This simulation demonstrates quantum interference patterns
predicted by the XOR-SHIFT framework, focusing on information
preservation during measurement processes.

Author: Auric
Version: v38.0
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
import argparse

# ======================================================================
# XOR-SHIFT Operations Implementation
# ======================================================================

def xor_operation(state_a, state_b):
    """
    Implements the XOR operation between two quantum states.
    
    Parameters:
        state_a, state_b: Complex-valued numpy arrays representing quantum states
        
    Returns:
        Complex-valued numpy array representing the XOR result
    """
    # Information differential in amplitude and phase
    amp_diff = np.abs(state_a) - np.abs(state_b)
    phase_a = np.angle(state_a)
    phase_b = np.angle(state_b)
    phase_diff = np.mod(phase_a - phase_b + np.pi, 2*np.pi) - np.pi
    
    # Construct the XOR state
    xor_state = amp_diff * np.exp(1j * phase_diff)
    
    # Normalize
    if np.linalg.norm(xor_state) > 0:
        xor_state = xor_state / np.linalg.norm(xor_state)
    
    return xor_state

def shift_operation(state, operator):
    """
    Implements the SHIFT operation on a quantum state.
    
    Parameters:
        state: Complex-valued numpy array representing quantum state
        operator: Complex-valued numpy matrix representing the SHIFT operator
        
    Returns:
        Complex-valued numpy array representing the shifted state
    """
    # Apply the operator
    shifted_state = np.dot(operator, state)
    
    # Normalize
    shifted_state = shifted_state / np.linalg.norm(shifted_state)
    
    return shifted_state

# ======================================================================
# Quantum Interference Simulation
# ======================================================================

def simulate_quantum_interference(num_steps=100, measurement_strength=0.1, 
                                  plot_results=True):
    """
    Simulates quantum interference with weak measurements
    under the XOR-SHIFT framework.
    
    Parameters:
        num_steps: Number of simulation steps
        measurement_strength: Strength of weak measurements (0-1)
        plot_results: Whether to generate plots
        
    Returns:
        Dictionary containing simulation results
    """
    # Initialize system
    dim = 2  # Two-level system (qubit)
    initial_state = np.array([1.0, 0.0])  # |0⟩ state
    
    # Prepare superposition
    hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    state = np.dot(hadamard, initial_state)
    
    # Reference state for XOR representation
    reference_state = initial_state
    
    # Time evolution operator
    H = np.array([[0, 1], [1, 0]])  # Pauli-X as Hamiltonian
    dt = 0.1
    U = expm(-1j * H * dt)
    
    # Measurement operators (weak Z-measurement)
    M0 = np.array([[1, 0], [0, np.sqrt(1-measurement_strength)]])
    M1 = np.array([[0, 0], [0, np.sqrt(measurement_strength)]])
    
    # Initialize arrays for tracking
    states = np.zeros((num_steps, dim), dtype=complex)
    xor_states = np.zeros((num_steps, dim), dtype=complex)
    measurement_results = np.zeros(num_steps)
    information_preservation = np.zeros(num_steps)
    
    # Run simulation
    for i in range(num_steps):
        # Store current state
        states[i] = state
        
        # Calculate XOR representation
        xor_states[i] = xor_operation(state, reference_state)
        
        # Perform weak measurement
        p1 = np.abs(np.dot(M1, state))**2
        p0 = np.abs(np.dot(M0, state))**2
        
        if np.random.random() < p1.sum():
            # Outcome 1
            state = np.dot(M1, state) / np.sqrt(p1.sum())
            measurement_results[i] = 1
        else:
            # Outcome 0
            state = np.dot(M0, state) / np.sqrt(p0.sum())
            measurement_results[i] = 0
            
        # Calculate time evolution
        state = np.dot(U, state)
        
        # Calculate information preservation
        original_xor = xor_operation(states[0], reference_state)
        current_xor = xor_operation(state, reference_state)
        information_preservation[i] = np.abs(np.vdot(original_xor, current_xor))**2
    
    # Generate results
    results = {
        'states': states,
        'xor_states': xor_states,
        'measurement_results': measurement_results,
        'information_preservation': information_preservation,
        'parameters': {
            'num_steps': num_steps,
            'measurement_strength': measurement_strength
        }
    }
    
    # Generate plots if requested
    if plot_results:
        plot_simulation_results(results)
    
    return results

def plot_simulation_results(results):
    """
    Plot the simulation results.
    
    Parameters:
        results: Dictionary containing simulation results
    """
    states = results['states']
    xor_states = results['xor_states']
    measurement_results = results['measurement_results']
    information_preservation = results['information_preservation']
    num_steps = results['parameters']['num_steps']
    measurement_strength = results['parameters']['measurement_strength']
    
    # Create figure
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), dpi=100)
    
    # Time steps
    time_steps = np.arange(num_steps)
    
    # Plot state evolution
    axes[0].plot(time_steps, np.abs(states[:, 0])**2, 'b-', label='|⟨0|ψ⟩|²')
    axes[0].plot(time_steps, np.abs(states[:, 1])**2, 'r-', label='|⟨1|ψ⟩|²')
    axes[0].set_xlabel('Time Step')
    axes[0].set_ylabel('Probability')
    axes[0].set_title('Quantum State Evolution')
    axes[0].legend()
    axes[0].grid(True)
    
    # Plot XOR representation
    axes[1].plot(time_steps, np.abs(xor_states[:, 0])**2, 'g-', label='|⟨0|ψ⊕ref⟩|²')
    axes[1].plot(time_steps, np.abs(xor_states[:, 1])**2, 'm-', label='|⟨1|ψ⊕ref⟩|²')
    axes[1].set_xlabel('Time Step')
    axes[1].set_ylabel('XOR Information')
    axes[1].set_title('XOR Representation Evolution')
    axes[1].legend()
    axes[1].grid(True)
    
    # Plot information preservation
    axes[2].plot(time_steps, information_preservation, 'k-')
    axes[2].plot(time_steps, np.ones(num_steps) * (1 - measurement_strength)**2, 'r--', 
                 label='Standard QM prediction')
    axes[2].plot(time_steps, np.ones(num_steps) * np.exp(-measurement_strength * time_steps / 10), 'g--',
                 label='XOR-SHIFT prediction')
    axes[2].set_xlabel('Time Step')
    axes[2].set_ylabel('Information Preservation Ratio')
    axes[2].set_title('Information Preservation During Measurement')
    axes[2].set_ylim(0, 1.05)
    axes[2].legend()
    axes[2].grid(True)
    
    # Add measurement markers
    for i, result in enumerate(measurement_results):
        if result > 0:
            axes[0].axvline(x=i, color='gray', linestyle=':', alpha=0.3)
            axes[1].axvline(x=i, color='gray', linestyle=':', alpha=0.3)
            axes[2].axvline(x=i, color='gray', linestyle=':', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('quantum_interference_simulation.png', dpi=300)
    
    # Display prediction comparison
    final_ipr = information_preservation[-1]
    standard_qm = (1 - measurement_strength)**(num_steps/10)
    xor_shift = np.exp(-measurement_strength * num_steps / 10)
    
    print(f"Final Information Preservation Ratio: {final_ipr:.4f}")
    print(f"Standard QM prediction: {standard_qm:.4f}")
    print(f"XOR-SHIFT prediction: {xor_shift:.4f}")
    print(f"Deviation from standard QM: {(final_ipr - standard_qm):.4f}")
    print(f"Deviation from XOR-SHIFT: {(final_ipr - xor_shift):.4f}")

# ======================================================================
# Main Execution
# ======================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Quantum Interference Simulation')
    parser.add_argument('--steps', type=int, default=100,
                        help='Number of simulation steps')
    parser.add_argument('--strength', type=float, default=0.1,
                        help='Measurement strength (0-1)')
    parser.add_argument('--no-plot', action='store_true',
                        help='Disable plotting')
    
    args = parser.parse_args()
    
    print("XOR-SHIFT Quantum Interference Simulation")
    print("=========================================")
    print(f"Steps: {args.steps}, Measurement Strength: {args.strength}")
    
    results = simulate_quantum_interference(
        num_steps=args.steps,
        measurement_strength=args.strength,
        plot_results=not args.no_plot
    )
    
    # Example output of observables for the paper
    print("\nXOR-SHIFT Framework Predictions:")
    print("---------------------------------")
    final_ipr = results['information_preservation'][-1]
    expected_ipr = np.exp(-args.strength * args.steps / 10)
    print(f"Information Preservation Ratio: {final_ipr:.4f} (expected: {expected_ipr:.4f})")
    
    # Sample state in standard and XOR representations
    mid_idx = args.steps // 2
    mid_state = results['states'][mid_idx]
    mid_xor = results['xor_states'][mid_idx]
    
    print("\nSample State Representations:")
    print(f"Standard: |ψ⟩ = ({mid_state[0]:.4f})|0⟩ + ({mid_state[1]:.4f})|1⟩")
    print(f"XOR: |ψ⊕ref⟩ = ({mid_xor[0]:.4f})|0⟩ + ({mid_xor[1]:.4f})|1⟩") 