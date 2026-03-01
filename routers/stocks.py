# routers/stocks.py
# HTTP layer — defines URL paths and HTTP methods for the /stocks endpoints.
# Business logic is delegated to services/stock.py.

from fastapi import APIRouter, Query
from schemas.stock import StockCandleResponse, StockResponse
from services.stock import fetch_all_stocks, fetch_stock, fetch_stock_history

router = APIRouter()


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
    return fetch_all_stocks()


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
    return fetch_stock(ticker.upper())


# ---------------------------------------------------------------------------
# GET /stocks/{ticker}/history
# ---------------------------------------------------------------------------
@router.get(
    "/{ticker}/history",
    response_model=StockCandleResponse,
    summary="Get historical OHLCV candles for a stock",
    description=(
        "Returns OHLCV candlestick bars for the requested ticker.\n\n"
        "**resolution** – candle width: `1`, `5`, `15`, `30`, `60` (minutes), `D` (day), `W` (week), `M` (month).\n\n"
        "**days** – how many calendar days of history to fetch (1–365, default 30)."
    ),
)
def get_stock_history(
    ticker: str,
    resolution: str = Query(default="D", description="Candle resolution: 1 5 15 30 60 D W M"),
    days: int       = Query(default=30,  ge=1, le=365, description="Calendar days of history to return"),
):
    return fetch_stock_history(ticker.upper(), resolution=resolution, days=days)
