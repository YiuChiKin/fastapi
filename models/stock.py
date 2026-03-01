# models/stock.py
# Represents the database table structure.
# In a real project this would use SQLAlchemy or another ORM.
# Kept as a plain dataclass here for demonstration purposes.

from dataclasses import dataclass, field


@dataclass
class CandleBar:
    timestamp: int   # Unix timestamp (seconds)
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class StockCandle:
    ticker: str
    resolution: str
    bars: list[CandleBar] = field(default_factory=list)


@dataclass
class Stock:
    ticker: str          # e.g. "AAPL"
    company_name: str    # e.g. "Apple Inc."
    exchange: str        # e.g. "NASDAQ"
    sector: str          # e.g. "Technology"
    price: float         # latest price in USD
    change_pct: float    # daily change percentage
