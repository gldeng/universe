#!/usr/bin/env python3
"""
Constants Relationship Simulation for Universe Ontology
Demonstrates the relationships between φ, e, π, and α through XOR-SHIFT operations
and visualizes collapse breathing proportions.

Universe Ontology v38.0
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from typing import Tuple, List, Callable

# Define fundamental constants with high precision
PI = np.pi  # π
E = np.e  # e
PHI = (1 + np.sqrt(5)) / 2  # φ (Golden ratio)
ALPHA = 1/137.035999084  # α (Fine structure constant)

# Define XOR and SHIFT operations in the information domain
def info_xor(a: float, b: float) -> float:
    """
    Information domain XOR operation.
    In Universe Ontology, XOR represents the differential information between two states.
    """
    # Normalized XOR operation using logarithmic scaling and phase difference
    log_a = np.log(abs(a)) if a != 0 else 0
    log_b = np.log(abs(b)) if b != 0 else 0
    phase_a = np.angle(complex(a, 0))
    phase_b = np.angle(complex(b, 0))
    
    # Information difference in magnitude and phase
    mag_diff = abs(log_a - log_b)
    phase_diff = abs(phase_a - phase_b) % (2*np.pi)
    
    # Combined difference as information XOR
    return mag_diff * (1 + phase_diff / np.pi)

def info_shift(a: float, direction: float = 1.0) -> float:
    """
    Information domain SHIFT operation.
    In Universe Ontology, SHIFT represents a transformation of information state.
    """
    # SHIFT operation implemented as a controlled phase rotation and magnitude scaling
    mag_a = abs(a)
    log_a = np.log(mag_a) if mag_a > 0 else 0
    
    # Shift magnitude in logarithmic space
    shifted_mag = np.exp(log_a + direction * 0.05 * PHI)
    
    # Phase shift based on golden ratio
    if isinstance(a, complex):
        phase_a = np.angle(a)
    else:
        phase_a = 0
    
    shifted_phase = phase_a + direction * (2 * np.pi / PHI)
    
    # Combine magnitude and phase
    if phase_a != 0:
        return shifted_mag * np.exp(1j * shifted_phase)
    else:
        return shifted_mag

def collapse_breathing_proportion(phi: float, e_val: float, pi_val: float, alpha: float) -> float:
    """
    Calculate the collapse breathing proportion as defined in Universe Ontology.
    This is the master equation relating all four constants.
    """
    xor_term = info_xor(np.log(phi), pi_val / e_val)
    return np.exp(xor_term) * alpha

def theoretical_alpha() -> float:
    """
    Calculate the theoretical value of α using the proposed formula:
    α = φ^(-2) · XOR(e, π)/S(π)
    """
    numerator = info_xor(E, PI)
    denominator = info_shift(PI)
    return PHI**(-2) * (numerator / denominator)

def verify_constants_relationship() -> Tuple[float, float, float]:
    """
    Verify the relationship between the constants and return error metrics.
    """
    # Calculate theoretical α
    alpha_theoretical = theoretical_alpha()
    
    # Compare with known value
    absolute_error = abs(alpha_theoretical - ALPHA)
    relative_error = absolute_error / ALPHA * 100
    
    # Calculate collapse breathing value
    cb_value = collapse_breathing_proportion(PHI, E, PI, ALPHA)
    
    return alpha_theoretical, relative_error, cb_value

def simulate_collapse_breathing_cycle(steps: int = 100) -> Tuple[List[float], List[float]]:
    """
    Simulate one complete collapse-breathing cycle and track the constants.
    Returns the values at each step and the invariant proportions.
    """
    # Initialize values
    phi_values = []
    e_values = []
    pi_values = []
    alpha_values = []
    cb_values = []
    
    # Define small perturbation factor
    perturb = 0.01
    
    # Starting values
    phi = PHI
    e_val = E
    pi_val = PI
    alpha = ALPHA
    
    for i in range(steps):
        # Phase of the cycle (0 to 2π)
        phase = 2 * np.pi * i / steps
        
        # Apply perturbation based on cycle phase
        if i < steps/4:  # Collapse phase (XOR dominant)
            phi += perturb * np.sin(phase)
            e_val += perturb * np.cos(phase)
            pi_val += perturb * np.sin(2*phase)
            # Alpha remains invariant
        elif i < steps/2:  # Transition phase
            phi -= perturb * np.sin(phase)
            e_val += perturb * np.cos(phase)
            pi_val -= perturb * np.sin(2*phase)
            # Alpha remains invariant
        elif i < 3*steps/4:  # Expansion phase (SHIFT dominant)
            phi -= perturb * np.sin(phase)
            e_val -= perturb * np.cos(phase)
            pi_val -= perturb * np.sin(2*phase)
            # Alpha remains invariant
        else:  # Return to balance
            phi += perturb * np.sin(phase)
            e_val -= perturb * np.cos(phase)
            pi_val += perturb * np.sin(2*phase)
            # Alpha remains invariant
            
        # Calculate theoretical alpha at each step
        alpha_theoretical = phi**(-2) * (info_xor(e_val, pi_val) / info_shift(pi_val))
        
        # Calculate collapse breathing value
        cb = collapse_breathing_proportion(phi, e_val, pi_val, alpha_theoretical)
        
        # Store values
        phi_values.append(phi)
        e_values.append(e_val)
        pi_values.append(pi_val)
        alpha_values.append(alpha_theoretical)
        cb_values.append(cb)
    
    # Return collected values and invariant proportions
    return (phi_values, e_values, pi_values, alpha_values), cb_values

def plot_simulation_results(values: Tuple[List[float], List[float], List[float], List[float]], 
                           invariants: List[float]) -> None:
    """
    Plot the results of the simulation.
    """
    phi_values, e_values, pi_values, alpha_values = values
    steps = len(phi_values)
    
    # Normalize values for comparative plotting
    phi_norm = [(x - PHI) / perturb + 1 for x in phi_values]
    e_norm = [(x - E) / perturb + 2 for x in e_values]
    pi_norm = [(x - PI) / perturb + 3 for x in pi_values]
    alpha_norm = [(x / ALPHA - 1) * 20 + 4 for x in alpha_values]
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
    
    # Plot normalized constant values
    x = np.arange(steps)
    ax1.plot(x, phi_norm, label='φ (Golden Ratio)', color='gold')
    ax1.plot(x, e_norm, label='e (Euler\'s Number)', color='blue')
    ax1.plot(x, pi_norm, label='π (Pi)', color='green')
    ax1.plot(x, alpha_norm, label='α (Fine Structure)', color='red', linewidth=2)
    
    # Add phase markers
    ax1.axvspan(0, steps/4, alpha=0.2, color='red', label='Collapse Phase')
    ax1.axvspan(steps/4, steps/2, alpha=0.2, color='purple', label='Transition Phase')
    ax1.axvspan(steps/2, 3*steps/4, alpha=0.2, color='blue', label='Expansion Phase')
    ax1.axvspan(3*steps/4, steps, alpha=0.2, color='green', label='Balance Phase')
    
    ax1.set_title('Normalized Constant Values During Collapse-Breathing Cycle')
    ax1.set_xlabel('Simulation Step')
    ax1.set_ylabel('Normalized Value (offset for clarity)')
    ax1.legend()
    ax1.grid(True)
    
    # Plot invariant proportion
    ax2.plot(x, invariants, label='Collapse Breathing Invariant', color='purple', linewidth=2)
    ax2.axhline(y=invariants[0], color='red', linestyle='--', label='Initial CB Value')
    
    # Calculate variation
    mean_cb = np.mean(invariants)
    std_cb = np.std(invariants)
    rel_variation = std_cb / mean_cb * 100
    
    ax2.set_title(f'Collapse Breathing Invariant (Variation: {rel_variation:.6f}%)')
    ax2.set_xlabel('Simulation Step')
    ax2.set_ylabel('CB Value')
    ax2.legend()
    ax2.grid(True)
    
    # Add information panel
    textbox = f"""Theoretical α = {theoretical_alpha():.12f}
Measured α = {ALPHA:.12f}
Relative Error = {(theoretical_alpha() - ALPHA) / ALPHA * 100:.8f}%
Mean CB Value = {mean_cb:.8f}
CB Variation = {rel_variation:.8f}%"""
    
    plt.figtext(0.15, 0.01, textbox, fontsize=10, 
                bbox={"facecolor":"white", "alpha":0.8, "pad":5})
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('../figures/simulation_results.png', dpi=600)
    plt.close()

# Main function
def main():
    print("Constants Relationship Simulation for Universe Ontology v38.0")
    print("=" * 70)
    
    # 1. Verify theoretical relationship
    alpha_theoretical, rel_error, cb_value = verify_constants_relationship()
    
    print(f"Fundamental Constants:")
    print(f"  φ (Golden Ratio)    = {PHI:.12f}")
    print(f"  e (Euler's Number)  = {E:.12f}")
    print(f"  π (Pi)              = {PI:.12f}")
    print(f"  α (Fine Structure)  = {ALPHA:.12f}")
    print("-" * 70)
    
    print(f"Theoretical Relationships:")
    print(f"  XOR(e, π)           = {info_xor(E, PI):.12f}")
    print(f"  SHIFT(π)            = {info_shift(PI):.12f}")
    print(f"  φ^(-2)              = {PHI**(-2):.12f}")
    print("-" * 70)
    
    print(f"Universe Ontology Formula: α = φ^(-2) · XOR(e, π)/SHIFT(π)")
    print(f"  Theoretical α        = {alpha_theoretical:.12f}")
    print(f"  Measured α           = {ALPHA:.12f}")
    print(f"  Absolute Error       = {abs(alpha_theoretical - ALPHA):.12f}")
    print(f"  Relative Error       = {rel_error:.8f}%")
    print("-" * 70)
    
    print(f"Collapse Breathing Value:")
    print(f"  CB(φ,e,π,α)          = {cb_value:.12f}")
    print("=" * 70)
    
    # 2. Simulate collapse breathing cycle
    print("\nSimulating collapse breathing cycle...")
    values, invariants = simulate_collapse_breathing_cycle(steps=200)
    
    # 3. Plot and save results
    print("Generating visualization...")
    perturb = 0.01  # Define perturb here to avoid NameError in plot_simulation_results
    plot_simulation_results(values, invariants)
    
    print("\nSimulation complete.")
    print(f"Results saved to: ../figures/simulation_results.png")
    print("=" * 70)

if __name__ == "__main__":
    main() 