# schemas/stock.py
# Pydantic schemas that define what data enters and leaves the API.
# Decoupled from the DB model so we control exactly what is exposed.

from pydantic import BaseModel, Field


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
