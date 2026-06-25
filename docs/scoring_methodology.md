# Central Bank Credibility Index (CBCI): A Methodological Framework

**Prepared by:** Quantitative Macroeconomic Research Group  
**Classification:** Working Paper / Methodology Note  

## Abstract
This paper outlines the mathematical and theoretical framework for the Central Bank Credibility Index (CBCI). The index quantifies the nebulous concept of "institutional credibility" into a rigorous, empirical score ranging from $0$ to $100$. The CBCI is a composite of five sub-indices: Inflation Forecast Accuracy, Inflation Anchoring, Currency Stability, Bond Market Confidence, and Policy Consistency. 

---

## 1. Inflation Forecast Accuracy
**Weight:** 20%

**Academic Justification:** 
Credibility relies heavily on the public and financial markets' belief that the central bank correctly assesses the macroeconomic environment (Blinder, 2000). A central bank that consistently fails to forecast its own primary mandate target suffers severe reputational damage.

**Formula:** 
Mean Absolute Error (MAE) of the Central Bank’s 12-month-ahead inflation forecast vs. realized inflation.
$$E_{i,t} = | \pi_{i, t+12}^{forecast} - \pi_{i, t+12}^{realized} |$$

**Normalization Approach:** 
To map errors to a 0-100 scale, we apply a Min-Max scaling cross-sectionally across the 10 target central banks at time $t$. Lower forecast error yields a higher score.
$$Score = 100 \times \left(1 - \frac{E_{i,t} - E_{min,t}}{E_{max,t} - E_{min,t}}\right)$$

**Potential Weaknesses:** 
Global, exogenous structural shocks (e.g., pandemic supply chain collapses, geopolitical energy crises) cause simultaneous forecast failures. The normalization approach mitigates this by scoring *relative* error, but cannot eliminate the penalty for unforecastable black swan events.

---

## 2. Inflation Anchoring
**Weight:** 30% (Primary Mandate)

**Academic Justification:** 
The primary objective of modern monetary policy is price stability (Svensson, 1999). Significant, persistent deviations from the stated inflation target erode the "anchor" of long-term inflation expectations, leading to wage-price spirals.

**Formula:** 
Absolute deviation of current headline inflation from the official target.
$$D_{i,t} = | \pi_{i,t} - \pi_{i,target} |$$

**Normalization Approach:** 
We apply a linear decay function with a strict cutoff threshold $K$ (e.g., 400 basis points or 4%). 
$$Score = 100 \times \max\left(0, 1 - \frac{D_{i,t}}{K}\right)$$
*If inflation strays more than 4% from the target, the anchoring score drops to 0.*

**Potential Weaknesses:** 
This formulation does not differentiate between supply-side shocks (which central banks cannot easily control) and demand-side policy failures. It assumes all deviation is a cost to credibility.

---

## 3. Currency Stability
**Weight:** 15%

**Academic Justification:** 
Extreme currency volatility signals a loss of international confidence in the purchasing power of the fiat currency and the competence of the underlying monetary authority (Reinhart & Rogoff, 2004). 

**Formula:** 
Annualized realized volatility of the Real Effective Exchange Rate (REER) over a rolling 90-day window.
$$V_{FX, t} = \sqrt{252} \times \sigma(\Delta \ln(REER_{t-90:t}))$$

**Normalization Approach:** 
Empirical Cumulative Distribution Function (eCDF). We rank the current volatility against the historical distribution (2010–Present) of REER volatility for all G10 currencies.
$$Score = 100 \times (1 - P(V \le V_{FX, t}))$$

**Potential Weaknesses:** 
Not all central banks explicitly target exchange rates (e.g., the Federal Reserve). A currency might fluctuate wildly due to global safe-haven flows or external trade dynamics rather than a lack of monetary credibility.

---

## 4. Bond Market Confidence
**Weight:** 15%

**Academic Justification:** 
Long-term sovereign yields reflect the market's expectation of future monetary policy and inflation premiums (Gürkaynak, Sack, & Swanson, 2005). High volatility in the long end of the curve suggests market confusion or lack of trust in the central bank's long-term guidance.

**Formula:** 
Realized volatility of 10-year sovereign bond yields over a rolling 30-day window. 
$$V_{B, t} = \sigma(\Delta y_{10yr, t-30:t})$$

**Normalization Approach:** 
Cross-sectional Min-Max scaling, similar to the forecast error approach. Lower volatility equals a higher confidence score.

**Potential Weaknesses:** 
Sovereign bond yields are heavily influenced by *fiscal* policy and government debt levels. A central bank could be unfairly penalized for a profligate treasury department driving up risk premiums.

---

## 5. Policy Consistency
**Weight:** 20%

**Academic Justification:** 
"Forward guidance" is a critical policy tool at the zero-lower bound and beyond (Woodford, 2012). If a central bank signals a dovish stance but hikes rates shortly after, it destroys the efficacy of future guidance and creates market shocks.

**Formula:** 
An NLP-derived alignment score between the textual sentiment of the central bank's communication at time $t$ and the actual policy rate decision at time $t+1$. 
Let $S_t \in \{-1, 0, 1\}$ be the NLP signal (Dovish, Neutral, Hawkish). Let $R_{t+1}$ be the rate move (Cut, Hold, Hike).
$$C_{t} = \begin{cases} 
1 & \text{if } S_t \text{ and } R_{t+1} \text{ match direction} \\
0.5 & \text{if one is neutral} \\
0 & \text{if they contradict (e.g., Dovish then Hike)}
\end{cases}$$
The final score is a 12-month rolling average of $C_t$.

**Normalization Approach:** 
The rolling average naturally falls between $0$ and $1$. Multiply by $100$.

**Potential Weaknesses:** 
Rapid policy pivots are sometimes necessary due to fast-changing incoming data. Rigid consistency might punish a central bank for correctly reacting to new information, effectively rewarding stubbornness over adaptability.

---
## Final Index Calculation
The composite CBCI score at month $t$ for Central Bank $i$ is the weighted sum of the five sub-indices:

$$CBCI_{i,t} = (0.20 \times Forecast) + (0.30 \times Anchor) + (0.15 \times Currency) + (0.15 \times Bond) + (0.20 \times Consistency)$$
