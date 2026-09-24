#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script: classical_models.py
Author: Simone Razzetti
Date: 05/07/2026
Notes: 
"""

# ----------------------------------------------------------------------------------------------------------------------------
# Imports
import numpy as np
from tqdm import tqdm

# ----------------------------------------------------------------------------------------------------------------------------

# --- Local Hidden Variable (LHV) Model Implementation ---
# We define Alice and Bob's measurement outcomes as deterministic functions f(angle, lam) -> {+1, -1}.
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
    return -np.sign(np.cos(lam - angle))


# Helper function to calculate the correlation terms for the CHSH inequality
def get_E_classical(a, b, n_samples=100000):
    """
    Computes the expectation value E(a, b) by averaging the product 
    of local outcomes over the hidden variable distribution, assuming a uniform distribution.
    """
    # Suppose lambda is uniformly distributed in [0, 2pi]
    lam = np.random.uniform(0, 2*np.pi, n_samples)
    return np.mean(A(a, lam) * B(b, lam))


def chsh_classical(a=0.0, ap=np.pi/2, b=np.pi/4, bp=-np.pi/4, n_samples=100000):
    """
    Calculates the CHSH 'S' value. By default, it uses the standard settings for Alice (a, a') 
    and Bob (b, b') that maximize quantum violation. 
    The CHSH parameter is defined as (see derivation from C = (A+A')B + (A-A')B'):
        S = |E(a,b) + E(a',b) + E(a,b') - E(a',b')|
    Bell's theorem states that for any Local Hidden Variable (LHV) model: |S| <= 2.
    """
    E_ab   = get_E_classical(a, b, n_samples)
    E_apb  = get_E_classical(ap, b, n_samples)
    E_abp  = get_E_classical(a, bp, n_samples)
    E_apbp = get_E_classical(ap, bp, n_samples)

    # Compute the absolute value of the CHSH statistic
    S = E_ab + E_apb + E_abp - E_apbp
    return S

# -----------------------------------------------------
# The following function simulates the CHSH experiment as it would be performed
# in a real laboratory setting, where Alice and Bob independently and randomly
# choose their measurement directions for each trial.
# This is conceptually different from chsh_classical(), which directly computes 
# each correlator E(a,b) in the statistical limit (infinite trials, fixed angles).
# Here instead, each trial contributes to one of the four correlators depending
# on the random angle choices - reproducing the actual experimental protocol.

def simulate_classical_experiment(n_trials=1000000, a=0.0, ap=np.pi/2, b=np.pi/4, bp=-np.pi/4, print_corr=True):
    """
    Simulates the CHSH experiment as it would be performed in a real lab.
    For each trial, Alice and Bob independently and randomly choose their measurement angle. 
    This is statistically equivalent to computing E(a,b) directly, but faithfully 
    reproduces the experimental protocol.
    """        
    # counter
    sums   = {'a_b': 0, 'a_bp': 0, 'ap_b': 0, 'ap_bp': 0}
    counts = {'a_b': 0, 'a_bp': 0, 'ap_b': 0, 'ap_bp': 0}

    print(f'Running {n_trials} classical toy experiments...')
    for _ in tqdm(range(n_trials)):
        # independent random choice for Alice and Bob
        alice_angle = np.random.choice([a, ap])
        bob_angle   = np.random.choice([b, bp])

        # identify which correlator this trial contributes to
        alice_key = 'a'  if alice_angle == a else 'ap'
        bob_key   = 'b'  if bob_angle   == b else 'bp'
        key = f"{alice_key}_{bob_key}"
        
        # hidden var: suppose lambda is uniformly distributed in [0, 2pi]
        lam = np.random.uniform(0, 2*np.pi)
        
        # measurement
        outcome = A(alice_angle, lam) * B(bob_angle, lam)
        
        # update the counters
        sums[key]   += outcome
        counts[key] += 1

    # computes empirical correlators
    E_ab   = sums['a_b']   / counts['a_b']
    E_abp  = sums['a_bp']  / counts['a_bp']
    E_apb  = sums['ap_b']  / counts['ap_b']
    E_apbp = sums['ap_bp'] / counts['ap_bp']

    if print_corr:
        print(f"E(a,b)   = {E_ab:.4f}")
        print(f"E(a,b')  = {E_abp:.4f}")
        print(f"E(a',b)  = {E_apb:.4f}")
        print(f"E(a',b') = {E_apbp:.4f}")

    S = E_ab + E_apb + E_abp - E_apbp
    return S

# ----------------------------------------------------------------------------------------------------------------------------
# MAIN SCRIPT
# ----------------------------------------------------------------------------------------------------------------------------

def main () :
    print("classical_models.py is a library!")

    # only for debugging
    S = chsh_classical()
    print(f'|S| classic = {abs(S):.4f}')
    S = simulate_classical_experiment(n_trials=10000, print_corr=False)
    print(f'|S| by full simulation = {abs(S):.4}')
    return

# ----------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__": 
    main ()