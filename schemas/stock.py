# schemas/stock.py
# Pydantic schemas that define what data enters and leaves the API.
# Decoupled from the DB model so we control exactly what is exposed.

from pydantic import BaseModel, Field


class CandleBar(BaseModel):
    """A single OHLCV bar returned by the history endpoint."""
    timestamp: int   = Field(..., description="Unix timestamp (seconds UTC)", example=1700000000)
    open:      float = Field(..., example=180.10)
    high:      float = Field(..., example=182.50)
    low:       float = Field(..., example=179.80)
    close:     float = Field(..., example=181.30)
    volume:    float = Field(..., example=52_000_000)

    class Config:
        from_attributes = True


class StockCandleResponse(BaseModel):
    """Schema returned by GET /stocks/{ticker}/history."""
    ticker:     str           = Field(..., example="AAPL")
    resolution: str           = Field(..., example="D")
    bars:       list[CandleBar]

    class Config:
        from_attributes = True


class StockResponse(BaseModel):
    """Schema returned by the API for a single stock."""
    ticker: str = Field(..., example="AAPL")
    company_name: str = Field(..., example="Apple Inc.")
    exchange: str = Field(..., example="NASDAQ")
    sector: str = Field(..., example="Technology")
    price: float = Field(..., example=189.50)
    change_pct: float = Field(..., example=1.23)

    class Config:
        from_attributes = True
