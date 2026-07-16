"""
Target Generator Module
"""
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class TargetGenerator:
    def __init__(self):
        self.validation_log = []
        
    def sanitize_nhy(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'NHY' in df.columns:
            # 101, 999 etc to NaN
            df['TARGET_NHY'] = pd.to_numeric(df['NHY'], errors='coerce')
            invalid_mask = df['TARGET_NHY'] > 5.0
            num_invalid = invalid_mask.sum()
            if num_invalid > 0:
                logger.warning(f"Sanitized {num_invalid} invalid NHY values.")
                df.loc[invalid_mask, 'TARGET_NHY'] = np.nan
        else:
            df['TARGET_NHY'] = np.nan
        return df
        
    def generate_updrs_total(self, df: pd.DataFrame) -> pd.DataFrame:
        core_cols = ['NP1RTOT', 'NP1PTOT', 'NP2PTOT', 'NP3TOT', 'NP4TOT']
        avail_cols = [c for c in core_cols if c in df.columns]
        
        if avail_cols:
            df['TARGET_TOTAL_UPDRS'] = df[avail_cols].sum(axis=1, skipna=False)
            # If all were NaN, result is NaN. If partially missing, we should probably keep it NaN or use skipna=True.
            # For strict clinical targets, skipna=False is safer to avoid artificially low scores.
        else:
            df['TARGET_TOTAL_UPDRS'] = np.nan
            
        return df
        
    def generate_deltas(self, df: pd.DataFrame) -> pd.DataFrame:
        df['TARGET_UPDRS_DELTA_12'] = np.nan
        df['TARGET_UPDRS_DELTA_24'] = np.nan
        df['TARGET_UPDRS_DELTA_36'] = np.nan
        
        if 'TARGET_TOTAL_UPDRS' not in df.columns or 'EVENT_ID' not in df.columns or 'PATNO' not in df.columns:
            return df
            
        # Create mapping of (PATNO, EVENT_ID) -> UPDRS
        score_map = df.set_index(['PATNO', 'EVENT_ID'])['TARGET_TOTAL_UPDRS'].to_dict()
        
        def get_delta(row, target_visit):
            bl_score = row['TARGET_TOTAL_UPDRS']
            if pd.isna(bl_score): return np.nan
            fut_score = score_map.get((row['PATNO'], target_visit), np.nan)
            return fut_score - bl_score
            
        # Only compute deltas for Baseline (BL) visits to predict future progression
        bl_mask = df['EVENT_ID'] == 'BL'
        df.loc[bl_mask, 'TARGET_UPDRS_DELTA_12'] = df[bl_mask].apply(lambda r: get_delta(r, 'V04'), axis=1)
        df.loc[bl_mask, 'TARGET_UPDRS_DELTA_24'] = df[bl_mask].apply(lambda r: get_delta(r, 'V06'), axis=1)
        df.loc[bl_mask, 'TARGET_UPDRS_DELTA_36'] = df[bl_mask].apply(lambda r: get_delta(r, 'V08'), axis=1)
        
        return df

    def validate_targets(self, df: pd.DataFrame, filepath: str):
        lines = ["# Target Generation Validation\n"]
        lines.append(f"- **Total Rows**: {len(df)}")
        for t in ['TARGET_NHY', 'TARGET_TOTAL_UPDRS', 'TARGET_UPDRS_DELTA_12']:
            if t in df.columns:
                miss = df[t].isnull().sum()
                lines.append(f"- **{t}**: {len(df)-miss} valid, {miss} missing")
            else:
                lines.append(f"- **{t}**: NOT FOUND")
                
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
