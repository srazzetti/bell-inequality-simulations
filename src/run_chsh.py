#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script: run_chsh.py
Author: Simone Razzetti
Date: 05/10/2026
Description: 
"""

# ----------------------------------------------------------------------------------------------------------------------------
# Imports
import numpy as np
import matplotlib.pyplot as plt
from classical_models import *
from quantum_model import *

# ----------------------------------------------------------------------------------------------------------------------------
# Functions and classes


# ----------------------------------------------------------------------------------------------------------------------------
# MAIN SCRIPT
# ----------------------------------------------------------------------------------------------------------------------------

def main () :
    # --- CLASSICAL LHV MODEL ---
    print(f"\n{'#'*40}")
    print(f"{' CLASSICAL LHV SIMULATION ':#^40}")
    print(f"{'#'*40}")

    # statistical limit
    S_cl_limit = chsh_classical()
    print(f"\n[Statistical limit] |S| = {abs(S_cl_limit):.4f}")

    # experimental protocol simulation --> random choices for a/a' and b/b' for each trial
    print(f"\n[Sampling] Running full classical experiment simulation...")
    S_cl_exp = simulate_classical_experiment(1_000_000)
    print(f"\n>> Final |S| (Classical Experiment): {abs(S_cl_exp):.4f}")

    print(f"\n{'-'*40}")

    # --- QUANTUM MECHANICAL MODEL ---
    print(f"\n{'#'*40}")
    print(f"{' QUANTUM CHSH SIMULATION ':#^40}")
    print(f"{'#'*40}")

    # statistical limit
    S_qu_limit = chsh_quantum()
    print(f"\n[Statistical limit] |S| = {abs(S_qu_limit):.4f}")

    # experimental protocol simulation --> random choices for a/a' and b/b' for each trial
    print(f"\n[Sampling] Running full quantum experiment simulation...")
    S_qu_exp = simulate_quantum_experiment(100_000)
    print(f"\n>> Final |S| (Quantum Experiment): {abs(S_qu_exp):.4f}")

    # --- SUMMARY ---
    print(f"\n{'#'*40}")
    print(f"{' SUMMARY ':#^40}")
    print(f"{'#'*40}")
    print(f"\n  Classical bound    |S| <= 2.0000")
    print(f"  Quantum bound    |S| <= {2*np.sqrt(2):.4f}  (quantum maximum)")
    print(f"\n  --- Statistical limit ---")
    print(f"  Classical S        |S|  = {abs(S_cl_limit):.4f}")
    print(f"  Quantum   S        |S|  = {abs(S_qu_limit):.4f}")
    print(f"\n  --- Experimental simulation ---")
    print(f"  Classical S        |S|  = {abs(S_cl_exp):.4f}")
    print(f"  Quantum   S        |S|  = {abs(S_qu_exp):.4f}")
    print(f"\n  Violation of classical bound: {'YES !' if abs(S_qu_exp) > 2 else 'NO !'}")
    print(f"{'#'*40}\n")    
    return

# ----------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__": 
    main ()
