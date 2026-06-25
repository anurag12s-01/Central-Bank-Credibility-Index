import pandas as pd

def calculate_cbci(
    forecast_score: pd.Series,
    anchoring_score: pd.Series,
    currency_score: pd.Series,
    bond_score: pd.Series,
    consistency_score: pd.Series
) -> pd.Series:
    """
    Calculate the final Central Bank Credibility Index (CBCI) score.
    Weights based on methodology:
    - Forecast Accuracy: 20%
    - Inflation Anchoring: 30%
    - Currency Stability: 15%
    - Bond Market Confidence: 15%
    - Policy Consistency: 20%
    """
    weights = {
        'forecast': 0.20,
        'anchoring': 0.30,
        'currency': 0.15,
        'bond': 0.15,
        'consistency': 0.20
    }
    
    cbci = (
        forecast_score * weights['forecast'] +
        anchoring_score * weights['anchoring'] +
        currency_score * weights['currency'] +
        bond_score * weights['bond'] +
        consistency_score * weights['consistency']
    )
    
    return cbci.clip(0, 100)

if __name__ == "__main__":
    banks = ['FED', 'ECB']
    f_sc = pd.Series([85.0, 90.0], index=banks)
    a_sc = pd.Series([70.0, 80.0], index=banks)
    c_sc = pd.Series([95.0, 85.0], index=banks)
    b_sc = pd.Series([88.0, 92.0], index=banks)
    p_sc = pd.Series([100.0, 75.0], index=banks)
    
    final = calculate_cbci(f_sc, a_sc, c_sc, b_sc, p_sc)
    print("Final CBCI Scores:\n", final)
