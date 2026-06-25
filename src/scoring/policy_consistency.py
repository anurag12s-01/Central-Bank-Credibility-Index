import pandas as pd
import numpy as np

def calculate_alignment_score(nlp_sentiment: pd.Series, rate_move: pd.Series) -> pd.Series:
    """
    Calculate alignment between text sentiment (-1 to 1) and rate move (-1, 0, 1).
    Returns 1 if matching direction, 0.5 if one is neutral, 0 if contradicting.
    """
    scores = []
    for s, r in zip(nlp_sentiment, rate_move):
        if pd.isna(s) or pd.isna(r):
            scores.append(pd.NA)
            continue
            
        s_sign = 1 if s > 0 else (-1 if s < 0 else 0)
        r_sign = 1 if r > 0 else (-1 if r < 0 else 0)
        
        if s_sign == r_sign:
            scores.append(1.0)
        elif s_sign == 0 or r_sign == 0:
            scores.append(0.5)
        else:
            scores.append(0.0)
            
    return pd.Series(scores, index=nlp_sentiment.index)

def score_policy_consistency(alignment_scores: pd.Series, window: int = 12) -> pd.Series:
    """
    Calculate final consistency score via a rolling average, multiplied by 100.
    """
    # Ensure numeric for mean calculation
    numeric_scores = pd.to_numeric(alignment_scores, errors='coerce')
    rolling_avg = numeric_scores.rolling(window=window, min_periods=1).mean()
    return (rolling_avg * 100).clip(0, 100)

if __name__ == "__main__":
    sentiments = pd.Series([0.8, -0.5, 0.0, 0.2])
    rate_moves = pd.Series([0.25, -0.25, 0.0, -0.25])
    alignment = calculate_alignment_score(sentiments, rate_moves)
    scores = score_policy_consistency(alignment, window=2)
    print("Alignment:\n", alignment)
    print("Consistency Scores:\n", scores)
