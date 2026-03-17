# CA1 Subtype Analysis Code Repository

This repository contains analysis pipelines for studying CA1 neuronal subtypes across multiple experimental modalities, including electrophysiology, transcriptomics, and behaviour.

---

## Repository Structure

### 1. Electrophysiology/

This folder contains scripts for extracting and analyzing intrinsic electrophysiological properties of neurons.

**Files:**
- `EPhys_IV_features.py` → Computes current–voltage (I–V) relationships
- `EPhys_FI_features.py` → Calculates firing rate vs current (F–I curves)
- `EPhys_Ih_features.py` → Extracts Ih-related properties (sag, rebound)
- `EPhys_RMP.py` → Computes resting membrane potential (RMP)

**Purpose:**
To characterize intrinsic excitability and membrane properties of neuronal subtypes.

---

### 2. Transcriptome/

This folder contains scripts for transcriptomic analysis file, including integration with external datasets.

**Files:**
- `Allen_smartseq_comparision.py` → Maps subtype-specific gene signatures onto the Allen Brain Smart-seq reference dataset
- Associated README files explaining specific pipelines

**Purpose:**
To validate subtype identity using gene expression profiles and external single-cell datasets.

---

### 3. Behaviour/

This folder contains analysis scripts related to behavioural experiments.

**Files:**
- `freezing_analysis.py` → Quantifies freezing behavior (e.g., fear conditioning)
- `README.md` → Description of behavioral analysis pipeline

**Purpose:**
To link neuronal subtype differences with behavioral outcomes.

---

## Requirements

- Python 3.10+
- scanpy
- pandas
- matplotlib
- openpyxl
- efel

Install using:
```
pip install scanpy pandas matplotlib openpyxl
```

## Notes

- Ensure input data paths are correctly set inside each script
- Large datasets (e.g., `.h5ad`) may not be included in the repository
- Modify parameters within scripts as needed for reproducibility

---

## Authors

Dheeraj Songara, Hiyaa Ghosh

---

