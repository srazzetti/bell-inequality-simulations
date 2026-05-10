#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script: quantum_model.py
Author: Simone Razzetti
Date: 05/10/2026
Notes: 
"""

# ----------------------------------------------------------------------------------------------------------------------------
# Imports
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from tqdm import tqdm

# ----------------------------------------------------------------------------------------------------------------------------

# --- Quantum Implementation ---
# We simulate the CHSH experiment using a two-qubit quantum circuit.
# The singlet state is prepared and measurements are performed along 
# arbitrary directions via basis rotations before measurement.
# The quantum correlator for the singlet state is E(a,b) = -cos(a-b),
# which violates the classical bound |S| <= 2, reaching S = 2.828
# for the optimal angle settings (CHSH, 1969).

simulator = AerSimulator()

def create_bell_circuit(theta_a : float, theta_b : float):
    """
    Prepares the singlet state and performs projective measurements along 
    directions theta_a (Alice, qubit 0) and theta_b (Bob, qubit 1).

    Measurement along axis theta is implemented by rotating the state
    by -theta (ry(-theta)) before measuring in the computational Z basis.
    This is equivalent to rotating the measurement axis by +theta, since
    only the relative orientation between state and axis matters.
    """
    qc = QuantumCircuit(2, 2)
    # Bell state
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)
    qc.z(1)

    # Measurement directions 
    qc.ry(-theta_a, 0)
    qc.ry(-theta_b, 1)
    qc.measure([0, 1], [0, 1])

    return qc

# Helper functions to calculate the correlation terms for the CHSH inequality
def correlation(counts, shots):
    """
    Computes the correlation E(a,b) from measurement counts.
    Outcomes are encoded as: 0 -> +1, 1 -> -1.

    Note on Qiskit bit ordering: bitstring[0] is qubit 1 (Bob),
    bitstring[1] is qubit 0 (Alice).
    """
    corr = 0
    for bitstring, count in counts.items():
        b = 1 if bitstring[0] == '0' else -1
        a = 1 if bitstring[1] == '0' else -1
        corr += a * b * count / shots
    return corr

def get_E_quantum(theta_a, theta_b, shots=10000):
    """
    Computes the quantum expectation value E(a, b) by running the Bell circuit 
    and averaging over measurement outcomes. 
    For the singlet state, the theoretical value is E(a,b) = -cos(a-b).
    """
    qc = create_bell_circuit(theta_a, theta_b)
    job = simulator.run(qc, shots=shots)
    counts = job.result().get_counts()
    return correlation(counts, shots)


def chsh_quantum(a=0.0, a_p=np.pi/2, b=np.pi/4, b_p=-np.pi/4, shots=10000):
    """
    Calculates the CHSH S value using quantum simulation. 
    Default angles are chosen to maximize quantum violation.
    The CHSH parameter is defined as (see derivation from C = (A+A')B + (A-A')B'):
        S = E(a,b) + E(a',b) + E(a,b') - E(a',b')
    Quantum mechanics predicts |S| = 2.828, violating the classical
    bound |S| <= 2 (Bell, 1964; CHSH, 1969).
    """
    E_ab   = get_E_quantum(a, b, shots)
    E_apb  = get_E_quantum(a_p, b, shots)
    E_abp  = get_E_quantum(a, b_p, shots)
    E_apbp = get_E_quantum(a_p, b_p, shots)

    # Compute the absolute value of the CHSH statistic
    S = abs(E_ab + E_apb + E_abp - E_apbp)
    return S

# -----------------------------------------------------
# The following function simulates the CHSH experiment as it would be performed
# in a real laboratory setting, where Alice and Bob independently and randomly
# choose their measurement directions for each trial.
#
# This is conceptually different from chsh_quantum(), which directly computes 
# each correlator E(a,b) in the statistical limit (infinite trials, fixed angles).
# Here instead, each trial contributes to one of the four correlators depending
# on the random angle choices — reproducing the actual experimental protocol.

def simulate_experiment_quantum(n_trials=100000, shots_per_trial=1):
    """
    Simulates the CHSH experiment as it would be performed in a real lab.
    For each trial, Alice and Bob independently and randomly choose their
    measurement angle. This is statistically equivalent to computing E(a,b) 
    directly, but faithfully reproduces the experimental protocol.
    """
    a, ap = 0, np.pi/2
    b, bp = np.pi/4, -np.pi/4

    sums   = {'a_b': 0, 'a_bp': 0, 'ap_b': 0, 'ap_bp': 0}
    counts = {'a_b': 0, 'a_bp': 0, 'ap_b': 0, 'ap_bp': 0}

    print(f'shots per trial = {shots_per_trial}')
    print(f'Running {n_trials} quantum toy experiments...')
    for _ in tqdm(range(n_trials)):
        # independent random choice for Alice and Bob
        alice_angle = np.random.choice([a, ap])
        bob_angle   = np.random.choice([b, bp])

        # identify which correlator this trial contributes to
        alice_key = 'a'  if alice_angle == a else 'ap'
        bob_key   = 'b'  if bob_angle   == b else 'bp'
        key = f"{alice_key}_{bob_key}"

        # run the quantum circuit for this trial
        qc = create_bell_circuit(alice_angle, bob_angle)
        job = simulator.run(qc, shots=shots_per_trial)
        trial_counts = job.result().get_counts()

        # accumulate
        for bitstring, count in trial_counts.items():
            b_out = 1 if bitstring[0] == '0' else -1
            a_out = 1 if bitstring[1] == '0' else -1
            sums[key]   += a_out * b_out * count
            counts[key] += count

    # compute correlators from accumulated results
    E_ab   = sums['a_b']   / counts['a_b']
    E_abp  = sums['a_bp']  / counts['a_bp']
    E_apb  = sums['ap_b']  / counts['ap_b']
    E_apbp = sums['ap_bp'] / counts['ap_bp']

    print(f"E(a,b)   = {E_ab:.4f}")
    print(f"E(a,b')  = {E_abp:.4f}")
    print(f"E(a',b)  = {E_apb:.4f}")
    print(f"E(a',b') = {E_apbp:.4f}")

    S = abs(E_ab + E_apb + E_abp - E_apbp)
    return S


# ----------------------------------------------------------------------------------------------------------------------------
# MAIN SCRIPT
# ----------------------------------------------------------------------------------------------------------------------------

def main () :
    print("quantum_model.py is a library!")

    # debug
    S = chsh_quantum()
    print(f'S quantum = {S:.4f}')
    S = simulate_experiment_quantum(10000)
    print(f'S by full simulation = {S:.4}')
    return

# ----------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__": 
    main ()