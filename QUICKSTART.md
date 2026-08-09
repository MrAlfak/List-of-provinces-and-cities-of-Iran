# Quick Start | شروع سریع

## 1. Install

```bash
git clone https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran.git
cd List-of-provinces-and-cities-of-Iran
python -m pip install -r requirements.txt
```

## 2. Check the dataset

```bash
python scripts/validate_data.py
python scripts/audit_data.py
python -m pytest tests/
```

`validate_data.py` checks structural integrity. `audit_data.py` reports semantic/enrichment debt. The checked-in legacy dataset is intentionally **not** advertised as an authoritative registry until rebuilt from a documented administrative source.

## 3. Generate derived files

```bash
python scripts/generate_all.py
```

This creates/refreshes:

```text
iran_cities.min.json
iran_cities.csv
iran_cities.geojson
iran_cities.mysql.sql
iran_cities.postgresql.sql
```

## 4. Run the API

Development:

```bash
python api_server.py
```

Then open:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/api/v1/meta
http://127.0.0.1:8000/api/v1/provinces
http://127.0.0.1:8000/api/v1/cities?page=1&per_page=100
```

Production-style local container:

```bash
docker compose up --build
```

## 5. Rebuild city membership from country divisions

When you have a normalized source snapshot:

```bash
python scripts/rebuild_from_divisions.py \
  --divisions-csv /path/to/divisions.csv \
  --legacy-json iran_cities.json \
  --output iran_cities.rebuilt.json

python scripts/validate_data.py --input iran_cities.rebuilt.json
python scripts/audit_data.py --input iran_cities.rebuilt.json --strict
```

Do not overwrite `iran_cities.json` with a new snapshot until provenance and the strict audit are complete. See `data/README.md`.
