import os
import hashlib

class VersionValidator:
    @staticmethod
    def audit(feature_store_path="C:/Users/Sheran/Desktop/Parkinson/data/feature_store/feature_store_v1/master_features.parquet"):
        if not os.path.exists(feature_store_path):
            return {"Status": "FAIL", "Message": f"Feature store file not found: {feature_store_path}"}
            
        try:
            # REAL HASH CALCULATION
            sha256_hash = hashlib.sha256()
            with open(feature_store_path, "rb") as f:
                # Read and update hash in chunks
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            file_hash = sha256_hash.hexdigest()
            return {"Status": "PASS", "FileHash": file_hash, "File": feature_store_path}
        except Exception as e:
             return {"Status": "FAIL", "Message": str(e)}
