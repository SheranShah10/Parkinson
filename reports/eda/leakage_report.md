# Target Leakage Detection Report

## Identifier Leakage
The following variables are strict identifiers and must NOT be used as predictors:
- PATNO
- EVENT_ID
- INFODT

## High Correlation Leakage (>0.99)
The following features exhibit >0.99 correlation with targets and represent potential leakage:
- **NHY** correlates with TARGET_NHY (1.0000)

## Future-Derived Variables
Variables containing 'DELTA', 'CHANGE', or derived targets from future dates must be excluded during cross-sectional prediction tasks.