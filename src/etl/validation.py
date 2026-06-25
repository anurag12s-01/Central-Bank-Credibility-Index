from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional

class MacroIndicator(BaseModel):
    cb_id: str = Field(..., max_length=10)
    date: date
    indicator_type: str = Field(..., max_length=50)
    value: float

    @validator('cb_id')
    def valid_cb_id(cls, v):
        allowed_cbs = ['FED', 'ECB', 'BOE', 'BOJ', 'RBI', 'PBOC', 'SNB', 'BOC', 'RBA', 'BCB']
        if v not in allowed_cbs:
            raise ValueError(f"cb_id must be one of {allowed_cbs}")
        return v

class MarketData(BaseModel):
    cb_id: str = Field(..., max_length=10)
    date: date
    instrument: str = Field(..., max_length=50)
    close_price: Optional[float] = None
    volatility: Optional[float] = None
