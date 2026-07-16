#!/usr/bin/env python3
"""
Discover Datasets Script

Entry point to run the automated dataset discovery pipeline.
"""

import os
import sys
import logging

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.datasets.discovery import DiscoveryPipeline
from src.visualization.inventory_plots import InventoryVisualizer
from src.reporting.inventory_reports import InventoryReporter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dirs = [
        os.path.join(base_dir, 'data', 'raw'),
        os.path.join(base_dir, 'data', 'unzipped')
    ]
    reports_dir = os.path.join(base_dir, 'reports')
    figures_dir = os.path.join(reports_dir, 'figures')
    
    logger.info("Starting Dataset Discovery Pipeline...")
    
    pipeline = DiscoveryPipeline(data_dirs)
    pipeline.scan()
    
    inventory = pipeline.get_inventory()
    relationships = pipeline.get_relationships()
    
    logger.info(f"Discovered {len(inventory)} datasets. Generating reports...")
    
    reporter = InventoryReporter(reports_dir)
    reporter.generate_all(inventory, relationships)
    
    logger.info("Generating visualizations...")
    visualizer = InventoryVisualizer(figures_dir)
    visualizer.generate_all(inventory)
    
    logger.info(f"Discovery complete. Outputs saved to {reports_dir}")

if __name__ == "__main__":
    main()
