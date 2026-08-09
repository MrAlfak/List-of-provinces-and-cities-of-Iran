# 🇮🇷 Iran Provinces & Cities Data

[![Tests](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml/badge.svg)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[فارسی](README.fa.md) | English

A developer-friendly Iran location dataset with JSON, CSV, GeoJSON, SQL generators, a small read-only API, validation tools, and an explicit provenance workflow.

> [!WARNING]
> **Data status:** the checked-in `iran_cities.json` is a **legacy, not-yet-authoritative** compatibility dataset. Earlier versions incorrectly described every record as an official city. The legacy data contains known semantic debt (for example administrative areas/border facilities mixed with cities and weak automatic transliterations). Do not use it as a legal or authoritative registry until it is rebuilt from an identified administrative-division snapshot and passes the strict audit.

## What changed in v2.1

- Removed the circular pipeline that downloaded this repository's own JSON as its upstream source.
- Replaced the dangerous hand-written duplicate deletion list with conservative exact-duplicate detection.
- Added a source-backed rebuild pipeline based on administrative division type (`divisionType=5` for cities).
- Preserves existing numeric IDs where possible and adds stable `uid` / `official_code` fields for source-backed data.
- Added structural validation plus a separate semantic/enrichment audit.
- Hardened the API: `/api/v1`, pagination, Persian normalization, opt-in CORS, health/meta endpoints, no default debug mode.
- Split SQL generation into real MySQL and PostgreSQL dialects with correct string escaping.
- Docker now runs Gunicorn as a non-root user and has a working healthcheck.
- CI now validates, tests, audits, regenerates outputs, and smoke-tests the Docker image.

## Files

```text
iran_cities.json               # Legacy compatibility dataset / canonical output after an approved rebuild
iran_cities.min.json           # Derived minified JSON
iran_cities.csv                # Derived CSV
iran_cities.geojson            # Derived GeoJSON
api_server.py                   # Read-only API
scripts/rebuild_from_divisions.py
scripts/validate_data.py
scripts/audit_data.py
scripts/generate_all.py
data/provenance.json            # Provenance policy and current status
```

SQL files are generated on demand:

```bash
python scripts/generate_sql.py --dialect both
# iran_cities.mysql.sql
# iran_cities.postgresql.sql
```

## Quick start

```bash
git clone https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran.git
cd List-of-provinces-and-cities-of-Iran
python -m pip install -r requirements.txt
python scripts/validate_data.py
python -m pytest tests/
python scripts/audit_data.py
```

The normal audit is report-only for the legacy snapshot. A newly rebuilt source-backed dataset should pass strict mode:

```bash
python scripts/audit_data.py --input iran_cities.rebuilt.json --strict
```

## Rebuild from administrative divisions

The canonical question **"is this record a city?"** must come from an identified country-divisions source, not from coordinates or name similarity.

The importer accepts normalized UTF-8 CSV with:

```text
id,parentCountryDivisionId,name,code,divisionType
```

where `divisionType=5` means city.

```bash
python scripts/rebuild_from_divisions.py \
  --divisions-csv /path/to/divisions.csv \
  --legacy-json iran_cities.json \
  --output iran_cities.rebuilt.json

python scripts/validate_data.py --input iran_cities.rebuilt.json
python scripts/audit_data.py --input iran_cities.rebuilt.json --strict
```

See [`data/README.md`](data/README.md) and [`data/provenance.json`](data/provenance.json). A reproducible historical baseline is the Statistical Center of Iran 1398 division spreadsheet; prefer a newer official snapshot when available.

## API

Local development:

```bash
python api_server.py
```

Production-style container:

```bash
docker compose up --build
```

Main endpoints:

```text
GET /health
GET /api/v1/meta
GET /api/v1/provinces
GET /api/v1/provinces/<id>
GET /api/v1/cities?page=1&per_page=100&province_id=<id>&q=<query>
GET /api/v1/cities/<id>
GET /api/v1/search?q=<query>
```

Legacy `/api/...` aliases remain available for backward compatibility. CORS is disabled unless `CORS_ORIGINS` is explicitly configured.

## Direct JavaScript usage

```javascript
import iranCities from './iran_cities.json' with { type: 'json' };

const tehran = iranCities.find((province) => province.province === 'تهران');
console.log(tehran);
```

## Data model

Source-backed records can include stable source identifiers and hierarchy fields in addition to legacy compatibility fields:

```json
{
  "id": 1,
  "uid": "ir:province:<source-code>",
  "official_code": "<source-code>",
  "province": "...",
  "cities": [
    {
      "id": 1,
      "uid": "ir:city:<source-code>",
      "official_code": "<source-code>",
      "name": "...",
      "county": "...",
      "district": "...",
      "latitude": null,
      "longitude": null
    }
  ]
}
```

Coordinates and English names are enrichment fields and may be `null` until independently verified.

## Contributing data corrections

A data correction should include the source and snapshot/date that supports the change. Please do not submit "duplicate fixes" based only on shared coordinates, similar spelling, or aliases. The data-correction issue template is the preferred starting point.

## Publishing

The npm package is validated and regenerated before release. PyPI publishing is intentionally disabled until a self-contained Python wheel is implemented and installation is covered by CI.

## License

Project code and repository-authored material are MIT licensed; see [LICENSE](LICENSE). Upstream datasets may have their own provenance/licensing requirements, which must be recorded before import.

**Version:** 2.1.0
