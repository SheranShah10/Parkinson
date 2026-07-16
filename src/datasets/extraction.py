"""
Extraction Module

Responsibility: Safely extract ZIP archives without overwriting or renaming.
"""
import os
import zipfile
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ArchiveExtractor:
    def __init__(self, raw_dir: str, unzip_dir: str):
        self.raw_dir = raw_dir
        self.unzip_dir = unzip_dir
        os.makedirs(self.unzip_dir, exist_ok=True)
        self.extraction_logs: List[Dict[str, Any]] = []

    def extract_all(self):
        for root, _, files in os.walk(self.raw_dir):
            for file in files:
                if file.lower().endswith('.zip'):
                    filepath = os.path.join(root, file)
                    self._extract_single(filepath)
        return self.extraction_logs

    def _extract_single(self, filepath: str):
        filename = os.path.basename(filepath)
        folder_name = os.path.splitext(filename)[0]
        # Replace spaces or weird chars with underscores for the folder name
        folder_name = "".join([c if c.isalnum() else "_" for c in folder_name])
        target_dir = os.path.join(self.unzip_dir, folder_name)
        
        log_entry = {
            "archive_name": filename,
            "status": "success",
            "extracted_files": 0,
            "target_dir": target_dir,
            "error_message": None
        }

        if os.path.exists(target_dir):
            logger.info(f"Target directory {target_dir} already exists. Skipping extraction for {filename}.")
            log_entry["status"] = "skipped_exists"
            self.extraction_logs.append(log_entry)
            return

        logger.info(f"Extracting {filename} to {target_dir}...")
        try:
            os.makedirs(target_dir, exist_ok=True)
            with zipfile.ZipFile(filepath, 'r') as z:
                # Basic protection against Zip Slip
                for member in z.namelist():
                    member_path = os.path.abspath(os.path.join(target_dir, member))
                    if not member_path.startswith(os.path.abspath(target_dir)):
                        raise Exception("Zip Slip vulnerability detected.")
                z.extractall(target_dir)
                log_entry["extracted_files"] = len(z.namelist())
        except Exception as e:
            logger.error(f"Failed to extract {filename}: {str(e)}")
            log_entry["status"] = "error"
            log_entry["error_message"] = str(e)
            
        self.extraction_logs.append(log_entry)
