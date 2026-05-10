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
    print(f"\n[Statistical limit] S = {S_cl_limit:.4f}")

    # experimental protocol simulation
    print(f"\n[Sampling] Running full classical experiment simulation...")
    S_cl_exp = simulate_classical_experiment(1_000_000)
    print(f"\n>> Final S (Classical Experiment): {S_cl_exp:.4f}")

    print(f"\n{'-'*40}")

    # --- QUANTUM MECHANICAL MODEL ---
    print(f"\n{'#'*40}")
    print(f"{' QUANTUM CHSH SIMULATION ':#^40}")
    print(f"{'#'*40}")

    # statistical limit
    S_qu_limit = chsh_quantum()
    print(f"\n[Statistical limit] S = {S_qu_limit:.4f}")

    # experimental protocol simulation
    print(f"\n[Sampling] Running full quantum experiment simulation...")
    S_qu_exp = simulate_quantum_experiment(100_000)
    print(f"\n>> Final S (Quantum Experiment): {S_qu_exp:.4f}")

    # --- SUMMARY ---
    print(f"\n{'#'*40}")
    print(f"{' SUMMARY ':#^40}")
    print(f"{'#'*40}")
    print(f"\n  Classical bound    |S| <= 2.0000")
    print(f"  Tsirelson bound    |S| <= {2*np.sqrt(2):.4f}  (quantum maximum)")
    print(f"\n  Classical S        |S|  = {S_cl_exp:.4f}")
    print(f"  Quantum   S        |S|  = {S_qu_exp:.4f}")
    print(f"\n  Violation of classical bound: {'YES' if S_qu_exp > 2 else 'NO'}")
    print(f"{'#'*40}\n")
    
    return

# ----------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__": 
    main ()
