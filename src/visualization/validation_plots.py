"""
Validation Plots Module
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as plt_sns
from typing import List, Dict, Any

class ValidationVisualizer:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        try:
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            pass

    def plot_extraction_summary(self, logs: List[Dict[str, Any]]):
        if not logs: return
        df = pd.DataFrame(logs)
        plt.figure(figsize=(6, 4))
        plt_sns.countplot(data=df, x='status', palette='pastel')
        plt.title('ZIP Extraction Summary')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'extraction_summary.png'), dpi=300)
        plt.close()

    def plot_validation_status(self, registry: List[Dict[str, Any]]):
        if not registry: return
        df = pd.DataFrame(registry)
        plt.figure(figsize=(6, 4))
        plt_sns.countplot(data=df, x='is_valid', palette='pastel')
        plt.title('Dataset Validation Status')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'validation_status.png'), dpi=300)
        plt.close()
        
    def plot_identifier_coverage(self, registry: List[Dict[str, Any]]):
        if not registry: return
        # Count datasets with PATNO
        patno_counts = sum(1 for r in registry if "PATNO" in [i.upper() for i in r.get("found_identifiers", [])])
        total = len(registry)
        
        plt.figure(figsize=(6, 4))
        plt.bar(['Contains PATNO', 'Missing PATNO'], [patno_counts, total - patno_counts], color=['#4C72B0', '#C44E52'])
        plt.title('PATNO Identifier Coverage')
        plt.ylabel('Number of Datasets')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'identifier_coverage.png'), dpi=300)
        plt.close()

    def generate_all(self, logs: List[Dict[str, Any]], registry: List[Dict[str, Any]]):
        self.plot_extraction_summary(logs)
        self.plot_validation_status(registry)
        self.plot_identifier_coverage(registry)
