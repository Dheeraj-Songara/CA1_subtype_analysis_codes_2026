# Intrinsic Electrophysiology Extraction Suite

This repository contains a suite of standalone Python scripts for extracting intrinsic membrane properties and action potential features from whole-cell patch-clamp recordings stored in Axon Binary Format (`.abf`).

This pipeline was used to profile and compare the intrinsic excitability of distinct neuronal subpopulations (e.g., Type A and Type B CA1 pyramidal neurons) as described in the accompanying manuscript.

---

## Overview of Scripts

The suite consists of four modular scripts, each tailored to a specific electrophysiological protocol. All scripts automatically detect the sampling rate from the recording (`abf.dataRate`) and compute timing in milliseconds, ensuring compatibility across datasets without hardcoded assumptions. Stimulus periods are dynamically identified from the command waveform (`sweepC`) wherever applicable.

Recordings were initiated ~5 minutes after achieving whole-cell configuration.

---

## 1. `EPhys_RMP.py` — Resting Membrane Potential

- **Protocol:** Gap-free baseline recordings (no current injection).
- **Mechanism:** Estimates resting membrane potential (RMP) by averaging a baseline segment of the voltage trace (e.g. last 10 seconds of 1 minute trace), avoiding transient artifacts.
- **Output:** `RMP.csv`

---

## 2. `EPhys_IV_features.py` — Input Resistance (IR)

- **Protocol:** Current step recordings with hyperpolarizing and/or depolarizing pulses.
- **Mechanism:**  
  - Detects stimulus onset and offset from non-zero regions of the command waveform (`sweepC`)  
  - Computes baseline voltage (~5 ms before stimulus onset) and steady-state voltage (~5 ms before stimulus end), each averaged over a 1 ms window  
  - Calculates voltage deflection (ΔV) per sweep  
  - Estimates injected current from the command trace  
  - Computes input resistance using linear regression (V = I · R) across valid sweeps  
- **Output:** `IR.csv`

---

## 3. `EPhys_Ih_features.py` — Ih Sag Analysis

- **Protocol:** Hyperpolarizing current step recordings (e.g., ~750 ms duration).
- **Mechanism:**  
  - Detects stimulus onset from the command waveform (`sweepC`)  
  - Defines the stimulus window using a user-specified duration (e.g., 750 ms)  
  - Uses the Blue Brain Project’s Electrophysiology Feature Extraction Library (`efel`)  
  - Extracts:
    - Sag amplitude  
    - Sag ratio (`sag_ratio1`)  
  - Reports mean values across valid sweeps  
- **Output:** `Ih_feature.csv`

---

## 4. `EPhys_FI_features.py` — Action Potential Features & F–I Curve

- **Protocol:** Depolarizing current step recordings with user-defined stimulus duration (e.g., 750 ms).
- **Mechanism:**  
  - Automatically detects stimulus timing from the command waveform (`sweepC`)  
  - Detects action potentials using:
    - dV/dt ≥ 20 mV/ms  
    - 0 mV crossing  
  - Constructs F–I curve (spike count per sweep)  
  - Identifies the rheobase sweep (first sweep with ≥1 spike)  
  - Extracts from rheobase:
    - Spike amplitude  
    - Threshold  
    - First-spike delay (relative to stimulus onset)  
  - Computes adaptation index from inter-spike intervals  
- **Output:** `intrinsic.csv`

---

## Requirements

Ensure you are using Python 3.12 and install the following dependencies:

```bash
pip install pyabf efel scipy numpy pandas
