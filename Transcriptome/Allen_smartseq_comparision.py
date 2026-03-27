#!/usr/bin/env python3
"""
allen_reference_mapping.py

Computational pipeline for projecting in-house CA1 neuronal subtype signatures 
(Type A and Type B) onto the Allen Institute Smart-seq reference atlas.

This script performs standard scRNA-seq preprocessing, calculates subtype-specific 
gene module scores based on DESeq2 contrasts, and classifies reference cells 
using a defined percentile threshold.

"""

import scanpy as sc
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path
from typing import List, Tuple, Dict

# === EXPERIMENTAL PARAMETERS ===
# Centralizing parameters makes the pipeline easily reproducible and modifiable
TOP_N_GENES = 100               # Number of top DEGs to use for module scoring
SCORE_PERCENTILE = 0.8          # Quantile threshold for classifying cells
TARGET_SUM = 1e6                # Normalization target (Smart-seq recommendation)
MIN_CELLS_PER_GENE = 10         # Filter threshold for rare transcripts
SUBCLASS_TARGET = "CA1-ProS"    # Target anatomical region in reference

def preprocess_reference(h5ad_path: str) -> sc.AnnData:
    """Loads and preprocesses the Allen Smart-seq reference dataset."""
    print(f"Loading reference atlas from {h5ad_path}...")
    adata = sc.read_h5ad(h5ad_path, backed=None)
    
    sc.pp.calculate_qc_metrics(adata, percent_top=None, log1p=False, inplace=True)
    sc.pp.filter_genes(adata, min_cells=MIN_CELLS_PER_GENE)
    sc.pp.normalize_total(adata, target_sum=TARGET_SUM)
    sc.pp.log1p(adata)
    
    # Store the normalized/log-transformed data in raw for safe keeping
    adata.raw = adata
    
    # Subset to the region of interest
    ca1_adata = adata[adata.obs["subclass_label"] == SUBCLASS_TARGET].copy()
    return ca1_adata.raw.to_adata()

def extract_signatures(excel_path: str, type_a_sheet: str, type_b_sheet: str, 
                       valid_genes: pd.Index) -> Tuple[List[str], List[str]]:
    """Extracts the top N valid marker genes from different sheets of a single DESeq2 Excel file."""
    
    def get_valid_genes(path: str, sheet: str) -> List[str]:
        df = pd.read_excel(path, sheet_name=sheet)
        genes = df["Gene_symbol"].tolist()
        # Filter against genes actually present in the reference atlas
        valid = [g for g in genes if g in valid_genes]
        return valid[:TOP_N_GENES]

    type_a_genes = get_valid_genes(excel_path, type_a_sheet)
    type_b_genes = get_valid_genes(excel_path, type_b_sheet)
    
    print(f"Retained {len(type_a_genes)} Type A genes and {len(type_b_genes)} Type B genes for scoring.")
    return type_a_genes, type_b_genes


def classify_subtypes(adata: sc.AnnData, type_a_genes: List[str], type_b_genes: List[str]) -> sc.AnnData:
    """Scores cells based on signatures and strictly classifies them into subtypes."""
    
    # Calculate module scores
    sc.tl.score_genes(adata, gene_list=type_a_genes, score_name="Type_A_score")
    sc.tl.score_genes(adata, gene_list=type_b_genes, score_name="Type_B_score")

    # Determine dynamic thresholds
    type_a_thresh = adata.obs["Type_A_score"].quantile(SCORE_PERCENTILE)
    type_b_thresh = adata.obs["Type_B_score"].quantile(SCORE_PERCENTILE)

    # Strict isolation: Find Type A cells first
    type_a_cells = adata.obs_names[adata.obs["Type_A_score"] >= type_a_thresh]
    
    # Identify Type B cells strictly from the remaining pool (preventing double assignment)
    remaining_cells = adata.obs_names.difference(type_a_cells)
    remaining_adata = adata[remaining_cells]
    type_b_cells = remaining_adata.obs_names[remaining_adata.obs["Type_B_score"] >= type_b_thresh]

    print(f"Identified {len(type_a_cells)} Type A-like cells and {len(type_b_cells)} Type B-like cells.")

    # Annotate the object
    adata.obs["Subtype_Classification"] = "Unassigned"
    adata.obs.loc[type_a_cells, "Subtype_Classification"] = "Type A-like"
    adata.obs.loc[type_b_cells, "Subtype_Classification"] = "Type B-like"
    adata.obs["Subtype_Classification"] = adata.obs["Subtype_Classification"].astype("category")

    # Subset the object to only include our classified populations for downstream plotting
    classified_adata = adata[adata.obs["Subtype_Classification"].isin(["Type A-like", "Type B-like"])].copy()
    
    # Scale data for visualization
    sc.pp.scale(classified_adata, max_value=10)
    classified_adata.layers["scaled"] = classified_adata.X.copy()
    
    return classified_adata

def plot_signatures(adata: sc.AnnData, type_a_genes: List[str], type_b_genes: List[str], output_dir: Path):
    """Generates and saves publication-ready dotplots for the identified subtypes."""
    
    # Define custom colormaps
    blue_green_cmap = LinearSegmentedColormap.from_list("blue_green", ["#0566c6", "#e4e9ec", "#059141"])
    green_blue_cmap = LinearSegmentedColormap.from_list("green_white_blue", ["#1a9850", "#ffffff", "#2166ac"])

    # Plot Type A Signature
    sc.pl.dotplot(
        adata,
        var_names=type_a_genes,  
        groupby="Subtype_Classification",
        layer="scaled",
        cmap=blue_green_cmap,
        show=False
    )
    plt.savefig(output_dir / "Type_A_Signature_Dotplot.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Plot Type B Signature
    sc.pl.dotplot(
        adata,
        var_names=type_b_genes,  
        groupby="Subtype_Classification",
        layer="scaled",
        cmap=green_blue_cmap,
        show=False
    )
    plt.savefig(output_dir / "Type_B_Signature_Dotplot.png", dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Setup directories
    output_dir = Path("results/single_cell_mapping")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Define file paths (Now just one Excel file)
    REFERENCE_H5AD = "allen_smartseq_hippocampus.h5ad"
    DESEQ_EXCEL = "Data 1.xlsx"

    # Execute pipeline
    print("Starting Reference Mapping Pipeline...\n" + "-"*40)
    
    ca1_full = preprocess_reference(REFERENCE_H5AD)
    
    # Note: Ensure "Type A" and "Type B" exactly match your Excel sheet names. 
    # If they are still named "gfp" and "ngfp", change them here.
    type_a_genes, type_b_genes = extract_signatures(
        DESEQ_EXCEL, 
        "Type A",   # Sheet name for Type A
        "Type B",   # Sheet name for Type B
        ca1_full.var_names
    )
    
    ca1_classified = classify_subtypes(ca1_full, type_a_genes, type_b_genes)
    
    print("Generating visualizations...")
    plot_signatures(ca1_classified, type_a_genes, type_b_genes, output_dir)
    
    print(f"Pipeline complete. Outputs saved to: ./{output_dir}/")

if __name__ == "__main__":
    main()