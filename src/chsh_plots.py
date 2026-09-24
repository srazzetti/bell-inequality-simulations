#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script: chsh_plots.py
Author: Simone Razzetti
Date: 09/24/2026
Description: 
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qiskit_aer import AerSimulator

# Import local modules
from classical_models import chsh_classical
from quantum_model import chsh_quantum, create_bell_circuit, correlation

# Initialize Aer Simulator
simulator = AerSimulator()

# Path to src/ directory
SRC_DIR = Path(__file__).resolve().parent
# Path to project root (proj/)
PROJECT_ROOT = SRC_DIR.parent
# Path to proj/results/
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------------------------------------------------------------
# 1D PLOTS (S vs Bob's Angle)

def chsh_1d_comparison_plot(n_angles=100, n_samples=1000):
    """
    Plots CHSH S-value as a function of Bob's angle theta for both Classical and Quantum models.
    Returns the Matplotlib Figure object alongside simulation data.
    """
    thetas = np.linspace(0, 2 * np.pi, n_angles)
    S_classical_values = []
    S_quantum_values = []

    a, ap = 0.0, np.pi / 2

    for theta in thetas:
        b = theta
        bp = b - np.pi / 2
        
        S_classical_values.append(chsh_classical(a, ap, b, bp, n_samples))
        S_quantum_values.append(chsh_quantum(a, ap, b, bp, n_samples))

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(thetas, S_classical_values, label='Classical LHV', color='blue', linewidth=2)
    ax.plot(thetas, S_quantum_values, label='Quantum Mechanics', color='orange', linewidth=2)
    
    # Bell Bound lines
    ax.axhline(2, color='red', linestyle='--', label='Classical Bound (|S| = 2)')
    ax.axhline(-2, color='red', linestyle='--')
    
    # Highlight Violation Regions
    S_q_arr = np.array(S_quantum_values)
    ax.fill_between(thetas, S_q_arr, 2, where=(S_q_arr > 2), color='green', alpha=0.25, label='Quantum Violation')
    ax.fill_between(thetas, S_q_arr, -2, where=(S_q_arr < -2), color='green', alpha=0.25)

    ax.set_xlabel("Bob's angle θ (rad)")
    ax.set_ylabel("CHSH S parameter")
    ax.set_title("CHSH Inequality: Classical vs Quantum Mechanics")
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    return fig, thetas, S_classical_values, S_quantum_values


# ----------------------------------------------------------------------------------------------------------------------------
# 2D HEATMAPS

def get_S_matrix_classical(grid_resolution=60, n_samples=10000):
    """
    Computation of Classical CHSH S(a, b) matrix over Alice and Bob angle grids.
    """
    a_range = np.linspace(0, 2 * np.pi, grid_resolution)
    b_range = np.linspace(0, 2 * np.pi, grid_resolution)
    A_grid, B_grid = np.meshgrid(a_range, b_range)

    lam = np.random.uniform(0, 2 * np.pi, size=(n_samples, 1, 1))

    def get_E_grid(a_g, b_g):
        A_out = np.sign(np.cos(a_g[None, :, :] - lam))
        B_out = -np.sign(np.cos(b_g[None, :, :] - lam))
        return np.mean(A_out * B_out, axis=0)

    Ap_grid = A_grid + np.pi / 2
    Bp_grid = B_grid + np.pi / 2

    E_ab   = get_E_grid(A_grid, B_grid)
    E_abp  = get_E_grid(A_grid, Bp_grid)
    E_apb  = get_E_grid(Ap_grid, B_grid)
    E_apbp = get_E_grid(Ap_grid, Bp_grid)

    S_matrix = E_ab - E_abp + E_apb + E_apbp
    return A_grid, B_grid, S_matrix


def get_S_matrix_quantum(grid_resolution=40, shots=512):
    """
    Qiskit simulation for Quantum CHSH S(a, b) heatmap.
    """
    a_range = np.linspace(0, 2 * np.pi, grid_resolution)
    b_range = np.linspace(0, 2 * np.pi, grid_resolution)
    A_grid, B_grid = np.meshgrid(a_range, b_range)

    circuits = []
    for a, b in zip(A_grid.ravel(), B_grid.ravel()):
        ap, bp = a + np.pi / 2, b + np.pi / 2
        circuits.append(create_bell_circuit(a, b))
        circuits.append(create_bell_circuit(a, bp))
        circuits.append(create_bell_circuit(ap, b))
        circuits.append(create_bell_circuit(ap, bp))

    job = simulator.run(circuits, shots=shots)
    results = job.result()

    S_matrix = np.zeros(A_grid.shape)
    idx = 0
    for i in range(grid_resolution):
        for j in range(grid_resolution):
            E_ab   = correlation(results.get_counts(idx), shots)
            E_abp  = correlation(results.get_counts(idx + 1), shots)
            E_apb  = correlation(results.get_counts(idx + 2), shots)
            E_apbp = correlation(results.get_counts(idx + 3), shots)
            
            S_matrix[i, j] = E_ab - E_abp + E_apb + E_apbp
            idx += 4

    return A_grid, B_grid, S_matrix


def plot_chsh_heatmaps_comparison(grid_resolution=50, n_samples=10000, shots=512):
    """
    Generates side-by-side heatmaps comparing Classical LHV and Quantum CHSH landscapes.
    Returns the Matplotlib Figure object.
    """
    print("Calculating Classical Heatmap...")
    A_g, B_g, S_class = get_S_matrix_classical(grid_resolution=grid_resolution, n_samples=n_samples)
    
    print("Calculating Quantum Heatmap (Qiskit Batch)...")
    _, _, S_quant = get_S_matrix_quantum(grid_resolution=grid_resolution, shots=shots)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # --- Classical Plot ---
    im1 = axes[0].pcolormesh(A_g, B_g, S_class, cmap='RdBu_r', vmin=-2.82, vmax=2.82, shading='auto')
    axes[0].contour(A_g, B_g, S_class, levels=[-1.9, 1.9], colors='black', linestyles='--', linewidths=1.5)
    axes[0].set_title(r'Classical LHV Model ($|S| \leq 2$ Bound)')
    axes[0].set_xlabel('Alice Angle $a$ (rad)')
    axes[0].set_ylabel('Bob Angle $b$ (rad)')
    fig.colorbar(im1, ax=axes[0], label='CHSH S Value')

    # --- Quantum Plot ---
    im2 = axes[1].pcolormesh(A_g, B_g, S_quant, cmap='RdBu_r', vmin=-2.82, vmax=2.82, shading='auto')
    axes[1].contour(A_g, B_g, S_quant, levels=[-1.9, 1.9], colors='black', linestyles='--', linewidths=1.5)
    axes[1].set_title(r'Quantum Mechanics (Tsirelson Bound $|S| \leq 2\sqrt{2}$)')
    axes[1].set_xlabel('Alice Angle $a$ (rad)')
    axes[1].set_ylabel('Bob Angle $b$ (rad)')
    fig.colorbar(im2, ax=axes[1], label='CHSH S Value')

    fig.tight_layout()
    return fig


# ----------------------------------------------------------------------------------------------------------------------------
# MAIN SCRIPT
# ----------------------------------------------------------------------------------------------------------------------------

def main():

    print("--- Running 1D Comparison Plot ---")
    fig_1d, _, _, _ = chsh_1d_comparison_plot(n_angles=100, n_samples=10000)
    # save the figure
    output_1d_path = RESULTS_DIR / "chsh_1d_comparison.png"
    fig_1d.savefig(output_1d_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_1d_path}")
    # show the figure
    plt.show()
    plt.close(fig_1d)

    print("\n--- Running 2D Heatmap Comparison ---")
    # save the figure
    fig_2d = plot_chsh_heatmaps_comparison(grid_resolution=50, n_samples=10000, shots=1024)
    output_2d_path = RESULTS_DIR / "chsh_2d_heatmaps.png"
    fig_2d.savefig(output_2d_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_2d_path}")
    # show the figure
    plt.show()
    plt.close(fig_2d)

if __name__ == "__main__":
    main()