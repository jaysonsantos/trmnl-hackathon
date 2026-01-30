# BVG Journey Planner (FastAPI)

Small FastAPI service that proxies the BVG Transport REST API (via `https://v6.bvg.transport.rest`) to retrieve public transport journey options.

## What it does

- Resolves human-readable addresses/stops into BVG stop IDs (`/locations`).
- Fetches journey options between two stops (`/journeys`).
- Returns raw JSON from the upstream API (ideal for feeding into a renderer/template).

This repository also includes a TRMNL-compatible template in `markup.html` for displaying up to three journey options on an e-ink screen.

## Requirements

- Python 3.14+

Dependencies are defined in `pyproject.toml`.

## Install

Use `uv`:

```bash
uv sync
```

## Run

Start the API locally:

```bash
python main.py
```

This launches Uvicorn on `http://0.0.0.0:8000`.

## API

### `GET /`

Returns the contents of `mock.json` (useful for local testing while iterating on templates).

### `GET /get-directions`

Query params:

- `from_address` (string)
- `to_address` (string)
- `arrival_time` (string) — currently accepted but not forwarded upstream

Example:

```bash
curl "http://localhost:8000/get-directions?from_address=Alexanderplatz&to_address=Hermannplatz&arrival_time=2026-01-30T18:10:00"
```

## Notes

- The service currently selects the first `/locations` result whose `type` is `stop`.
- `arrival_time` is not wired into the upstream request yet; if you want arrival/departure time filtering, we can extend `get_journey_info` to include the appropriate parameter.

## Authors

Created by Jayson Reis (@jaysonsantos), Artem Sierikov (@sierikov) and Darijan Ducic at the Zed + TRMNL Hackathon (Berlin, Jan 2026).
