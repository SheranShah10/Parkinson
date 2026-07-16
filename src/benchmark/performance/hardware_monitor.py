import platform

class HardwareMonitor:
    @staticmethod
    def get_hardware_stats():
        stats = {
            "OS": platform.system(),
            "Processor": platform.processor(),
            "CPU_Count_Logical": None,
            "RAM_GB": None,
            "GPU_Available": False,
            "GPUs": []
        }
        
        try:
            import psutil
            stats["CPU_Count_Logical"] = psutil.cpu_count()
            stats["RAM_GB"] = round(psutil.virtual_memory().total / (1024**3), 2)
        except ImportError:
            stats["PSUTIL_ERROR"] = "psutil module not installed"
            
        try:
            import torch
            if torch.cuda.is_available():
                stats["GPU_Available"] = True
                for i in range(torch.cuda.device_count()):
                    prop = torch.cuda.get_device_properties(i)
                    stats["GPUs"].append({
                        "Name": prop.name,
                        "VRAM_GB": round(prop.total_memory / (1024**3), 2)
                    })
        except ImportError:
            stats["TORCH_ERROR"] = "torch module not installed"
            
        return stats
