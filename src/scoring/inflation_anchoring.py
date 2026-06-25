import pandas as pd
import numpy as np

def calculate_inflation_deviation(actual_inflation: pd.Series, target_inflation: pd.Series) -> pd.Series:
    """Calculate absolute deviation from the target inflation rate."""
    return (actual_inflation - target_inflation).abs()

def score_inflation_anchoring(deviations: pd.Series, threshold: float = 4.0) -> pd.Series:
    """
    Score inflation anchoring based on absolute deviation.
    Threshold K sets the point where the score drops to 0 (default 4.0%).
    """
    scores = 100 * np.maximum(0, 1 - (deviations / threshold))
    return pd.Series(scores, index=deviations.index).clip(0, 100)

if __name__ == "__main__":
    actual = pd.Series([2.2, 5.0, 1.0], index=['FED', 'ECB', 'BOJ'])
    target = pd.Series([2.0, 2.0, 2.0], index=['FED', 'ECB', 'BOJ'])
    deviations = calculate_inflation_deviation(actual, target)
    scores = score_inflation_anchoring(deviations)
    print("Inflation Anchoring Scores:\n", scores)
