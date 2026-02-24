# routers/stocks.py
# HTTP layer — defines URL paths and HTTP methods for the /stocks endpoints.
# Real data is fetched from the Finnhub API (https://finnhub.io).

import os

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from models.stock import Stock
from schemas.stock import StockResponse

load_dotenv()

router = APIRouter()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

# ---------------------------------------------------------------------------
# Tickers tracked by the list endpoint — extend as needed
# ---------------------------------------------------------------------------
TRACKED_TICKERS = ["AAPL", "MSFT", "JPM", "XOM", "AMZN"]


# ---------------------------------------------------------------------------
# Helper — fetch a single stock from Finnhub (quote + company profile)
# ---------------------------------------------------------------------------
def _fetch_stock(ticker: str) -> Stock:
    """Call Finnhub quote and profile2 endpoints and return a Stock instance."""
    if not FINNHUB_API_KEY or FINNHUB_API_KEY == "your_api_key_here":
        raise HTTPException(
            status_code=503,
            detail="FINNHUB_API_KEY is not configured. Add it to your .env file.",
        )

    params = {"symbol": ticker, "token": FINNHUB_API_KEY}

    try:
        with httpx.Client(timeout=10.0) as client:
            quote_resp = client.get(f"{FINNHUB_BASE_URL}/quote", params=params)
            profile_resp = client.get(f"{FINNHUB_BASE_URL}/stock/profile2", params=params)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Finnhub request failed: {exc}") from exc

    if quote_resp.status_code != 200 or profile_resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Finnhub returned an unexpected status code.")

    quote = quote_resp.json()
    profile = profile_resp.json()

    # Finnhub returns an empty dict / zero price for unknown tickers
    if not profile or quote.get("c", 0) == 0:
        raise HTTPException(status_code=404, detail=f"Stock '{ticker}' not found.")

    return Stock(
        ticker=ticker,
        company_name=profile.get("name", ticker),
        exchange=profile.get("exchange", "N/A"),
        sector=profile.get("finnhubIndustry", "N/A"),
        price=round(quote.get("c", 0.0), 2),      # current price
        change_pct=round(quote.get("dp", 0.0), 2), # daily % change
    )


# ---------------------------------------------------------------------------
# GET /stocks/
# ---------------------------------------------------------------------------
@router.get(
    "/",
    response_model=list[StockResponse],
    summary="List tracked stocks",
    description="Returns live quotes for a predefined list of American stocks via Finnhub.",
)
def get_all_stocks():
    return [_fetch_stock(t) for t in TRACKED_TICKERS]


# ---------------------------------------------------------------------------
# GET /stocks/{ticker}
# ---------------------------------------------------------------------------
@router.get(
    "/{ticker}",
    response_model=StockResponse,
    summary="Get a stock by ticker symbol",
    description="Returns the live quote of any stock identified by its ticker symbol (case-insensitive) via Finnhub.",
)
def get_stock_by_ticker(ticker: str):
    return _fetch_stock(ticker.upper())
