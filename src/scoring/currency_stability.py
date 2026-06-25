import pandas as pd
import numpy as np
from scipy.stats import percentileofscore

def calculate_reer_volatility(reer_series: pd.Series, window: int = 90) -> pd.Series:
    """
    Calculate annualized realized volatility of the Real Effective Exchange Rate.
    Assumes daily data input.
    """
    log_returns = np.log(reer_series / reer_series.shift(1))
    volatility = log_returns.rolling(window=window).std() * np.sqrt(252)
    return volatility

def score_currency_stability(current_volatility: pd.Series, historical_volatilities: pd.Series) -> pd.Series:
    """
    Score currency stability using empirical CDF.
    Lower volatility yields a higher score (0-100).
    """
    scores = []
    clean_history = historical_volatilities.dropna()
    
    for vol in current_volatility:
        if pd.isna(vol) or len(clean_history) == 0:
            scores.append(np.nan)
        else:
            # P(V <= V_t)
            percentile = percentileofscore(clean_history, vol) / 100.0
            scores.append(100 * (1 - percentile))
            
    return pd.Series(scores, index=current_volatility.index).clip(0, 100)

if __name__ == "__main__":
    dates = pd.date_range("2023-01-01", periods=200)
    reer = pd.Series(100 + np.random.randn(200).cumsum(), index=dates)
    vol = calculate_reer_volatility(reer)
    scores = score_currency_stability(vol.tail(5), vol)
    print("Currency Stability Scores:\n", scores)
