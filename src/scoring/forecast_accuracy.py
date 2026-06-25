import pandas as pd

def calculate_forecast_error(forecasts: pd.Series, realized: pd.Series) -> pd.Series:
    """Calculate absolute forecast error."""
    return (forecasts - realized).abs()

def score_forecast_accuracy(errors: pd.Series) -> pd.Series:
    """
    Score forecast accuracy using cross-sectional Min-Max scaling.
    Lower error yields a higher score (0-100).
    """
    min_err = errors.min()
    max_err = errors.max()
    
    if max_err == min_err or pd.isna(max_err):
        return pd.Series(100.0, index=errors.index)
        
    scores = 100 * (1 - (errors - min_err) / (max_err - min_err))
    return scores.clip(0, 100)

if __name__ == "__main__":
    import numpy as np
    forecasts = pd.Series([2.1, 3.0, 1.5], index=['FED', 'ECB', 'BOE'])
    realized = pd.Series([2.5, 2.8, 4.0], index=['FED', 'ECB', 'BOE'])
    errors = calculate_forecast_error(forecasts, realized)
    scores = score_forecast_accuracy(errors)
    print("Forecast Accuracy Scores:\n", scores)
