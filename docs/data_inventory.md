# Central Bank Credibility Index (CBCI) - Data Inventory

This inventory outlines the official macroeconomic and market data sources required to build the CBCI, prioritizing institutional APIs (IMF, BIS, OECD, World Bank, FRED, and specific central banks).

| Provider | Dataset | API Availability | Download URL / API Endpoint | Frequency | Coverage (Countries) | Key Variables to Extract |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FRED (St. Louis Fed)** | Federal Reserve Economic Data | Yes (REST API) | [FRED API](https://fred.stlouisfed.org/docs/api/fred/) | Daily, Monthly | US (Primary), Global | US CPI (`CPIAUCSL`), Fed Funds Rate (`FEDFUNDS`), 2Y/10Y Treasuries (`DGS2`, `DGS10`) |
| **BIS** | BIS Statistics (Policy Rates, CPI, FX) | Yes (SDMX API) | [BIS SDMX API](https://data.bis.org/api) | Daily, Monthly | Global (All 10 targets) | Central Bank Policy Rates, CPI (Monthly), Effective Exchange Rates |
| **IMF** | International Financial Statistics (IFS) | Yes (JSON REST API) | [IMF Data API](https://datahelp.imf.org/knowledgebase/articles/667681-using-json-restful-api) | Monthly | Global (All 10 targets) | Consumer Prices (Inflation), Government Bond Yields, Central Bank Discount Rates |
| **OECD** | Main Economic Indicators (MEI) | Yes (SDMX API) | [OECD API](https://data.oecd.org/api/sdmx-json-documentation/) | Monthly | OECD + Partners | Harmonized CPI, Short-term Interest Rates, Long-term Interest Rates |
| **World Bank** | World Development Indicators (WDI) | Yes (REST API) | [World Bank API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) | Annual, Monthly | Global | Macro Baseline: Annual Inflation, Real Interest Rates, GDP Growth |
| **ECB** | ECB Data Portal (formerly SDW) | Yes (SDMX API) | [ECB API Help](https://data.ecb.europa.eu/help/api/overview) | Daily, Monthly | Euro Area | HICP (Inflation), Main Refinancing Rate, Euro Area Sovereign Yield Curve |
| **Bank of England** | Interactive Statistical Database (IADB) | Yes (REST API) | [BOE IADB](https://www.bankofengland.co.uk/statistics/research-datasets) | Daily, Monthly | UK | Official Bank Rate, UK CPI, UK Gilt Yields (2Y, 10Y) |
| **Bank of Japan** | BOJ Time-Series Data Portal | Yes (API / CSV) | [BOJ Data Portal](https://www.stat-search.boj.or.jp/index_en.html) | Daily, Monthly | Japan | Policy-Rate Balances, Japan CPI, JGB Yields |
| **Reserve Bank of India** | Database on Indian Economy (DBIE) | Limited (Scraping/Excel) | [RBI DBIE](https://dbie.rbi.org.in/) | Daily, Monthly | India | Policy Repo Rate, CPI (Combined), 10Y G-Sec Yield |
| **People's Bank of China** | PBOC Statistics | None (Scraping req.) | [PBOC Stats](http://www.pbc.gov.cn/en/3688006/index.html) | Monthly | China | Loan Prime Rate (LPR), China CPI |
| **Various Central Banks** | Monetary Policy Statements & Minutes | None (Scraping req.) | Respective CB websites (e.g., FOMC Calendar) | 6-8 times / year | All 10 Targets | Unstructured Text Data for NLP Sentiment Analysis (Hawkish vs Dovish) |

> [!TIP]
> **Engineering Strategy:** While the IMF, BIS, and OECD offer broad coverage, fetching specific daily yield volatility and high-frequency policy rates often requires a combination of **FRED** (for US data), **BIS** (for global rate alignment), and **Yahoo Finance (`yfinance`)** as a fallback for high-frequency daily sovereign bond yields (to calculate the "Market Trust" volatility metric). Unstructured text will require custom scraping modules per central bank.
