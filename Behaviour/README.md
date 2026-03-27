# Automated Freezing Detection Pipeline

This repository contains the custom Python pipeline used for quantifying freezing behavior in rodent contextual fear memory assays, as described in the manuscript.

## Overview
This script (`freezing_analysis.py`) automates the detection of freezing bouts by calculating absolute pixel-intensity differences across consecutive video frames. 

Freezing is defined strictly as an absence of movement (excluding respiration/ threshold), quantified here as a frame-by-frame motion score dropping below a manually validated threshold (e.g. 200000) for a sustained minimum duration (default: 0.5 seconds).

## Requirements
The code was written and tested using Python 3.12. Ensure you have the required dependencies installed:

```bash
pip install opencv-python numpy pandas matplotlib
