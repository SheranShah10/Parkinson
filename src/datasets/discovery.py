"""
Discovery Orchestrator

Responsibility: Walk data directories and invoke profilers, classifiers, and mappers.
"""

import os
import glob
from typing import List, Dict, Any
from .profiler import DatasetProfiler
from .classifier import DatasetClassifier
from .relationships import RelationshipMapper

import logging
logger = logging.getLogger(__name__)

class DiscoveryPipeline:
    """Pipeline to discover and catalog datasets."""
    
    SUPPORTED_EXTENSIONS = {'.csv', '.tsv', '.txt', '.xls', '.xlsx', '.parquet', '.json', '.zip'}
    
    def __init__(self, directories: List[str]):
        self.directories = directories
        self.inventory: List[Dict[str, Any]] = []
        self.mapper = RelationshipMapper()
        
    def scan(self):
        """Scans directories recursively and profiles datasets."""
        for directory in self.directories:
            if not os.path.exists(directory):
                logger.warning(f"Directory {directory} does not exist. Skipping.")
                continue
                
            for root, _, files in os.walk(directory):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in self.SUPPORTED_EXTENSIONS:
                        filepath = os.path.join(root, file)
                        logger.info(f"Discovering: {filepath}")
                        
                        # Profile
                        meta = DatasetProfiler.profile(filepath, ext)
                        
                        # Classify (if tabular)
                        cols = meta.get("column_names", [])
                        meta["category"] = DatasetClassifier.classify(file, cols)
                        
                        # Track relationships
                        self.mapper.add_dataset(file, cols)
                        
                        # Add relative path
                        meta["relative_path"] = os.path.relpath(filepath, start=os.path.dirname(os.path.dirname(self.directories[0])))
                        
                        self.inventory.append(meta)
                        
    def get_inventory(self) -> List[Dict[str, Any]]:
        return self.inventory
        
    def get_relationships(self) -> List[Dict[str, Any]]:
        return self.mapper.generate_relationship_map()
