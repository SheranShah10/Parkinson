"""
Configuration Validator
"""
import os
import yaml
import logging

class ConfigValidator:
    def __init__(self, configs_dir: str):
        self.configs_dir = configs_dir
        self.errors = []
        self.parsed_keys = set()
        
    def validate(self):
        for root, _, files in os.walk(self.configs_dir):
            for file in files:
                if file.endswith('.yaml'):
                    self._check_file(os.path.join(root, file))
        return self.errors
        
    def _check_file(self, filepath: str):
        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    self._recursively_check_keys(data, os.path.basename(filepath))
        except Exception as e:
            self.errors.append(f"Failed to parse {filepath}: {str(e)}")
            
    def _recursively_check_keys(self, d: dict, source: str, prefix: str = ""):
        for k, v in d.items():
            full_key = f"{prefix}.{k}" if prefix else k
            # Optional: Check duplicates across entirely different files if strict
            # For now, just ensuring it reads fine.
            if isinstance(v, dict):
                self._recursively_check_keys(v, source, full_key)
