# Configuration Guide
## Hierarchy
- `base.yaml`: Project defaults
- `paths.yaml`: Relative paths
- `constants/`: Hardcoded references (PATNO, EVENT_ID)
## Best Practices
- Never hardcode paths in source code.
- Always load configs via the central config manager.
- Subclass core models and register them using `@MODELS.register()`.