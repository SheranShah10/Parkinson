class HardwareValidator:
    @staticmethod
    def audit():
        report = {"Status": "PASS", "GPUs": 0, "VRAM": "0MB"}
        try:
            import torch
            if torch.cuda.is_available():
                report["GPUs"] = torch.cuda.device_count()
                report["VRAM"] = f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB"
        except ImportError:
            report["Status"] = "FAIL: Missing torch"
        return report
