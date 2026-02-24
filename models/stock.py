# models/stock.py
# Represents the database table structure.
# In a real project this would use SQLAlchemy or another ORM.
# Kept as a plain dataclass here for demonstration purposes.

from dataclasses import dataclass


@dataclass
class Stock:
    ticker: str          # e.g. "AAPL"
    company_name: str    # e.g. "Apple Inc."
    exchange: str        # e.g. "NASDAQ"
    sector: str          # e.g. "Technology"
    price: float         # latest price in USD
    change_pct: float    # daily change percentage
