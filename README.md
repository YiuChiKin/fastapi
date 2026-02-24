# FastAPI Project Setup Instructions

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Run the FastAPI server

```bash
uvicorn main:app --reload
or
python -m uvicorn main:app --reload
```

- Open your browser and go to: http://127.0.0.1:8000
- Interactive API docs: http://127.0.0.1:8000/docs

---

## Project Structure

```
fastapi/
├── main.py             # App entry point, registers all routers
├── routers/            # HTTP layer — URL paths and HTTP methods only
│   ├── __init__.py
│   └── stocks.py
├── models/             # Database layer — ORM table definitions
│   ├── __init__.py
│   └── stock.py
├── schemas/            # API layer — Pydantic validation & serialization
│   ├── __init__.py
│   └── stock.py
├── requirements.txt
└── README.md
```

### Why Separate Routers, Models, and Schemas?

| Layer | Responsibility |
|-------|---------------|
| **Router** | Handles HTTP concerns (paths, methods, status codes). Keeps endpoints thin. |
| **Model** | Represents the database table/document via an ORM (e.g. SQLAlchemy). |
| **Schema** | Defines what data enters and leaves the API via Pydantic. Enables validation and controls what fields are exposed. |

**Key benefits:**
- **Security** — schemas prevent leaking sensitive DB fields (e.g. `hashed_password`)
- **Flexibility** — one DB model can have multiple API shapes (`StockCreate` vs `StockResponse`)
- **Maintainability** — DB changes don't break the API contract
- **Single Responsibility** — each layer does exactly one thing

---

## Available Endpoints

### Stocks

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/stocks/` | List all American stocks |
| `GET` | `/stocks/{ticker}` | Get a single stock by ticker symbol |
