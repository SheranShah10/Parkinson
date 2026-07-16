#!/usr/bin/env python3
"""
Build Metadata Registry Script
"""
import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.metadata.inspector import DatasetInspector
from src.metadata.relationship_mapper import RelationshipMapper
from src.metadata.schema_generator import SchemaGenerator
from src.metadata.validator import MetadataValidator
from src.reporting.metadata_reports import MetadataReporter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    unzip_dir = os.path.join(base_dir, 'data', 'unzipped')
    reports_dir = os.path.join(base_dir, 'reports')
    meta_dir = os.path.join(base_dir, 'metadata')
    
    logger.info("Starting Metadata Registry Generation...")
    
    inspector = DatasetInspector()
    mapper = RelationshipMapper()
    schema_gen = SchemaGenerator()
    validator = MetadataValidator()
    reporter = MetadataReporter(reports_dir, meta_dir)
    
    datasets = []
    schemas = {}
    
    for d in [raw_dir, unzip_dir]:
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.csv'):
                    filepath = os.path.join(root, file)
                    logger.info(f"Inspecting {file}...")
                    stats = inspector.inspect(filepath)
                    datasets.append(stats)
                    schemas[file] = schema_gen.generate_schema(stats)
                    
    logger.info("Mapping relationships...")
    rels = mapper.map_relationships(datasets)
    mermaid = mapper.generate_mermaid_er(rels["relationships"])
    
    logger.info("Validating metadata...")
    errors = validator.validate(datasets)
    
    logger.info("Writing reports and catalogs...")
    reporter.write_inventories(datasets)
    reporter.write_schemas(schemas)
    reporter.write_relationships(rels, mermaid)
    reporter.write_data_dictionary(schemas)
    reporter.write_validation_report(errors)
    reporter.write_modality_catalog(datasets)
    
    logger.info("Metadata Generation complete.")

if __name__ == "__main__":
    main()
