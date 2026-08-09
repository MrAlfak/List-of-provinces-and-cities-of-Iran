# Quick start

The checked-in canonical dataset is the source-backed **SCI 1402** snapshot with **31 provinces and 1,450 independent cities**.

## Validate and test

```bash
python -m pip install -r requirements.txt
python scripts/validate_data.py
python scripts/audit_data.py --strict
python -m pytest tests/
```

`--strict` validates source membership/provenance. Missing coordinates or English names are optional enrichment and are reported separately.

## Generate all formats

```bash
python scripts/generate_all.py
```

Generated/maintained formats:

```text
iran_cities.json
iran_cities.min.json
iran_cities.csv
iran_cities.geojson
iran_cities.mysql.sql
iran_cities.postgresql.sql
```

`iran_cities.geojson` is only the geocoded subset; use `iran_cities.json` for the complete 1,450-city membership list.

## Run API

```bash
python api_server.py
```

or:

```bash
docker compose up --build
```

Health check:

```text
GET /health
```

Main API namespace:

```text
/api/v1
```

## Data identity

Prefer `official_code` / `uid` for source-backed identity. Numeric `id` values are retained for legacy compatibility where mapping was unambiguous.

## Rebuild the pinned 1402 snapshot

The rebuild is explicit and reproducible. In GitHub Actions, manually run the **Tests** workflow with `rebuild_1402=true`.

Locally, use `scripts/rebuild_from_amar_1402.py` with the exact source revision recorded in `data/provenance.json`. The importer will stop if the expected 1,659 raw rows, 209 excluded urban subareas or 1,450 canonical city count changes unexpectedly.

## Licensing

Code is MIT. The 1402 source-backed dataset and data derivatives are GPL-3.0; see `DATA_LICENSE.md`.

---

# شروع سریع فارسی

دیتاست اصلی فعلی snapshot منبع‌دار **۱۴۰۲** با **۳۱ استان و ۱٬۴۵۰ شهر مستقل** است.

```bash
python -m pip install -r requirements.txt
python scripts/validate_data.py
python scripts/audit_data.py --strict
python -m pytest tests/
python scripts/generate_all.py
```

برای فهرست کامل شهرها از `iran_cities.json` استفاده کنید. GeoJSON فقط رکوردهای دارای مختصات را شامل می‌شود. کد پروژه MIT و دیتاست/خروجی‌های داده‌ای ۱۴۰۲ تحت GPL-3.0 هستند.
