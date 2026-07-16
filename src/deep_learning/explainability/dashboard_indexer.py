import json
import os

class DashboardIndexer:
    @staticmethod
    def generate_indices(base_dir):
        # Generates metadata/patient_explanation_index.json
        index = {"patients": [], "biomarkers": []}
        index_path = os.path.join(base_dir, "metadata", "patient_explanation_index.json")
        with open(index_path, "w") as f:
            json.dump(index, f)
        return index_path
