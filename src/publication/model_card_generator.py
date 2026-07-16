import os
class ModelCardGenerator:
    @staticmethod
    def generate_card(model_name, is_completed, out_dir):
        status = "Training executed natively." if is_completed else "Training not executed in current environment (Dependency skipped)."
        card = f"# Model Card: {model_name}\n\n## Overview\n{status}\n\n## Metrics\n"
        card += "Available.\n" if is_completed else "NOT AVAILABLE.\n"
        with open(os.path.join(out_dir, f"{model_name}.md"), "w") as f:
            f.write(card)
