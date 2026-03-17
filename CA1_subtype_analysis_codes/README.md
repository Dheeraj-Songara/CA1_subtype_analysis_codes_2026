# CA1 Neuronal Subtype Mapping to Allen Brain Atlas

This repository contains the computational pipeline used to project *in vivo* transcriptomic signatures of CA1 pyramidal neuron subpopulations (Type A and Type B) onto the Allen Institute Smart-seq reference atlas.

This analysis accompanies the manuscript:
**[Add your paper title here]**

---

## 🔬 Overview

To validate the existence of CA1 neuronal subpopulations across independent datasets, this pipeline maps differentially expressed gene (DEG) signatures onto the Allen Brain Institute Smart-seq dataset.

The workflow includes:
- Reference dataset preprocessing (Smart-seq hippocampus)
- DEG signature extraction from bulk RNA-seq (DESeq2)
- Gene module scoring using Scanpy
- Strict subtype classification using percentile thresholds
- Visualization via publication-ready dot plots

---

## 📂 Repository Structure

.
├── scripts/
│   └── Allen_smartseq_comparision.py
├── data/
│   ├── allen_smartseq_hippocampus.h5ad
│   └── DESeq2_results_Type_A_vs_B.xlsx
├── results/
│   └── single_cell_mapping/
├── README.md
├── requirements.txt

---

## ⚙️ Requirements

Python 3.10+

Install dependencies:

pip install scanpy pandas matplotlib openpyxl

---

## 🚀 Usage

Run the pipeline:

python Allen_smartseq_comparision.py

---

## 🧠 Method Summary

1. Preprocessing
2. Signature Extraction
3. Cell Classification
4. Visualization

---

## 📊 Outputs

results/single_cell_mapping/

---

## 📌 Reproducibility

Key parameters:
- TOP_N_GENES = 100  
- SCORE_PERCENTILE = 0.8  
- TARGET_SUM = 1e6  
- MIN_CELLS_PER_GENE = 10  

---

## 📁 Data Availability

- Allen Brain Smart-seq dataset: [Add link]
- Processed DEG results: Included / [Add link]

---

## 📜 DOI (for publication)

After creating a GitHub release, archive via Zenodo:
https://zenodo.org

---

## 👤 Author

Dheeraj Songara  

---

## 📄 License

[Add license]

---

## 🙏 Acknowledgements

- Allen Institute for Brain Science  
- Scanpy ecosystem  
