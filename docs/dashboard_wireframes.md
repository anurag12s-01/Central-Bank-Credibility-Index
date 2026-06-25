# Central Bank Credibility Index (CBCI) - Executive Dashboard Wireframes

**Target Audience:** JPMorgan Economists, BlackRock Strategists, Deloitte Risk Consultants
**Design Language:** Institutional Dark Mode (Deep charcoals `#121212`, accented with vibrant teal `#00E5FF` for positive metrics, and crimson `#FF1744` for negative metrics/shocks). Clean, data-dense, zero-clutter.

---

## Page 1: Global Rankings (The Executive Summary)
*Goal: 5-second snapshot of global monetary credibility.*

```text
+-----------------------------------------------------------------------------+
| [Logo] Central Bank Credibility Index (CBCI)        [Year: 2026 ▼] [Export] |
+-----------------------------------------------------------------------------+
|  Global Avg CBCI    |  Most Credible       |  Biggest YTD Drop              |
|  64.2 (-2.1)        |  SNB (89.1)          |  BOE (-14.3)                   |
+---------------------+----------------------+--------------------------------+
|                                      |                                      |
|       [ GLOBAL CHOROPLETH MAP ]      |      [ CREDIBILITY LEADERBOARD ]     |
|                                      |                                      |
|   - Countries shaded from Dark Red   |   1. Swiss National Bank (89.1)  ▲   |
|     (Score 0) to Cyan (Score 100)    |   2. Federal Reserve     (85.4)  ▼   |
|   - Hover tooltips show 5-pillar     |   3. Bank of Japan       (79.2)  -   |
|     score breakdown.                 |   ...                                |
|                                      |   10. Central Bank of X  (42.1)  ▼   |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
```

---

## Page 2: Historical Trends (Macro Timeline)
*Goal: Track the erosion or building of trust since the 2010s.*

```text
+-----------------------------------------------------------------------------+
|  Historical Trends | Select CB: [ FED x ] [ ECB x ]          [2010 - 2026]  |
+-----------------------------------------------------------------------------+
|                                                                             |
|      [ MULTI-LINE CHART: CBCI SCORE OVER TIME (2010 - 2026) ]               |
|                                                                             |
|  100 |                                            *--------- FED            |
|      |        *-----------*                      /                          |
|   75 |-------/             \----------*---------*                           |
|      |                                 \                                    |
|   50 |                                  *------------------- ECB            |
|      |                                                                      |
|      +-------------------------------------------------------------         |
|        2010       2014       2018       2022       2026                     |
|                                                                             |
|  * Shaded vertical bands indicate major macro events (e.g., COVID, Taper)   |
+-----------------------------------------------------------------------------+
```

---

## Page 3: Forecast Accuracy (The 'Blind Spot' Analysis)
*Goal: Expose which central banks consistently fail to predict their own mandates.*

```text
+-----------------------------------------------------------------------------+
|  Forecast Accuracy | Sub-Index: [ Inflation Forecast MAE ]                  |
+-----------------------------------------------------------------------------+
|   [ SCATTER PLOT: FORECAST ERROR vs. REALIZED INFLATION ]                   |
|                                                                             |
|       High Realized Infl.                                                   |
|       |                     (BOE)                                           |
|       |                                                                     |
|       |            (ECB)             (FED)                                  |
|       |                                                                     |
|-------+--------------------------------------------- High Forecast Error    |
|       |   (SNB)                                                             |
|       |            (BOJ)                                                    |
+-------+---------------------------------------------------------------------+
| [ BAR CHART: Historical MAE by CB ] | [ HEATMAP: Error Magnitude by Year ]  |
| FED ||||||                          |       2023  2024  2025  2026          |
| ECB ||||||||||                      | FED   Dark  Med   Light Light         |
| BOE ||||||||||||||                  | ECB   Dark  Dark  Med   Light         |
+-------------------------------------+---------------------------------------+
```

---

## Page 4: Policy Shock Monitor (The NLP Quadrant)
*Goal: Quantify forward guidance efficacy for strategists pricing rate curves.*

```text
+-----------------------------------------------------------------------------+
|  Policy Shock Monitor | NLP Statement Sentiment vs. Actual Rate Move        |
+-----------------------------------------------------------------------------+
|                                                                             |
|         "DOVISH SHOCK" (Score: 0)  |  "HAWKISH ALIGNMENT" (Score: 100)      |
|           Dovish Talk -> Hiked     |    Hawkish Talk -> Hiked               |
|  HIKE  ----------------------------+-----------------------------------     |
|         * BOE (Q3 2023)            |       * FED (Q1 2024)                  |
|                                    |       * ECB (Q2 2024)                  |
|                                    |                                        |
|  HOLD  ----------------------------+-----------------------------------     |
|                                    |                                        |
|                                    |                                        |
|  CUT   ----------------------------+-----------------------------------     |
|          * BOJ (Q4 2025)           |       * SNB (Q1 2026)                  |
|          "DOVISH ALIGNMENT" (100)  |    "HAWKISH SHOCK" (0)                 |
|                                                                             |
|             DOVISH NLP <-------------+-------------> HAWKISH NLP            |
+-----------------------------------------------------------------------------+
```
> [!IMPORTANT]
> **Risk Consultant Value-Add:** This specific quadrant identifies periods where central bank communication actively destroyed market pricing, a critical input for portfolio risk models.

---

## Page 5: Currency Stability (FX Volatility)
*Goal: Analyze fiat stability through the lens of REER volatility.*

```text
+-----------------------------------------------------------------------------+
|  Currency Stability | Real Effective Exchange Rate (REER) Volatility        |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [ VOLATILITY GAUGE (Current) ]  |  [ ROLLING 90-DAY REER VOLATILITY ]      |
|                                  |                                          |
|      ( ) Low (SNB, FED)          |    Line chart tracking the V_fx          |
|     (   ) Medium (ECB)           |    formula output over the last 5 years. |
|    (     ) High (BOC, RBA)       |    Peaks indicate loss of FX confidence. |
|                                  |                                          |
+----------------------------------+------------------------------------------+
|  [ FX Correlation Matrix ]       |  [ Volatility Percentile eCDF Curve ]    |
|  How closely FX volatility maps  |  Where current volatility sits in the    |
|  to CBCI drops (R-squared).      |  historical distribution.                |
+----------------------------------+------------------------------------------+
```

---

## Page 6: Central Bank Comparison (The Head-to-Head)
*Goal: Deep-dive fundamental comparison for analysts writing institutional reports.*

```text
+-----------------------------------------------------------------------------+
|  Compare: [ Federal Reserve ▼ ]   vs.   [ European Central Bank ▼ ]         |
+-----------------------------------------------------------------------------+
|                                                                             |
|                       [ RADAR / SPIDER CHART ]                              |
|                                                                             |
|                          Forecast Accuracy                                  |
|                                  |                                          |
|                                 / \                                         |
|         Policy Consistency     /---\      Inflation Anchoring               |
|                                \---/                                        |
|                                 \ /                                         |
|                                  |                                          |
|                 Bond Market             Currency Stability                  |
|                 Confidence                                                  |
|                                                                             |
|        --- FED (Blue polygon)          --- ECB (Teal polygon)               |
|                                                                             |
+-----------------------------------------------------------------------------+
|  FED Weakness: Bond Confidence     |  ECB Weakness: Policy Consistency      |
|  FED Strength: Currency Stability  |  ECB Strength: Forecast Accuracy       |
+-----------------------------------------------------------------------------+
```
