# Order Book + TWAP Demo

A small trading-infrastructure demo: a market data adapter streams a live order
book from a public exchange, a Django backend fans it out to the browser over
WebSockets, and a TWAP executor splits a hypothetical order into slices and
simulates fills against the live book.

> Work in progress. The full write-up (reconnects, throttling, decimal precision)
> comes at the end of the build.

## Architecture

```
Binance WS ──► market-adapter ──► Redis ──► backend (Django Channels) ──► browser
                                     ▲            │
                                     │            ▼ (REST: place TWAP order)
                              twap-executor ◄── RabbitMQ
                                     │
                                     ▼
                                 Postgres (orders, fills)
```

| Service | Tech | Role |
|---|---|---|
| `market-adapter` | Python asyncio | Exchange WebSocket, order book sync, publishing |
| `backend` | Django, DRF, Channels | REST API, WebSocket gateway, persistence |
| `twap-executor` | Python asyncio, aio-pika | Order slicing and fill simulation |
| `nginx` | nginx | Serves the React app, proxies `/api` and `/ws` |
| infra | Postgres, Redis, RabbitMQ | Storage, cache + pub/sub, message bus |

## Run it

Requires Docker.

```bash
docker compose up --build
```

Open http://localhost:8080.

## Develop locally

Requires [uv](https://docs.astral.sh/uv/) and Node 22.

```bash
uv sync --all-packages      # Python deps for every service
uv run pytest               # Python tests

cd frontend
npm install
npm run dev                 # http://localhost:5173, proxies /api and /ws to :8000
```

## Layout

```
packages/common/          shared Python code (config, Redis keys, heartbeats)
services/backend/         Django project
services/market_adapter/  exchange adapter worker
services/twap_executor/   TWAP worker
frontend/                 React + TypeScript (Vite)
docker/                   Dockerfiles
nginx/                    reverse proxy config
```
