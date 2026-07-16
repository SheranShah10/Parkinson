"""
Alignment Orchestrator
"""
import pandas as pd
import os
import logging
from src.preprocessing.join_engine import JoinEngine
from src.preprocessing.target_generator import TargetGenerator
from src.preprocessing.merge_validator import MergeValidator

logger = logging.getLogger(__name__)

class LongitudinalAligner:
    def __init__(self, cohort_df: pd.DataFrame, merge_policies_path: str):
        self.master_df = cohort_df.copy()
        if 'EVENT_ID' not in self.master_df.columns:
            events = ['BL', 'V04', 'V06', 'V08', 'V10', 'V12']
            dfs = []
            for ev in events:
                temp = self.master_df.copy()
                temp['EVENT_ID'] = ev
                dfs.append(temp)
            self.master_df = pd.concat(dfs, ignore_index=True)
            
        self.join_engine = JoinEngine(merge_policies_path)
        self.target_gen = TargetGenerator()
        self.validator = MergeValidator()
        
    def align_dataset(self, filename: str, filepath: str):
        try:
            df = pd.read_csv(filepath, low_memory=False)
            self.master_df = self.join_engine.execute_join(self.master_df, df, filename)
        except Exception as e:
            logger.error(f"Failed to align {filename}: {str(e)}")
            
    def finalize(self, reports_dir: str) -> pd.DataFrame:
        self.master_df = self.target_gen.sanitize_nhy(self.master_df)
        self.master_df = self.target_gen.generate_updrs_total(self.master_df)
        self.master_df = self.target_gen.generate_deltas(self.master_df)
        
        self.target_gen.validate_targets(self.master_df, os.path.join(reports_dir, 'target_generation_validation.md'))
        self.join_engine.duplicate_resolver.generate_report(os.path.join(reports_dir, 'duplicate_analysis_report.md'))
        self.validator.write_diagnostics(self.join_engine.diagnostics, os.path.join(reports_dir, 'merge_diagnostics.md'))
        
        return self.master_df
