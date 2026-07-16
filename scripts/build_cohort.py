#!/usr/bin/env python3
import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing.cohort import CohortBuilder
from src.preprocessing.alignment import LongitudinalAligner
from src.preprocessing.checks import ConsistencyValidator
from src.visualization.cohort_plots import CohortVisualizer
from src.reporting.cohort_reports import CohortReporter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    unzip_dir = os.path.join(base_dir, 'data', 'unzipped')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    reports_dir = os.path.join(base_dir, 'reports')
    figures_dir = os.path.join(reports_dir, 'figures')
    
    os.makedirs(processed_dir, exist_ok=True)
    
    builder = CohortBuilder()
    participant_status_path = None
    for d in [raw_dir, unzip_dir]:
        for root, _, files in os.walk(d):
            for file in files:
                if 'participant_status' in file.lower() and file.endswith('.csv'):
                    participant_status_path = os.path.join(root, file)
                    break
            if participant_status_path: break
        if participant_status_path: break
                
    cohort_df = builder.build_cohort(participant_status_path)
    flow_log = builder.get_flow_log()
    
    # NEW ALIGNER
    merge_policies = os.path.join(base_dir, 'configs', 'datasets', 'merge_policies.yaml')
    aligner = LongitudinalAligner(cohort_df, merge_policies)
    
    for d in [raw_dir, unzip_dir]:
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.csv') and 'participant_status' not in file.lower():
                    aligner.align_dataset(file, os.path.join(root, file))
                    
    master_df = aligner.finalize(reports_dir)
    
    checks = ConsistencyValidator.validate(master_df)
    
    master_df.to_csv(os.path.join(processed_dir, 'master_longitudinal_dataset.csv'), index=False)
    master_df.to_parquet(os.path.join(processed_dir, 'master_longitudinal_dataset.parquet'), index=False)
    
    reporter = CohortReporter(reports_dir)
    reporter.generate_markdown(checks, flow_log, master_df)
    
    viz = CohortVisualizer(figures_dir)
    viz.generate_all(flow_log, master_df)
    
    logger.info("Phase 4 Pipeline completed successfully.")

if __name__ == "__main__":
    main()
