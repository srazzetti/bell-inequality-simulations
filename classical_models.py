#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script: classical_models.py
Author: Simone Razzetti
Date: 05/07/2026
Notes: look for the standard def of correlator
"""

# ----------------------------------------------------------------------------------------------------------------------------
# Imports
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------------------------------------------------------

# --- Local Hidden Variable (LHV) Model Implementation ---
# We define Alice and Bob's measurement outcomes as deterministic functions f(angle, lam) -> {+-1}.
# While any function mapping the hidden variable 'lam' to a binary outcome is theoretically valid,
# we adopt the "hidden direction" model for its physical intuition, rotational symmetry, 
# and historical relevance in Bell's original proof (Bell, 1964).

def A(angle: float, lam: float):
    """
    Simulates Alice's measurement: the outcome is determined by the 
    projection of the hidden variable 'lam' onto the measurement axis 'angle'
    """
    return np.sign(np.cos(lam - angle))

def B(angle: float, lam: float):
    """
    Simulates Bob's measurement: the outcome is determined by the 
    negative projection of the hidden variable 'lam' onto the measurement axis 'angle'
    """
    return np.sign(np.cos(lam - angle))


# Helper function to calculate the correlation terms for the CHSH inequality
def get_E_classical(a, b, n_samples=100000):
    """
    Computes the expectation value E(a, b) by averaging the product 
    of local outcomes over the hidden variable distribution.
    """
    # Suppose lambda is uniformly distributed in [0, 2pi]
    lam = np.random.uniform(0, 2*np.pi, n_samples)
    return np.mean(A(a, lam) * B(b, lam))

def chsh_classical(a=0.0, a_p=np.pi/2, b=np.pi/4, b_p=-np.pi/4, n_samples=100000):
    """
    Calculates the CHSH 'S' value. By default, it uses the standard settings for Alice (a, a') and Bob (b, b')
    that maximize quantum violation. 
    Bell's theorem states that for any Local Hidden Variable (LHV) model: |S| <= 2.
    """
    # The CHSH parameter S is a linear combination of four correlation terms:
    # S = E(a, b) + E(a', b) + E(a, b') - E(a', b') 
    # or C = (a+a')b + (a-a')b' measure outcome
    E_ab   = get_E_classical(a, b, n_samples)
    E_apb  = get_E_classical(a_p, b, n_samples)
    E_abp  = get_E_classical(a, b_p, n_samples)
    E_apbp = get_E_classical(a_p, b_p, n_samples)

    # Compute the absolute value of the CHSH statistic
    S = abs(E_ab + E_apb + E_abp - E_apbp)
    return S

# ----------------------------------------------------------------------------------------------------------------------------
# MAIN SCRIPT
# ----------------------------------------------------------------------------------------------------------------------------

def main () :
    print("Classical_models.py is a library!")

    # debug
    S = chsh_classical()
    print(f'S classic = {S:.4f}')
    return

# ----------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__": 
    main ()