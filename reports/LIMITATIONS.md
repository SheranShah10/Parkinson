# Project Limitations and Caveats

## Phase 8.2 (Temporal Sequence Construction) - Selection Bias
The temporal sequence architecture relies on the Phase 6 feature store (`master_features.parquet`), which acts as the foundational data source for deep learning sequence building.

**Caveat**: The temporal cohort contains exactly 1,467 patients, all of whom have exactly 6 longitudinal visits (`min: 6, max: 6`). This indicates a "complete case" analytical design executed during Phase 6 engineering.

**Impact**: This uniformly filtered structure systematically excludes patients who dropped out early or had irregular follow-up. In longitudinal Parkinson's Disease (PD) cohorts, early dropout is frequently correlated with faster progression or worse symptom burden. Therefore, the models trained on this sequence array may suffer from **selection bias**, leaning toward a healthier, more compliant patient profile.

*Note for Phase 8.6 (Publication Package)*: This limitation must be explicitly disclosed in the final manuscript and supplementary material, as it dictates the bounds within which the model's predictive validity holds.
