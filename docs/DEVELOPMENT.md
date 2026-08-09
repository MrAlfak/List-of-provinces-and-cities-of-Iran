# Development Guide

## Setup

```bash
python -m pip install -r requirements.txt
```

Useful commands:

```bash
make validate
make audit
make test
make generate
make docker-test
```

## Repository rule: canonical vs enrichment

Keep these concerns separate:

- **Canonical administrative membership**: whether a record is a province/county/district/city. This must come from a documented administrative-division snapshot.
- **Enrichment**: coordinates, English aliases, population, postal information, etc. Enrichment may be absent and must never be used to infer that a record is officially a city.

Do not add a manual list that deletes records merely because names or coordinates look similar.

## Data changes

For a source-backed refresh:

1. Record source/snapshot/checksum in `data/provenance.json`.
2. Keep the raw source outside generated output paths.
3. Rebuild with `scripts/rebuild_from_divisions.py`.
4. Run structural validation.
5. Run strict audit.
6. Review unmatched/renamed records manually against the source.
7. Replace the canonical JSON only after the previous steps pass.
8. Regenerate all derived formats.

```bash
python scripts/rebuild_from_divisions.py --divisions-csv source.csv --output iran_cities.rebuilt.json
python scripts/validate_data.py --input iran_cities.rebuilt.json
python scripts/audit_data.py --input iran_cities.rebuilt.json --strict
python scripts/generate_all.py
```

## Tests

Regression tests belong in `tests/`. Important invariants include:

- global numeric ID uniqueness;
- stable source-backed `uid` values;
- exactly one province capital;
- duplicate detection must not merge distinct names just because coordinates match;
- SQL escaping must remain safe for apostrophes;
- Persian search normalization must treat Arabic/Persian character variants consistently.

CI runs tests on Python 3.10 and 3.12, rebuilds derived artifacts, checks SQL escaping, builds Docker and smoke-tests `/health`.

## API development

The local command uses Flask's development server:

```bash
python api_server.py
```

Do not use that server for public production deployment. The Dockerfile uses Gunicorn. CORS is opt-in through `CORS_ORIGINS`.

API changes should preserve `/api/v1`; compatibility aliases under `/api/...` may be deprecated only with release notes and a migration path.

## Packaging

npm is the supported package-registry path in v2.1. PyPI is intentionally disabled until a self-contained Python wheel and clean-install CI test exist.

## Pull requests

Data PRs should say which source/snapshot supports each semantic correction. Code PRs should include regression coverage when fixing a failure mode.
