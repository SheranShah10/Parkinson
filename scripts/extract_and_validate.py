#!/usr/bin/env python3
"""
Extract and Validate Pipeline
"""
import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.datasets.extraction import ArchiveExtractor
from src.datasets.validation import DatasetValidator
from src.datasets.schema import SchemaInferencer
from src.datasets.registry import DatasetRegistry
from src.visualization.validation_plots import ValidationVisualizer
from src.reporting.validation_reports import ValidationReporter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    unzip_dir = os.path.join(base_dir, 'data', 'unzipped')
    reports_dir = os.path.join(base_dir, 'reports')
    figures_dir = os.path.join(reports_dir, 'figures')
    
    logger.info("Starting Data Extraction and Validation Pipeline...")
    
    # 1. Extraction
    extractor = ArchiveExtractor(raw_dir, unzip_dir)
    extraction_logs = extractor.extract_all()
    
    # 2. Validation & Schema
    registry = DatasetRegistry()
    schemas = {}
    
    dirs_to_scan = [raw_dir, unzip_dir]
    for directory in dirs_to_scan:
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                
                # Skip zips and pdfs for validation since they aren't tabular
                if file.lower().endswith(('.zip', '.pdf', '.docx', '.png', '.jpg')):
                    continue
                    
                logger.info(f"Validating {file}...")
                val_result = DatasetValidator.validate(filepath)
                
                sch_result = {}
                if val_result.get("is_valid") and val_result.get("is_supported"):
                    sch_result = SchemaInferencer.infer(filepath)
                    schemas[file] = sch_result
                
                registry.register(filepath, val_result, sch_result, base_dir)
                
    reg_data = registry.get_registry()
    
    # 3. Reports
    logger.info("Generating reports...")
    reporter = ValidationReporter(reports_dir)
    reporter.generate_all(extraction_logs, reg_data, schemas)
    
    logger.info("Generating visualizations...")
    visualizer = ValidationVisualizer(figures_dir)
    visualizer.generate_all(extraction_logs, reg_data)
    
    logger.info("Pipeline complete.")

if __name__ == "__main__":
    main()
