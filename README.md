# 🇮🇷 Iran Provinces & Cities Data

[![Tests](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml/badge.svg)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml)
[![Code License](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE)
[![Data License](https://img.shields.io/badge/data-GPL--3.0-blue.svg)](DATA_LICENSE.md)

[فارسی](README.fa.md) | English

A developer-friendly Iran city dataset with source-backed administrative membership, JSON/CSV/GeoJSON/SQL outputs, a read-only API, validation, provenance, and a reproducible rebuild pipeline.

> [!IMPORTANT]
> **Canonical data status:** `iran_cities.json` is source-backed to the **Statistical Center of Iran (SCI) 1402 administrative-division snapshot** mirrored at a pinned upstream revision. The raw source contains 1,659 `CODEREC=5` rows; 209 source-relative municipal subareas are excluded only when their base city exists in the same province and county, leaving **1,450 independent city records across 31 provinces**. This is an **as-of-1402 snapshot**, not a claim that no later administrative changes have occurred.

## Integrity status

The checked-in canonical dataset currently passes the strict membership audit:

- 31 provinces
- 1,450 canonical city records
- 0 records without `official_code`
- 0 duplicate `official_code` values
- 0 membership/provenance blockers
- provenance status: `source-backed`
- source SHA-256 and pinned mirror revision recorded in [`data/provenance.json`](data/provenance.json)

Optional enrichment is intentionally tracked separately. **703 records currently lack coordinate and English-name enrichment**, 319 retained English names are flagged as weak/automatic transliterations, and one duplicate coordinate group remains for review. None of those fields are used to determine city membership.

## Source and reproducibility

Canonical membership is rebuilt by [`scripts/rebuild_from_amar_1402.py`](scripts/rebuild_from_amar_1402.py) from the pinned 1402 SCI snapshot:

```text
Publisher: Statistical Center of Iran (مرکز آمار ایران)
Official source page identified upstream: https://amar.org.ir/geo
Mirror: sajaddp/list-of-cities-in-Iran
Pinned mirror commit: 474942269f75ec247e1af5684f5e3eca9f304431
Pinned source path: offical/list.json
Snapshot: 1402
```

The exact source checksum, counts, and refresh policy live in [`data/provenance.json`](data/provenance.json). The 209 excluded urban-subarea rows are retained as an audit trail in [`data/excluded-urban-subareas-1402.json`](data/excluded-urban-subareas-1402.json).

A rebuild is explicit rather than automatic on every push. Run the **Tests** workflow manually with `rebuild_1402=true`, or execute the importer locally against the pinned source file. Its hard invariants stop the rebuild if the expected 1,659 raw rows, 209 excluded subareas, or 1,450 canonical cities unexpectedly change.

## What changed in v2.1

- Replaced the circular self-download pipeline with a pinned, source-backed administrative snapshot.
- Replaced the hand-written duplicate deletion list with conservative source-relative classification.
- Preserved legacy numeric IDs only when an unambiguous match exists; source-backed `uid` / `official_code` identifiers are canonical.
- Added county/district hierarchy to city records.
- Separated structural validation, source-membership audit, and optional enrichment audit.
- Hardened the API: `/api/v1`, pagination, Persian normalization, opt-in CORS, health/meta endpoints, no default debug mode.
- Split SQL generation into real MySQL and PostgreSQL dialects with correct escaping.
- Made GeoJSON a geocoded subset instead of fabricating coordinates for un-enriched records.
- Docker runs Gunicorn as a non-root user and includes a working healthcheck.
- CI validates the 31/1,450 source-backed invariants, tests, regenerates outputs, and smoke-tests Docker.

## Files

```text
iran_cities.json                         # Canonical source-backed 1402 dataset (1,450 cities)
iran_cities.min.json                     # Minified canonical JSON
iran_cities.csv                          # CSV derivative
iran_cities.geojson                      # Geocoded subset only
iran_cities.mysql.sql                    # MySQL derivative
iran_cities.postgresql.sql               # PostgreSQL derivative
api_server.py                            # Read-only API
scripts/rebuild_from_amar_1402.py        # Pinned SCI 1402 importer
scripts/rebuild_from_divisions.py        # Generic normalized division importer
scripts/validate_data.py                 # Structural validation
scripts/audit_data.py                    # Membership/enrichment audit
scripts/generate_all.py                  # Derived artifact generation
data/provenance.json                     # Source, checksum, counts, policy
data/audit-report.json                   # Checked-in audit report
data/excluded-urban-subareas-1402.json   # 209 excluded source subareas
DATA_LICENSE.md                          # Data licensing/attribution
```

## Quick start

```bash
git clone https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran.git
cd List-of-provinces-and-cities-of-Iran
python -m pip install -r requirements.txt
python scripts/validate_data.py
python scripts/audit_data.py --strict
python -m pytest tests/
```

Regenerate derived files:

```bash
python scripts/generate_all.py
```

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

Legacy `/api/...` aliases remain for backward compatibility. CORS is disabled unless `CORS_ORIGINS` is explicitly configured.

## Direct JavaScript usage

```javascript
import iranCities from './iran_cities.json' with { type: 'json' };

const tehran = iranCities.find((province) => province.province === 'تهران');
console.log(tehran.cities.length);
```

## Data model

```json
{
  "id": 1,
  "uid": "ir:province:1402:<province-code>",
  "official_code": "1402:<province-code>",
  "province": "...",
  "cities": [
    {
      "id": 1,
      "uid": "ir:city:1402:<province>:<county>:<district>:<city>",
      "official_code": "1402:<province>:<county>:<district>:<city>",
      "name": "...",
      "county": "...",
      "county_code": "...",
      "district": "...",
      "district_code": "...",
      "latitude": null,
      "longitude": null,
      "english_name": null
    }
  ]
}
```

`official_code` and the source hierarchy identify membership. Coordinates and English names are optional enrichment and may be `null`.

## GeoJSON note

`iran_cities.geojson` contains only cities with valid coordinate enrichment. Its metadata reports the canonical total, geocoded feature count, and number skipped without coordinates. Use `iran_cities.json` when you need the complete 1,450-city membership list.

## Contributing data corrections

Every membership or hierarchy correction should include a source and snapshot/date. Do not delete a record only because coordinates match, spellings look similar, or names are aliases. Newer administrative decisions should be incorporated through a newer identified snapshot or an explicitly reviewed, sourced delta.

## Publishing

The npm package is validated and regenerated before release. PyPI publishing remains disabled until a self-contained Python wheel is implemented and clean-install tested in CI.

## License

- **Repository-authored code:** MIT — see [`LICENSE`](LICENSE).
- **1402 source-backed dataset and data derivatives:** GPL-3.0 — see [`DATA_LICENSE.md`](DATA_LICENSE.md) and [`LICENSE-DATA-GPL-3.0`](LICENSE-DATA-GPL-3.0).

**Version:** 2.1.0
