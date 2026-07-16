"""
Join Engine Module
"""
import pandas as pd
import logging
import yaml
import os
from typing import Tuple, Dict

from src.preprocessing.duplicate_resolver import DuplicateResolver

logger = logging.getLogger(__name__)

class JoinEngine:
    def __init__(self, merge_policies_path: str):
        with open(merge_policies_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.default_strategy = self.config.get("default", "one_to_one")
        self.policies = self.config.get("policies", {})
        self.duplicate_resolver = DuplicateResolver()
        self.diagnostics: list = []
        
    def _determine_policy(self, filename: str) -> Tuple[str, list]:
        name_lower = filename.lower()
        for domain, pol in self.policies.items():
            # A bit of heuristic mapping since file names vary
            if domain.lower() in name_lower or \
               (domain == 'Motor' and 'updrs' in name_lower) or \
               (domain == 'Proteomics' and 'saa' in name_lower) or \
               (domain == 'Smartphone' and 'roche' in name_lower) or \
               (domain == 'Biospecimens' and 'biospecimen' in name_lower):
                return pol.get("strategy", "one_to_one"), pol.get("identifiers", ["PATNO", "EVENT_ID"])
        return self.default_strategy, ["PATNO", "EVENT_ID"]

    def execute_join(self, master_df: pd.DataFrame, df: pd.DataFrame, filename: str) -> pd.DataFrame:
        strategy, identifiers = self._determine_policy(filename)
        
        initial_master = len(master_df)
        initial_df = len(df)
        
        # Standardize EVENT_ID if it's CLINICAL_EVENT
        if "CLINICAL_EVENT" in identifiers and "CLINICAL_EVENT" in df.columns:
            df = df.rename(columns={"CLINICAL_EVENT": "EVENT_ID"})
            identifiers = ["PATNO", "EVENT_ID"]
            
        if not set(identifiers).issubset(df.columns):
            logger.warning(f"Skipping {filename}: Missing identifiers {identifiers}")
            return master_df
            
        # Resolve duplicates
        df = self.duplicate_resolver.resolve(df, filename, identifiers, strategy)
        resolved_df_len = len(df)
        
        # Prefix columns except keys and known targets
        protected_cols = ['PATNO', 'EVENT_ID', 'INFODT', 'NHY', 'NP1RTOT', 'NP1PTOT', 'NP2PTOT', 'NP3TOT', 'NP4TOT']
        prefix = filename.split('_')[0][:5] + "_" if '_' in filename else filename[:5] + "_"
        rename_dict = {c: f"{prefix}{c}" for c in df.columns if c.upper() not in protected_cols}
        df = df.rename(columns=rename_dict)
        
        if strategy == "one_to_one" or strategy == "pivot":
            merged = pd.merge(master_df, df, on=['PATNO', 'EVENT_ID'], how='left', suffixes=('', '_dup'))
        elif strategy == "aggregate":
            # Simple aggregate mock (group by identifiers and take first for now or sum)
            df_agg = df.groupby(['PATNO', 'EVENT_ID']).first().reset_index()
            merged = pd.merge(master_df, df_agg, on=['PATNO', 'EVENT_ID'], how='left', suffixes=('', '_dup'))
        elif strategy == "sequence":
            # For sequence, we won't explode master_df. We just extract boolean flag or count.
            seq_stats = df.groupby('PATNO').size().reset_index(name=f'{prefix}count')
            merged = pd.merge(master_df, seq_stats, on='PATNO', how='left', suffixes=('', '_dup'))
        else:
            merged = master_df
            
        # Cleanup
        dups = [c for c in merged.columns if c.endswith('_dup')]
        if dups:
            merged = merged.drop(columns=dups)
            
        final_len = len(merged)
        
        self.diagnostics.append({
            "dataset": filename,
            "strategy": strategy,
            "master_before": initial_master,
            "df_before": initial_df,
            "df_resolved": resolved_df_len,
            "master_after": final_len,
            "dropped": initial_df - resolved_df_len
        })
        
        return merged
