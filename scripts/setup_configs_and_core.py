#!/usr/bin/env python3
"""
Setup Configs and Core Script
"""
import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config.validator import ConfigValidator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_docs(base_dir):
    docs = [
        "# Configuration Guide",
        "## Hierarchy",
        "- `base.yaml`: Project defaults",
        "- `paths.yaml`: Relative paths",
        "- `constants/`: Hardcoded references (PATNO, EVENT_ID)",
        "## Best Practices",
        "- Never hardcode paths in source code.",
        "- Always load configs via the central config manager.",
        "- Subclass core models and register them using `@MODELS.register()`."
    ]
    with open(os.path.join(base_dir, 'docs', 'configuration_guide.md'), 'w') as f:
        f.write("\n".join(docs))

def generate_validation_report(base_dir, errors):
    lines = ["# Configuration Validation Report\n"]
    if errors:
        for e in errors:
            lines.append(f"- [ERROR] {e}")
    else:
        lines.append("All YAML configurations successfully parsed and validated. No duplications or syntax errors detected.")
        
    with open(os.path.join(base_dir, 'reports', 'config_validation_report.md'), 'w') as f:
        f.write("\n".join(lines))

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    configs_dir = os.path.join(base_dir, 'configs')
    
    logger.info("Validating configuration files...")
    validator = ConfigValidator(configs_dir)
    errors = validator.validate()
    
    logger.info("Generating reports and docs...")
    generate_validation_report(base_dir, errors)
    generate_docs(base_dir)
    logger.info("Configuration and Core setup complete.")

if __name__ == "__main__":
    main()
