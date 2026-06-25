# Central Bank Credibility Index (CBCI) - Implementation Plan

## Goal Description
To build a flagship macroeconomic and quantitative portfolio project that measures and ranks the credibility of 10 major central banks from 2010 to 2026. The project will evaluate how well central banks manage inflation expectations, align their forward guidance with actual policy moves, and maintain market trust and independence. 

> [!NOTE]
> **Perspective:** This plan is designed from the viewpoint of a macroeconomic research team (IMF, BIS) combined with a quantitative research approach (JPMorgan). It focuses on robustness, replicability, and institutional-grade analytics.

## User Review Required
Please review the complete architecture and methodology below. Specifically, evaluate if the weighting in the **Scoring Framework** aligns with your strategic vision for the index, and if the **Database Schema** covers all the dimensions you intend to explore.

## 1. Project Architecture
The architecture is designed to handle time-series macroeconomic data and unstructured text data (policy statements) for NLP analysis.

*   **Data Ingestion Layer:** Python-based ETL pipelines connecting to official APIs (FRED, ECB SDW, BIS) and scraping central bank press releases.
*   **Data Storage Layer:** A relational database (PostgreSQL or SQLite for local portability) to store structured macro data, text metadata, and computed scores.
*   **Quantitative Engine:** Python (`pandas`, `numpy`, `statsmodels`) for computing moving averages, volatility, and inflation deviation.
*   **NLP Engine:** `transformers` (Hugging Face) or `nltk`/`spaCy` to run sentiment analysis (Hawkish vs. Dovish) on FOMC/ECB/BOE meeting statements.
*   **Presentation Layer:** Power BI for the executive dashboard and interactive visualizations.

## 2. Research Methodology
"Credibility" is notoriously difficult to quantify. We define Central Bank Credibility as a composite index of four pillars:

1.  **Inflation Anchoring (Targeting Discipline):** How closely has the central bank kept inflation (CPI/PCE) to its stated target (typically 2%)? We measure the absolute deviation from the target over a rolling 12-month window.
2.  **Forward Guidance Consistency (The Surprise Factor):** Do they do what they say? We use NLP to assign a Hawkish/Dovish score to policy statements. We then correlate this score with the actual interest rate move at the *following* meeting. High correlation = high consistency (no shocks).
3.  **Market Trust (Yield Volatility):** If a central bank is credible, its policy decisions should smoothly price into the market. We measure the volatility of 2-year and 10-year sovereign bond yields in the 3 days surrounding a policy rate decision. Lower volatility = higher market trust.
4.  **Institutional Independence:** A static or slowly moving score based on established academic indices (e.g., Cukierman-Webb-Neyapti) or credit rating proxies (Sovereign CDS spreads) indicating freedom from political interference.

## 3. Official Data Sources
*   **Macroeconomic Data (Inflation, GDP, Unemployment):** 
    *   Federal Reserve Economic Data (FRED) API
    *   ECB Statistical Data Warehouse (SDW)
    *   BIS Statistics API
    *   World Bank Open Data API
*   **Policy Rates & Communications:**
    *   Official Central Bank Websites (Scraped for press releases and minutes)
    *   BIS Central Bank Hub
*   **Market Data (Bond Yields, FX Rates):**
    *   Yahoo Finance API (`yfinance`) or Alpha Vantage
    *   Investing.com (via scraping or unofficial API for niche sovereign bonds)

## 4. Scoring Framework
The CBCI will be scored on a 0-100 scale, calculated monthly.

*   **Inflation Anchoring (40% Weight):** 
    *   Score = `100 - ( |Actual Inflation - Target Inflation| * Penalty Multiplier )`
    *   Capped between 0 and 100.
*   **Forward Guidance Consistency (30% Weight):** 
    *   NLP Sentiment Score ranges from -1 (Dovish) to +1 (Hawkish).
    *   If Sentiment matches Rate Move direction, Score = 100. If it contradicts (e.g., Dovish statement followed by a hike), Score = 0. We use a 6-month rolling average.
*   **Market Trust (20% Weight):** 
    *   Inversely proportional to the standard deviation of 2Y bond yields around meeting dates. Normalized across the 10 countries.
*   **Independence (10% Weight):** 
    *   Qualitative overlay mapped to a 0-100 scale based on institutional mandates.

## 5. Database Schema
A normalized relational schema to house the research data.

*   **`Dim_CentralBank`**: `CB_ID` (PK), `Bank_Name`, `Country`, `Target_Inflation`, `Governor`
*   **`Fact_MacroIndicators`**: `Date`, `CB_ID` (FK), `Indicator_Type` (e.g., CPI, Policy Rate), `Value`
*   **`Fact_MarketData`**: `Date`, `CB_ID` (FK), `Instrument` (e.g., 2Y_Yield, FX_Pair), `Close_Price`, `Volatility`
*   **`Fact_Communications`**: `Comm_ID` (PK), `Date`, `CB_ID` (FK), `Doc_Type` (Minutes, Statement), `Raw_Text`, `NLP_Hawkish_Score`
*   **`Fact_CBCI_Scores`**: `Date`, `CB_ID` (FK), `Inflation_Score`, `Guidance_Score`, `Market_Score`, `Independence_Score`, `Total_CBCI_Score`

## 6. Power BI Dashboard Architecture
A high-end, dark-themed, institutional-grade BI architecture.

*   **Page 1: Global Credibility Overview (The Executive Summary)**
    *   World map highlighting the 10 target regions. Tooltips show current CBCI score.
    *   Line chart showing the "Global Credibility Average" over time (2010-2026).
    *   Leaderboard matrix (Rank 1 to 10).
*   **Page 2: The Inflation Gap (Macro View)**
    *   Small multiples (grid of 10 line charts) showing Actual Inflation vs. Target Inflation for each bank.
    *   Highlighting periods of extreme deviation (e.g., 2022-2023 inflation shock).
*   **Page 3: The 'Surprise' Index (NLP & Forward Guidance)**
    *   Scatter plot: NLP Sentiment Score (X-axis) vs. Actual Rate Move (Y-axis).
    *   Quadrants showing "Predictable" vs. "Shock" zones.
*   **Page 4: Deep Dive Profiles**
    *   Slicer to select a specific Central Bank.
    *   Radar chart breaking down their score across the 4 pillars.

## 7. GitHub Repository Structure
Organized for a professional data science workflow within the newly created folder structure:

```text
Central-Bank-Credibility-Index/
│
├── data/
│   ├── raw/                 # Unprocessed API pulls and text dumps
│   ├── processed/           # Cleaned datasets ready for scoring
│   └── output/              # Final scoring tables for Power BI
│
├── docs/
│   ├── methodology.md       # Detailed math behind the scoring framework
│   └── data_dictionary.md   # DB schema definitions
│
├── src/
│   ├── ingestion/           # Scripts to hit FRED, ECB, BIS APIs
│   ├── nlp/                 # HuggingFace sentiment analysis scripts
│   ├── scoring/             # Logic to calculate the CBCI index
│   └── utils/               # Database connection strings, helpers
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_nlp_model_testing.ipynb
│   └── 03_scoring_framework_validation.ipynb
│
├── dashboard/
│   ├── CBCI_Dashboard_v1.pbix # Power BI file
│   └── theme.json             # High-end dark theme JSON for Power BI
│
├── reports/
│   └── CBCI_Annual_Report.pdf # Placeholder for generated PDF reports
│
├── requirements.txt         # Python dependencies
└── README.md                # Project overview and run instructions
```

## 8. LinkedIn Carousel Plan
A high-engagement, 7-slide carousel designed to attract recruiters, economists, and quant researchers.

*   **Slide 1 (Hook):** "Who really controls the economy? We tracked the credibility of the world's top 10 Central Banks from 2010-2026. The results might shock you. 🌍📉"
*   **Slide 2 (The Problem):** "In 2022, inflation targets were shattered globally. Forward guidance failed. How do we quantify 'trust' in monetary policy? Enter the Central Bank Credibility Index (CBCI)."
*   **Slide 3 (The Methodology):** "We built a quant model based on 4 pillars: 1. Inflation Anchoring 🎯 2. Forward Guidance Consistency (NLP) 🗣️ 3. Market Trust (Yield Volatility) 📊 4. Independence 🏛️"
*   **Slide 4 (The Tech Stack):** "Built for scale. Python for data ingestion (FRED, BIS). HuggingFace NLP for parsing thousands of FOMC/ECB statements. PostgreSQL for storage. Power BI for visualization."
*   **Slide 5 (The Data - Sneak Peek):** (Show a high-quality screenshot of the 'Surprise Index' scatter plot or the Inflation Gap small multiples).
*   **Slide 6 (The Rankings):** "The Most Credible Bank in 2026? [Insert Winner]. The Biggest Fall from Grace? [Insert Loser]. The data doesn't lie."
*   **Slide 7 (Call to Action):** "Want to explore the data yourself? Check out the interactive Power BI dashboard and the full open-source Python architecture on my GitHub. Link in the comments! 👇"

---
## Verification Plan
*   **Review:** User reviews this architecture to ensure it meets the standard of a high-end portfolio project.
*   **Next Steps:** Upon approval, we will begin creating the foundational scripts, SQL schema, and dummy data generation to kick off the execution phase.
