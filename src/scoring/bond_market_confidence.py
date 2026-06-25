import pandas as pd
import numpy as np

def calculate_yield_volatility(yield_series: pd.Series, window: int = 30) -> pd.Series:
    """Calculate rolling volatility of changes in 10-year bond yields."""
    yield_changes = yield_series.diff()
    return yield_changes.rolling(window=window).std()

def score_bond_confidence(volatilities: pd.Series) -> pd.Series:
    """
    Score bond market confidence using cross-sectional Min-Max scaling.
    Lower volatility yields a higher score (0-100).
    """
    min_vol = volatilities.min()
    max_vol = volatilities.max()
    
    if max_vol == min_vol or pd.isna(max_vol):
        return pd.Series(100.0, index=volatilities.index)
        
    scores = 100 * (1 - (volatilities - min_vol) / (max_vol - min_vol))
    return scores.clip(0, 100)

if __name__ == "__main__":
    vols = pd.Series([0.05, 0.12, 0.08], index=['FED', 'ECB', 'BOE'])
    scores = score_bond_confidence(vols)
    print("Bond Market Confidence Scores:\n", scores)
