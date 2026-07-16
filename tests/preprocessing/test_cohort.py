import pandas as pd
import numpy as np
from src.preprocessing.target_generator import TargetGenerator
from src.preprocessing.duplicate_resolver import DuplicateResolver

def test_duplicate_resolver():
    df = pd.DataFrame({
        'PATNO': [1, 1, 2],
        'EVENT_ID': ['BL', 'BL', 'BL'],
        'VAL': [10, 20, 30]
    })
    resolver = DuplicateResolver()
    res = resolver.resolve(df, 'test', ['PATNO', 'EVENT_ID'], 'one_to_one')
    assert len(res) == 2
    assert res.iloc[0]['VAL'] == 10

def test_target_deltas():
    df = pd.DataFrame({
        'PATNO': [1, 1, 1],
        'EVENT_ID': ['BL', 'V04', 'V06'],
        'TARGET_TOTAL_UPDRS': [10.0, 15.0, 22.0]
    })
    gen = TargetGenerator()
    res = gen.generate_deltas(df)
    assert res.loc[res['EVENT_ID'] == 'BL', 'TARGET_UPDRS_DELTA_12'].iloc[0] == 5.0
    assert res.loc[res['EVENT_ID'] == 'BL', 'TARGET_UPDRS_DELTA_24'].iloc[0] == 12.0
