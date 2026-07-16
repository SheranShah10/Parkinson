"""
Inventory Plots Module

Responsibility: Generate visualizations for the dataset inventory.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as plt_sns
from typing import List, Dict, Any

class InventoryVisualizer:
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        # Use a style available without internet if possible
        try:
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            pass

    def plot_dataset_sizes(self, df_inventory: pd.DataFrame):
        if df_inventory.empty or "file_size_bytes" not in df_inventory.columns:
            return
            
        plt.figure(figsize=(10, 6))
        # Convert to MB
        df_inventory['size_mb'] = df_inventory['file_size_bytes'] / (1024 * 1024)
        
        # Top 15 largest datasets
        top_n = df_inventory.nlargest(15, 'size_mb')
        plt_sns.barplot(data=top_n, y='file_name', x='size_mb', palette='viridis')
        
        plt.title('Top 15 Datasets by Size (MB)')
        plt.xlabel('Size in MB')
        plt.ylabel('Dataset')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'dataset_size_comparison.png'), dpi=300)
        plt.close()

    def plot_missing_values(self, df_inventory: pd.DataFrame):
        if df_inventory.empty or "missing_percentage" not in df_inventory.columns:
            return
            
        tabular = df_inventory[df_inventory['dataset_type'] == 'tabular'].copy()
        if tabular.empty: return
        
        plt.figure(figsize=(10, 6))
        top_n = tabular.nlargest(15, 'missing_percentage')
        plt_sns.barplot(data=top_n, y='file_name', x='missing_percentage', palette='magma')
        
        plt.title('Top 15 Datasets by Missing Values (%)')
        plt.xlabel('Missing Percentage (%)')
        plt.ylabel('Dataset')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'missing_value_comparison.png'), dpi=300)
        plt.close()

    def plot_patient_coverage(self, df_inventory: pd.DataFrame):
        if df_inventory.empty or "unique_patno_count" not in df_inventory.columns:
            return
            
        has_patno = df_inventory[df_inventory['unique_patno_count'] > 0].copy()
        if has_patno.empty: return
        
        plt.figure(figsize=(10, 6))
        top_n = has_patno.nlargest(15, 'unique_patno_count')
        plt_sns.barplot(data=top_n, y='file_name', x='unique_patno_count', palette='crest')
        
        plt.title('Top 15 Datasets by Patient Coverage (Unique PATNO)')
        plt.xlabel('Unique Patients')
        plt.ylabel('Dataset')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'patient_coverage.png'), dpi=300)
        plt.close()

    def generate_all(self, inventory: List[Dict[str, Any]]):
        if not inventory: return
        df = pd.DataFrame(inventory)
        self.plot_dataset_sizes(df)
        self.plot_missing_values(df)
        self.plot_patient_coverage(df)
