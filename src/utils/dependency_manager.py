import importlib

class DependencyManager:
    @staticmethod
    def check_dependency(module_name):
        try:
            importlib.import_module(module_name)
            return True, "Available"
        except ImportError as e:
            return False, str(e)
            
    @staticmethod
    def validate_environment():
        dependencies = ['sklearn', 'lightgbm', 'xgboost', 'catboost', 'matplotlib', 'seaborn', 'shap', 'optuna']
        report = {}
        for dep in dependencies:
            is_avail, msg = DependencyManager.check_dependency(dep)
            report[dep] = {"Available": is_avail, "Message": msg}
        return report
