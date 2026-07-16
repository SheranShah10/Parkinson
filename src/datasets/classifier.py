"""
Classifier Module

Responsibility: Automatically categorize datasets based on filename and metadata rules.
"""

import re
from typing import Dict, Any, List

class DatasetClassifier:
    """Rule-based dataset classifier."""
    
    CATEGORIES = {
        "Imaging (MRI)": r"(?i)(mri|dti|fmri)",
        "Imaging (DaTSCAN)": r"(?i)(datscan|spect)",
        "Clinical (Motor)": r"(?i)(updrs|motor|tremor)",
        "Clinical (Non-Motor)": r"(?i)(moca|cog|neuropsy|depression|sleep)",
        "Genetics": r"(?i)(genet|dna|wgs|gwas|snp)",
        "Proteomics": r"(?i)(proteom|protein)",
        "Metabolomics": r"(?i)(metabol)",
        "Biospecimens": r"(?i)(blood|csf|plasma|serum|urine|biospecimen)",
        "Digital Biomarkers (Wearables/Sensors)": r"(?i)(sensor|wearable|actigraph|watch)",
        "Digital Biomarkers (Smartphone)": r"(?i)(smart|phone|app|voice|tapping)",
        "Demographics": r"(?i)(demog|screen|enroll)",
        "Medication": r"(?i)(med|conmed|levodopa)"
    }
    
    @staticmethod
    def classify(filename: str, column_names: List[str]) -> str:
        """Classifies the dataset based on filename and columns."""
        combined_text = filename + " " + " ".join(column_names)
        
        for category, pattern in DatasetClassifier.CATEGORIES.items():
            if re.search(pattern, combined_text):
                return category
                
        return "Unknown"
