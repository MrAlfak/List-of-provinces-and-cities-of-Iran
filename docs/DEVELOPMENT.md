# Development guide

## Development principle

Canonical city membership is a data-provenance problem first. Do not infer city identity from coordinates, spelling similarity, map search results, or legacy IDs.

The current canonical baseline is the pinned SCI 1402 snapshot described in `data/provenance.json`: 31 provinces and 1,450 independent cities after source-relative urban-subarea filtering.

## Local checks

```bash
python -m pip install -r requirements.txt
python -m compileall -q api_server.py scripts tests
python scripts/validate_data.py
python scripts/audit_data.py --strict
python -m pytest tests/
python scripts/generate_all.py
```

`audit_data.py --strict` gates membership/provenance. Use `--strict-enrichment` only for workflows that require complete optional enrichment.

## Data changes

For changes to membership or hierarchy:

1. provide an official or clearly traceable source and effective snapshot/date;
2. record checksum and licensing;
3. diff by source hierarchy/identifiers;
4. never delete a record solely because coordinates or names resemble another record;
5. preserve a legacy numeric ID only for an unambiguous identity match;
6. update `official_code` / `uid`, provenance and audit trail;
7. run strict membership audit and regenerate all derivatives.

## Pinned 1402 rebuild

The 1402 rebuild is intentionally manual. Run the GitHub **Tests** workflow with `rebuild_1402=true`, or execute `scripts/rebuild_from_amar_1402.py` against the exact pinned source recorded in `data/provenance.json`.

The importer enforces three expected source invariants: 1,659 raw CODEREC=5 rows, 209 excluded municipal subareas, and 1,450 canonical cities. A mismatch is a review event, not something to auto-fix.

## Optional enrichment

Coordinates and English names may be null. GeoJSON therefore contains only geocoded records. Enrichment sources should be tracked independently from administrative membership.

## API / Docker

Run locally:

```bash
python api_server.py
```

Run containerized:

```bash
docker compose up --build
```

The Docker image runs Gunicorn as a non-root user. CI builds the image and smoke-tests `/health`.

## Tests

Tests cover source-backed identifiers, global ID uniqueness, county-scoped city names, Persian normalization, SQL escaping, optional coordinates, subarea classification, artifact generation, and API container health.

## Licensing

Repository-authored code is MIT. The current 1402 source-backed dataset and data derivatives are GPL-3.0; preserve `DATA_LICENSE.md` and `LICENSE-DATA-GPL-3.0` in data-bearing distributions.
