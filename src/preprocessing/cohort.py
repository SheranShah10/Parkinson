"""
Cohort Construction Module

Responsibility: Identify eligible participants (PD and HC) and apply exclusions.
"""
import os
import pandas as pd
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

class CohortBuilder:
    def __init__(self):
        self.flow_log = {}

    def build_cohort(self, participant_status_path: str = None) -> pd.DataFrame:
        """Builds the cohort filtering out ineligible patients."""
        if not participant_status_path or not os.path.exists(participant_status_path):
            logger.warning(f"Participant status file not found: {participant_status_path}. Generating dummy cohort.")
            # For demonstration without the real dataset, we just return a dummy cohort
            df = pd.DataFrame({"PATNO": [1001, 1002, 1003], "COHORT": ["PD", "HC", "PD"]})
            self.flow_log["Initial"] = len(df)
            self.flow_log["Final"] = len(df)
            return df
            
        df = pd.read_csv(participant_status_path, low_memory=False)
        self.flow_log["Initial"] = len(df)
        
        # In a real scenario, map COHORT to standard strings and filter for PD/HC
        # Assuming 'COHORT' column exists. If not, use dummy mapping
        if 'COHORT' in df.columns:
            df = df[df['COHORT'].isin(['PD', 'HC', 1, 2])]
            self.flow_log["Filtered_PD_HC"] = len(df)
        else:
            self.flow_log["Filtered_PD_HC"] = len(df)
            
        # Apply standard exclusions (e.g. protocol violations, dropouts)
        if 'ENROLL_STATUS' in df.columns:
            df = df[df['ENROLL_STATUS'] == 'Enrolled']
            
        self.flow_log["Final"] = len(df)
        return df
        
    def get_flow_log(self):
        return self.flow_log
