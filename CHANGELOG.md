# Changelog | تاریخچه تغییرات

Notable changes are documented here. Dates describe repository releases/changes, not the freshness date of the underlying administrative dataset.

## [2.1.0] - 2026-08-09

### Data integrity
- Marked the checked-in JSON as a legacy, non-authoritative compatibility dataset until it is rebuilt from an identified administrative-division snapshot.
- Added `data/provenance.json` and a documented evidence policy for new snapshots.
- Added `scripts/rebuild_from_divisions.py`; official city membership is derived from `divisionType=5`, while legacy coordinates/names are enrichment only.
- Preserved existing numeric IDs where possible and introduced source-backed `uid` / `official_code` fields.
- Replaced the hand-maintained duplicate deletion list with conservative exact-record duplicate detection.
- Removed the circular "download this repository's own JSON as upstream" behavior.
- Added semantic/enrichment auditing and stronger structural validation, including global city-ID uniqueness.

### API / runtime
- Added `/api/v1` endpoints while keeping legacy aliases.
- Added pagination, province filtering, normalized Persian search, `/health`, and `/api/v1/meta`.
- CORS is now opt-in and Flask debug mode is disabled by default.
- Dataset loading now fails loudly on missing/invalid files.
- Docker now uses Gunicorn, a non-root user, and a working healthcheck.

### Generated formats
- Replaced the misleading shared MySQL/PostgreSQL SQL file with separate dialect generators.
- Fixed SQL literal escaping (including apostrophes in names).
- Removed the stale checked-in `iran_cities.sql`; release/package generation produces `iran_cities.mysql.sql` and `iran_cities.postgresql.sql`.

### CI / publishing
- CI now runs structural validation, regression tests, semantic audit, derived-format generation, SQL escaping regression checks, Docker build, and API smoke test.
- Updated GitHub Actions versions.
- npm publishing now validates and regenerates artifacts first.
- Disabled PyPI publishing because the old metadata did not produce a self-contained installable data wheel.

### Documentation
- Removed claims that the legacy snapshot is a complete/official/fully precise registry.
- Updated README files, TypeScript types, source policy, and release guidance.

## [2.0.0] - historical

Version 2.0 introduced the expanded JSON dataset, coordinates, English-name enrichment, CSV/GeoJSON/SQL generators, Flask API, Docker files, tests, and documentation.

> Historical note: v2.0 documentation described 883 records as "all official cities" and called the dataset production-ready. The v2.1 audit found that those claims were not supported by a traceable authoritative source and that the legacy records include semantic classification issues. Those claims are superseded by v2.1.

## [1.0.0] - historical

Initial province/city data and telephone-code dataset.
