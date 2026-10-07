"""One inference bundle keeps the fitted preprocessing and classifier together."""

import numpy as np
import pandas as pd


class NetworkModel:
    """Validate and reorder feature columns before applying the training preprocessing."""

    def __init__(self, preprocessor, model, feature_names):
        self.preprocessor = preprocessor
        self.model = model
        self.feature_names = list(feature_names)

    def predict(self, x):
        """Predict encoded classes (0 corresponds to -1, 1 corresponds to 1)."""
        if not isinstance(x, pd.DataFrame) or x.empty:
            raise ValueError("Supply a non-empty CSV table.")
        if len(x.columns) != len(self.feature_names) or set(x.columns) != set(self.feature_names):
            raise ValueError("CSV columns must match the 30 input features; omit Result.")
        values = x.loc[:, self.feature_names].apply(pd.to_numeric, errors="raise")
        if np.isinf(values.to_numpy()).any():
            raise ValueError("Infinite feature values are not supported.")
        return self.model.predict(self.preprocessor.transform(values)).astype(int)
