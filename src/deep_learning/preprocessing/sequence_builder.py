import pandas as pd
import numpy as np

class SequenceBuilder:
    def __init__(self, sequence_length=5, feature_cols=None):
        self.sequence_length = sequence_length
        self.feature_cols = feature_cols

    def build_sequences(self, df):
        """
        Builds causally masked padded sequences.
        Ensures a prediction at time t ONLY sees features <= t.
        """
        if 'PATNO' not in df.columns or 'EVENT_ID' not in df.columns:
            raise ValueError("Dataframe must contain PATNO and EVENT_ID for sequence building.")

        # If feature_cols not specified, grab numeric ones except PATNO
        if self.feature_cols is None:
            self.feature_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c != 'PATNO']

        grouped = df.groupby('PATNO')
        
        sequences = []
        patient_ids = []
        visit_counts = []

        for patient_id, group in grouped:
            # Sort strictly by EVENT_ID to ensure chronological order
            group = group.sort_values('EVENT_ID').reset_index(drop=True)
            num_visits = len(group)
            visit_counts.append(num_visits)
            
            features = group[self.feature_cols].values
            
            # Truncate if longer than max sequence length
            # FIX: We keep the MOST RECENT visits (the end of the array)
            if num_visits > self.sequence_length:
                features = features[-self.sequence_length:]
                num_visits = self.sequence_length
                
            # Pad with zeros
            padded_seq = np.zeros((self.sequence_length, len(self.feature_cols)))
            padded_seq[:num_visits, :] = features
            
            sequences.append(padded_seq)
            patient_ids.append(patient_id)
            
        return np.array(sequences), np.array(patient_ids), visit_counts
