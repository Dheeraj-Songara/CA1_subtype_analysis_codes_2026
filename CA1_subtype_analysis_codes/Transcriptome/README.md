# Allen Brain Atlas Reference Mapping Pipeline

This repository contains the computational pipeline used to project *in vivo* transcriptomic signatures of CA1 pyramidal neuron subpopulations (Type A and Type B) onto the independent Allen Brain Institute Smart-seq reference atlas. 

https://brain-map.org/our-research/cell-types-taxonomies/cell-types-database-rna-seq-data/mouse-whole-cortex-and-hippocampus-smart-seq

This analysis accompanies the manuscript

## Overview
To validate the existence of our identified Type A and Type B CA1 subpopulations across independent datasets, this script (`allen_smartseq_comparision.py`) maps our top differentially expressed gene (DEG) signatures onto the Allen Institute's hippocampal scRNA-seq atlas. 

The pipeline performs standard preprocessing, calculates subtype-specific gene module scores controlling for technical noise, and conservatively classifies cells using a strict, mutually exclusive thresholding strategy.

## Requirements
The code is written in Python 3.12 Ensure the following dependencies are installed:

```bash
pip install scanpy pandas matplotlib openpyxl
