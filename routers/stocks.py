# routers/stocks.py
# HTTP layer — defines URL paths and HTTP methods for the /stocks endpoints.
# Business logic is delegated to services/stock.py.

from fastapi import APIRouter
from schemas.stock import StockResponse
from services.stock import fetch_all_stocks, fetch_stock

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
