# Allen Brain Atlas Reference Mapping Pipeline

This repository contains a computational pipeline for projecting in-house transcriptomic signatures of CA1 pyramidal neuron subpopulations (Type A and Type B) onto the Allen Institute Smart-seq reference atlas.

Allen Brain Atlas dataset:
https://brain-map.org/our-research/cell-types-taxonomies/cell-types-database-rna-seq-data/mouse-whole-cortex-and-hippocampus-smart-seq

---

## Overview

To validate the presence of Type A and Type B CA1 neuronal subpopulations in an independent dataset, this script (`allen_reference_mapping.py`) maps subtype-specific gene signatures onto the Allen Smart-seq hippocampal reference atlas.

The pipeline performs:

- Standard scRNA-seq preprocessing (filtering, normalization, log-transformation)
- Selecting the CA1 pyramidal neuron population (`CA1-ProS`)
- Extraction of top differentially expressed genes (DEGs) from DESeq2 results
- Gene module scoring using `scanpy.tl.score_genes`
- Conservative subtype classification using percentile-based thresholds
- Visualization of subtype-specific signatures via dot plots

---

## Pipeline Details

### 1. Preprocessing
- Filters genes expressed in fewer than 10 cells  
- Normalizes counts to a total of 1e6 (Smart-seq recommendation)  
- Log-transforms expression values  
- Subsets the dataset to CA1 pyramidal neurons (`subclass_label == "CA1-ProS"`)

---

### 2. Signature Extraction
- Reads DESeq2 results from a single Excel file  
- Extracts top N genes (default: 100) from:
  - `Type A` sheet  
  - `Type B` sheet  
- Filters genes to retain only those present in the reference dataset  

---

### 3. Module Scoring
- Computes:
  - `Type_A_score`
  - `Type_B_score`  
using `scanpy.tl.score_genes`

---

### 4. Subtype Classification
- Uses a percentile-based threshold (default: top 20%) for each score  
- Classification strategy:
  - Identify **Type A-like cells** first  
  - Identify **Type B-like cells** from remaining cells (mutually exclusive)  
- Cells not meeting criteria remain **Unassigned**  
- Downstream analysis focuses on classified populations only  

---

### 5. Visualization
- Scales expression values for visualization  
- Generates dot plots of:
  - Type A signature genes  
  - Type B signature genes  


---

## Inputs

- **Reference dataset:**  
  `allen_smartseq_hippocampus.h5ad`

- **DESeq2 results:**  
  `Data 1.xlsx` 
  - Sheet names must match:
    - `Type A`
    - `Type B`

---


## Requirements
The code is written in Python 3.12 Ensure the following dependencies are installed:

```bash
pip install scanpy numpy pandas matplotlib openpyxl
