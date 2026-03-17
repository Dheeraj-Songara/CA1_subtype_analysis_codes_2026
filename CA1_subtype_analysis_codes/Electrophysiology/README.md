# Intrinsic Electrophysiology Extraction Suite

This repository contains a suite of standalone Python scripts designed to extract intrinsic membrane properties and action potential kinetics from whole-cell patch-clamp recordings stored in Axon Binary Format (`.abf`). 

This automated pipeline was utilized to rigorously profile and compare the intrinsic excitability of distinct neuronal subpopulations (Type A and Type B CA1 pyramidal neurons) as described in the accompanying manuscript.

## Overview of Scripts
The suite is divided into four modular scripts, each tailored to a specific step-protocol. All scripts are explicitly hardcoded for data acquired at a 20 kHz sampling rate, ensuring that time-windows are calculated accurately across all files regardless of minor variations in sweep length.

### 1. `EPhys_RMP.py` (Resting Membrane Potential)
* Protocol: Designed for 1-minute, gap-free baseline recordings (I=0).
* Mechanism: Averages the final 10 seconds (seconds 50 to 60) of the trace to determine the steady-state resting membrane potential, avoiding any initial seal-settling artifacts.
* Output: `RMP.csv`

### 2. `EPhys_IV_features.py` (Input Resistance)
* Protocol: Designed for 2-second subthreshold current step recordings.
* Mechanism: Dynamically detects the exact start of the current injection by finding the minimum of the command waveform (`sweepC`) in the most hyperpolarized sweep. It averages the steady-state voltage response over the final 250 ms of the 1000 ms step. Resistance is calculated via linear regression (V = I \ R) across hyperpolarizing and non-spiking depolarizing sweeps.
* **Output: `IR.csv`

### 3. `EPhys_Ih_features.py` (Ih Sag Analysis)
* Protocol: Designed for 2-second recordings featuring a 750 ms hyperpolarizing current step.
* Mechanism: Utilizes the Blue Brain Project's Electrophysiology Feature Extraction Library (`efel`) to accurately detect and quantify the hyperpolarization-activated sag amplitude and sag ratio.
* Output: `Ih_feature.csv`

### 4. `EPhys_FI_features.py` (Action Potential Features & F-I Curve)
* Protocol: Designed for 2-second depolarizing step protocols.
* Mechanism: Identifies action potentials using a rigorous derivative threshold (dV/dt >= 20 mV/ms) combined with a 0 mV crossing requirement to build an F-I curve. It automatically isolates the rheobase sweep to extract the precise threshold, amplitude, adaptation index, and delay of the first elicited spike.
* Output: `intrinsic.csv`

## Requirements
Ensure you are using Python 3.12 and have the following dependencies installed:

```bash
pip install pyabf efel scipy numpy pandas
