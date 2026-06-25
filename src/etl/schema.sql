-- Central Bank Credibility Index (CBCI) PostgreSQL Schema

CREATE TABLE IF NOT EXISTS dim_central_bank (
    cb_id VARCHAR(10) PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    target_inflation NUMERIC(4,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_macro_indicators (
    id SERIAL PRIMARY KEY,
    cb_id VARCHAR(10) REFERENCES dim_central_bank(cb_id),
    date DATE NOT NULL,
    indicator_type VARCHAR(50) NOT NULL,
    value NUMERIC(10,4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (cb_id, date, indicator_type)
);

CREATE TABLE IF NOT EXISTS fact_market_data (
    id SERIAL PRIMARY KEY,
    cb_id VARCHAR(10) REFERENCES dim_central_bank(cb_id),
    date DATE NOT NULL,
    instrument VARCHAR(50) NOT NULL,
    close_price NUMERIC(10,4),
    volatility NUMERIC(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (cb_id, date, instrument)
);

CREATE TABLE IF NOT EXISTS fact_communications (
    comm_id SERIAL PRIMARY KEY,
    cb_id VARCHAR(10) REFERENCES dim_central_bank(cb_id),
    date DATE NOT NULL,
    doc_type VARCHAR(50),
    raw_text TEXT,
    nlp_hawkish_score NUMERIC(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (cb_id, date, doc_type)
);

CREATE TABLE IF NOT EXISTS fact_cbci_scores (
    id SERIAL PRIMARY KEY,
    cb_id VARCHAR(10) REFERENCES dim_central_bank(cb_id),
    date DATE NOT NULL,
    inflation_score NUMERIC(5,2),
    guidance_score NUMERIC(5,2),
    market_score NUMERIC(5,2),
    independence_score NUMERIC(5,2),
    total_cbci_score NUMERIC(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (cb_id, date)
);
