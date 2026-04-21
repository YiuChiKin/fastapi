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
| `GET` | `/stocks/{ticker}/history` | Get OHLCV candlestick history for a ticker |

---

## Docker

### Build the image

```bash
docker build -t stock-api:latest .
```

### Run the container

```bash
docker run -p 8000:8000 -e FINNHUB_API_KEY=your_key_here stock-api:latest
```

- Replace `your_key_here` with your actual [Finnhub API key](https://finnhub.io).
- Open your browser and go to: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs

### Push to a registry

```bash
docker tag stock-api:latest your-dockerhub-username/stock-api:latest
docker push your-dockerhub-username/stock-api:latest
```

---

## Helm (Kubernetes)

Helm deploys the app to any Kubernetes cluster. Helm CLI is required (`scoop install helm` on Windows).

### Chart structure

```
helm/
├── Chart.yaml           # Chart metadata (name, version)
├── values.yaml          # Default configuration values
└── templates/
    ├── _helpers.tpl     # Shared name/label helpers
    ├── secret.yaml      # Kubernetes Secret for FINNHUB_API_KEY
    ├── deployment.yaml  # Deployment with liveness & readiness probes
    ├── service.yaml     # ClusterIP Service (port 80 → 8000)
    ├── ingress.yaml     # Optional Ingress (disabled by default)
    └── hpa.yaml         # Optional HorizontalPodAutoscaler (disabled by default)
```

### Lint the chart

```bash
helm lint ./helm --set secret.finnhubApiKey=test
```

### Render templates locally (no cluster needed)

```bash
helm template stock-api ./helm --set secret.finnhubApiKey=test
```

### Install to a cluster

```bash
helm install stock-api ./helm --set secret.finnhubApiKey=your_key_here
```

### Upgrade after changes

```bash
helm upgrade stock-api ./helm --set secret.finnhubApiKey=your_key_here
```

### Uninstall

```bash
helm uninstall stock-api
```

### Key values (`values.yaml`)

| Key | Default | Description |
|-----|---------|-------------|
| `image.repository` | `your-dockerhub-username/stock-api` | Docker image to deploy |
| `image.tag` | `latest` | Image tag |
| `replicaCount` | `1` | Number of pod replicas |
| `secret.finnhubApiKey` | `""` | Finnhub API key (always set at install time) |
| `service.type` | `ClusterIP` | Kubernetes Service type |
| `ingress.enabled` | `false` | Enable Ingress |
| `autoscaling.enabled` | `false` | Enable HorizontalPodAutoscaler |

### Access the app after install

```bash
# Port-forward the service to localhost
kubectl port-forward svc/stock-api 8080:80
```

Then open: http://localhost:8080

$env:Path += ";C:\terraform"
$env:PATH += ";C:\Program Files\Docker\Docker\resources\bin"
docker build -t localhost/stock-api:latest .
cd terraform
terraform apply