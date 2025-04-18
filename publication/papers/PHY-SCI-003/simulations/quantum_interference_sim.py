#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quantum Interference Simulation for Information Ontology Paper
Author: Auric
Date: April 18, 2025
Version: 1.0

This script simulates quantum interference patterns in a double-slit experiment,
comparing standard quantum mechanics predictions with information ontology predictions.
It also generates synthetic experimental data for preliminary testing of the theory.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy import optimize
import os
import argparse
from datetime import datetime

# Physical constants
HBAR = 1.054571817e-34  # Reduced Planck constant (J·s)
C = 299792458  # Speed of light (m/s)
M_ELECTRON = 9.1093837015e-31  # Electron mass (kg)

# Information ontology coupling constant (predicted value)
ALPHA_THEORY = 1.35e-15  # m²

def psi_double_slit(x, wavelength, slit_distance, slit_width):
    """
    Calculate the wavefunction for a double-slit experiment.
    
    Parameters:
    -----------
    x : array
        Position array (m)
    wavelength : float
        De Broglie wavelength of particles (m)
    slit_distance : float
        Distance between slits (m)
    slit_width : float
        Width of each slit (m)
        
    Returns:
    --------
    psi : array
        Complex wavefunction
    """
    k = 2 * np.pi / wavelength
    
    # Single slit diffraction function
    def sinc(x):
        return np.where(x == 0, 1.0, np.sin(x) / x)
    
    # Diffraction from each slit
    psi1 = sinc(k * slit_width * (x + slit_distance/2) / 2) * np.exp(1j * k * (x + slit_distance/2))
    psi2 = sinc(k * slit_width * (x - slit_distance/2) / 2) * np.exp(1j * k * (x - slit_distance/2))
    
    # Total wavefunction (superposition)
    psi = (psi1 + psi2) / np.sqrt(2)
    
    return psi

def standard_qm_probability(x, wavelength, slit_distance, slit_width):
    """
    Calculate the probability density according to standard quantum mechanics.
    
    Parameters:
    -----------
    x : array
        Position array (m)
    wavelength : float
        De Broglie wavelength of particles (m)
    slit_distance : float
        Distance between slits (m)
    slit_width : float
        Width of each slit (m)
        
    Returns:
    --------
    prob : array
        Probability density
    """
    psi = psi_double_slit(x, wavelength, slit_distance, slit_width)
    return np.abs(psi)**2

def info_ontology_probability(x, wavelength, slit_distance, slit_width, alpha):
    """
    Calculate the probability density according to information ontology.
    Includes the characteristic second derivative term.
    
    Parameters:
    -----------
    x : array
        Position array (m)
    wavelength : float
        De Broglie wavelength of particles (m)
    slit_distance : float
        Distance between slits (m)
    slit_width : float
        Width of each slit (m)
    alpha : float
        Information coupling constant (m²)
        
    Returns:
    --------
    prob : array
        Modified probability density
    """
    # Standard QM probability
    psi = psi_double_slit(x, wavelength, slit_distance, slit_width)
    prob_std = np.abs(psi)**2
    
    # Numerical second derivative of probability
    dx = x[1] - x[0]
    d2_prob = np.gradient(np.gradient(prob_std, dx), dx)
    
    # Information ontology modification
    prob_info = prob_std + alpha * d2_prob
    
    # Ensure probability is non-negative and normalized
    prob_info = np.maximum(prob_info, 0)
    prob_info = prob_info / np.trapz(prob_info, x)
    
    return prob_info

def generate_synthetic_data(x, true_prob, num_points=100, noise_level=0.05):
    """
    Generate synthetic experimental data based on a true probability
    distribution with added noise.
    
    Parameters:
    -----------
    x : array
        Position array (m)
    true_prob : array
        True probability density
    num_points : int
        Number of data points to generate
    noise_level : float
        Relative noise level
        
    Returns:
    --------
    x_data : array
        x coordinates of data points
    y_data : array
        y values (counts) of data points
    y_err : array
        Error bars for y values
    """
    # Sample positions randomly with bias toward high-probability regions
    x_data = np.random.choice(x, size=num_points, p=true_prob/np.sum(true_prob))
    
    # Sort for better visualization
    x_data = np.sort(x_data)
    
    # Calculate true probability at these points (with interpolation)
    y_true = np.interp(x_data, x, true_prob)
    
    # Add Poisson noise
    counts = np.random.poisson(1000 * y_true)
    y_data = counts / 1000
    
    # Error bars based on Poisson statistics
    y_err = np.sqrt(counts) / 1000
    
    return x_data, y_data, y_err

def fit_alpha_parameter(x_data, y_data, y_err, x_full, wavelength, slit_distance, slit_width):
    """
    Fit the information coupling constant alpha to experimental data.
    
    Parameters:
    -----------
    x_data, y_data, y_err : arrays
        Experimental data points and errors
    x_full : array
        Full position array for theoretical curves
    wavelength, slit_distance, slit_width : float
        Experimental parameters
        
    Returns:
    --------
    alpha_fit : float
        Best-fit value for alpha parameter
    alpha_err : float
        Error estimate for alpha
    """
    def residual(alpha):
        # Interpolate theoretical prediction to data points
        theory_full = info_ontology_probability(x_full, wavelength, slit_distance, slit_width, alpha)
        theory_at_data = np.interp(x_data, x_full, theory_full)
        
        # Calculate weighted residuals
        res = (y_data - theory_at_data) / y_err
        return res
    
    # Perform least-squares fitting
    result = optimize.least_squares(residual, x0=[ALPHA_THEORY], bounds=([0], [1e-14]))
    alpha_fit = result.x[0]
    
    # Estimate error from Jacobian
    cov = np.linalg.inv(result.jac.T @ result.jac)
    alpha_err = np.sqrt(cov[0, 0])
    
    return alpha_fit, alpha_err

def calculate_chi_squared(x_data, y_data, y_err, x_full, theory_full):
    """
    Calculate chi-squared statistic for a theoretical prediction.
    
    Parameters:
    -----------
    x_data, y_data, y_err : arrays
        Experimental data points and errors
    x_full, theory_full : arrays
        Theoretical prediction curve
        
    Returns:
    --------
    chi2 : float
        Chi-squared statistic
    p_value : float
        p-value for the fit
    """
    # Interpolate theory to data points
    theory_at_data = np.interp(x_data, x_full, theory_full)
    
    # Calculate chi-squared
    chi2 = np.sum(((y_data - theory_at_data) / y_err)**2)
    
    # Degrees of freedom
    dof = len(x_data) - 1  # Subtracting 1 parameter for normalization
    
    # p-value (probability of exceeding this chi-squared)
    from scipy.stats import chi2
    p_value = 1 - chi2.cdf(chi2, dof)
    
    return chi2, p_value, dof

def run_simulation(output_dir="./results", save_figures=True):
    """
    Run the full simulation and analysis.
    
    Parameters:
    -----------
    output_dir : str
        Directory for saving results
    save_figures : bool
        Whether to save figures to disk
    """
    # Create output directory if it doesn't exist
    if save_figures and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Simulation parameters
    wavelength = 5e-7  # 500 nm (visible light)
    slit_distance = 1e-5  # 10 micrometers
    slit_width = 1e-6  # 1 micrometer
    screen_width = 1e-3  # 1 millimeter
    
    # Position array
    x = np.linspace(-screen_width/2, screen_width/2, 1000)
    
    # Calculate probability distributions
    prob_std = standard_qm_probability(x, wavelength, slit_distance, slit_width)
    prob_info = info_ontology_probability(x, wavelength, slit_distance, slit_width, ALPHA_THEORY)
    
    # Generate synthetic experimental data (using information ontology as "truth")
    x_data, y_data, y_err = generate_synthetic_data(x, prob_info, num_points=50)
    
    # Fit alpha parameter to the data
    alpha_fit, alpha_err = fit_alpha_parameter(x_data, y_data, y_err, x, wavelength, slit_distance, slit_width)
    prob_info_fit = info_ontology_probability(x, wavelength, slit_distance, slit_width, alpha_fit)
    
    # Calculate chi-squared for both theories
    chi2_std, p_std, dof = calculate_chi_squared(x_data, y_data, y_err, x, prob_std)
    chi2_info, p_info, _ = calculate_chi_squared(x_data, y_data, y_err, x, prob_info_fit)
    
    # Print results
    print(f"Simulation results:")
    print(f"Theoretical alpha: {ALPHA_THEORY:.3e} m²")
    print(f"Best-fit alpha:    {alpha_fit:.3e} ± {alpha_err:.3e} m²")
    print(f"Standard QM:       χ² = {chi2_std:.2f}, p = {p_std:.4f}, dof = {dof}")
    print(f"Information ontology: χ² = {chi2_info:.2f}, p = {p_info:.4f}, dof = {dof}")
    
    # Calculate residuals
    y_std_at_data = np.interp(x_data, x, prob_std)
    y_info_at_data = np.interp(x_data, x, prob_info_fit)
    residuals_std = (y_data - y_std_at_data) / y_err
    residuals_info = (y_data - y_info_at_data) / y_err
    
    # Plot the results
    plt.figure(figsize=(12, 9))
    
    # Panel A: Interference patterns
    plt.subplot(2, 1, 1)
    plt.plot(x * 1e6, prob_std, 'b--', label='Standard QM')
    plt.plot(x * 1e6, prob_info_fit, 'r-', label=f'Information Ontology (α = {alpha_fit:.3e} m²)')
    plt.errorbar(x_data * 1e6, y_data, yerr=y_err, fmt='ko', markersize=4, label='Experimental Data')
    plt.xlabel('Position (μm)')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.title('Double-Slit Interference Pattern')
    
    # Panel B: Residuals
    plt.subplot(2, 1, 2)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.2)
    plt.axhline(y=1, color='k', linestyle=':', alpha=0.2)
    plt.axhline(y=-1, color='k', linestyle=':', alpha=0.2)
    plt.plot(x_data * 1e6, residuals_std, 'bo', label=f'Standard QM (χ² = {chi2_std:.2f})')
    plt.plot(x_data * 1e6, residuals_info, 'ro', label=f'Information Ontology (χ² = {chi2_info:.2f})')
    plt.xlabel('Position (μm)')
    plt.ylabel('Residuals (σ)')
    plt.legend()
    plt.title('Residuals between Theory and Experiment')
    
    plt.tight_layout()
    
    # Save figure
    if save_figures:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(os.path.join(output_dir, f'interference_simulation_{timestamp}.png'), dpi=300)
        
        # Also save the data
        np.savez(os.path.join(output_dir, f'interference_data_{timestamp}.npz'),
                x=x, prob_std=prob_std, prob_info=prob_info, 
                x_data=x_data, y_data=y_data, y_err=y_err,
                alpha_fit=alpha_fit, alpha_err=alpha_err,
                chi2_std=chi2_std, p_std=p_std, 
                chi2_info=chi2_info, p_info=p_info)
    
    plt.show()
    
    # Summary of results
    result_summary = {
        "alpha_theory": ALPHA_THEORY,
        "alpha_fit": alpha_fit,
        "alpha_err": alpha_err,
        "chi2_std": chi2_std,
        "p_std": p_std,
        "chi2_info": chi2_info,
        "p_info": p_info
    }
    
    return result_summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run quantum interference simulation comparing standard QM with information ontology.')
    parser.add_argument('--output', type=str, default='./results', help='Directory for output files')
    parser.add_argument('--no-save', action='store_true', help='Do not save figures and data')
    args = parser.parse_args()
    
    results = run_simulation(output_dir=args.output, save_figures=not args.no_save) 