# CA1 Subtype Analysis Code Repository

This repository contains analysis pipelines for studying CA1 neuronal subtypes across multiple experimental modalities, including electrophysiology, transcriptomics, and behavior.

---

## Repository Structure

### 1. Electrophysiology/

This folder contains scripts for extracting and analyzing intrinsic electrophysiological properties of neurons.

**Files:**
- `EPhys_IV_features.py` → Computes current–voltage (I–V) relationships for input resistance calculations
- `EPhys_FI_features.py` → Calculates firing rate vs current (F–I curves)
- `EPhys_Ih_features.py` → Extracts Ih-sag amplitude and ratio
- `EPhys_RMP.py` → Computes resting membrane potential (RMP)

**Purpose:**
To characterize intrinsic excitability and membrane properties of neuronal subtypes.

---

### 2. Transcriptome

This folder contains scripts for Allen's SMART-seq analysis to identify A-like and B-like cells and generate dot plots.

**Files:**
- `Allen_smartseq_comparision.py` → Maps subtype-specific gene signatures onto the Allen Brain Smart-seq reference dataset
- Associated README files explaining specific pipelines

**Purpose:**
To establish subtype identity by comparing gene expression profiles with an external single-cell datasets.

---

### 3. Behavior/

This folder contains analysis scripts related to behavioral experiments.

**Files:**
- `freezing_analysis.py` → Quantifies freezing behavior (e.g., fear conditioning)
- `README.md` → Description of behavioral analysis pipeline

**Purpose:**
To link function of neuronal subtypes to behavioral outcomes.

---

## Requirements

- Python 3.10+
- scanpy
- pandas
- matplotlib
- openpyxl
- efel
- opencv

Install using:
```
pip install scanpy pandas matplotlib openpyxl opencv-python
```

## Notes

- Ensure input data paths are correctly set inside each script
- Large datasets (e.g., `.h5ad`) may not be included in the repository
- Modify parameters within scripts as needed for reproducibility

---

## Authors

Dheeraj Songara, Hiyaa Ghosh
