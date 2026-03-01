# services/stock.py
# Business logic layer — handles all Finnhub API calls and data assembly.
# Routers delegate to these functions and stay thin.

import os
from datetime import datetime, timedelta

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from models.stock import CandleBar, Stock, StockCandle

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

# ---------------------------------------------------------------------------
# Tickers tracked by the list endpoint — extend as needed
# ---------------------------------------------------------------------------
TRACKED_TICKERS = ["AAPL", "MSFT", "JPM", "XOM", "AMZN"]


# ---------------------------------------------------------------------------
# fetch_stock — used by GET /stocks/{ticker}
# ---------------------------------------------------------------------------
def fetch_stock(ticker: str) -> Stock:
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
        price=round(quote.get("c", 0.0), 2),       # current price
        change_pct=round(quote.get("dp", 0.0), 2),  # daily % change
    )


# ---------------------------------------------------------------------------
# fetch_all_stocks — used by GET /stocks/
# ---------------------------------------------------------------------------
def fetch_all_stocks() -> list[Stock]:
    """Return live quotes for all tracked tickers."""
    return [fetch_stock(ticker) for ticker in TRACKED_TICKERS]


# ---------------------------------------------------------------------------
# fetch_stock_history — used by GET /stocks/{ticker}/history
# ---------------------------------------------------------------------------
_VALID_RESOLUTIONS = {"1", "5", "15", "30", "60", "D", "W", "M"}


def fetch_stock_history(
    ticker: str,
    resolution: str = "D",
    days: int = 30,
) -> StockCandle:
    """Fetch OHLCV candles from Finnhub /stock/candle.

    Args:
        ticker:     Ticker symbol, e.g. "AAPL".
        resolution: Candle resolution – one of 1, 5, 15, 30, 60, D, W, M.
        days:       How many calendar days of history to return (max 365).
    """
    if not FINNHUB_API_KEY or FINNHUB_API_KEY == "your_api_key_here":
        raise HTTPException(
            status_code=503,
            detail="FINNHUB_API_KEY is not configured. Add it to your .env file.",
        )

    if resolution not in _VALID_RESOLUTIONS:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid resolution '{resolution}'. Choose from: {sorted(_VALID_RESOLUTIONS)}",
        )

    days = max(1, min(days, 365))
    now = datetime.utcnow()
    to_ts   = int(now.timestamp())
    from_ts = int((now - timedelta(days=days)).timestamp())

    params = {
        "symbol":     ticker,
        "resolution": resolution,
        "from":       from_ts,
        "to":         to_ts,
        "token":      FINNHUB_API_KEY,
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(f"{FINNHUB_BASE_URL}/stock/candle", params=params)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Finnhub request failed: {exc}") from exc

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Finnhub returned an unexpected status code.")

    data = resp.json()

    if data.get("s") == "no_data":
        raise HTTPException(
            status_code=404,
            detail=f"No historical data found for '{ticker}' with the given parameters.",
        )

    bars = [
        CandleBar(
            timestamp=t,
            open=round(o, 4),
            high=round(h, 4),
            low=round(l, 4),
            close=round(c, 4),
            volume=v,
        )
        for t, o, h, l, c, v in zip(
            data["t"], data["o"], data["h"], data["l"], data["c"], data["v"]
        )
    ]

    return StockCandle(ticker=ticker, resolution=resolution, bars=bars)
