"""
Cohort Plots Module
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as plt_sns
import numpy as np

class CohortVisualizer:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        try:
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            pass

    def plot_flow(self, flow: dict):
        if not flow: return
        labels = list(flow.keys())
        counts = list(flow.values())
        
        plt.figure(figsize=(8, 5))
        plt.plot(labels, counts, marker='o', linestyle='-', linewidth=2, markersize=8)
        plt.title('Cohort Flow Diagram')
        plt.ylabel('Number of Participants')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'cohort_flow_diagram.png'), dpi=300)
        plt.close()

    def plot_visit_distribution(self, df: pd.DataFrame):
        if 'EVENT_ID' not in df.columns: return
        plt.figure(figsize=(10, 6))
        plt_sns.countplot(data=df, x='EVENT_ID', palette='viridis', order=df['EVENT_ID'].value_counts().index)
        plt.title('Visit Distribution')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'visit_distribution.png'), dpi=300)
        plt.close()
        
    def plot_missingness_heatmap(self, df: pd.DataFrame):
        # Sample max 1000 rows and 50 cols to avoid memory issues and huge plots
        sample_df = df.sample(min(1000, len(df))).iloc[:, :50]
        plt.figure(figsize=(12, 8))
        plt_sns.heatmap(sample_df.isnull(), cbar=False, cmap='viridis')
        plt.title('Missing Modality Heatmap (Sample)')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'missing_visit_heatmap.png'), dpi=300)
        plt.close()

    def generate_all(self, flow: dict, df: pd.DataFrame):
        self.plot_flow(flow)
        self.plot_visit_distribution(df)
        self.plot_missingness_heatmap(df)
