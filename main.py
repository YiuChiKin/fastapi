from fastapi import FastAPI
from routers import stocks

app = FastAPI(title="Stock Market API", version="1.0.0")

app.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])


@app.get("/")
def read_root():
    return {"Hello": "World"}

