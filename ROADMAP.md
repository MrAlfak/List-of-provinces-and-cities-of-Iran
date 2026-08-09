# Roadmap | نقشه راه

The project now prioritizes **source integrity and reproducibility before new features**.

## P0 — Source-backed canonical dataset

- [x] Stop using generated repository data as its own upstream source.
- [x] Define provenance requirements in `data/provenance.json`.
- [x] Add an importer for normalized administrative divisions.
- [x] Make `divisionType=5` the canonical city-membership rule.
- [x] Preserve legacy numeric IDs where possible and introduce stable source-backed identifiers.
- [x] Remove unsafe manual duplicate deletion logic.
- [ ] Obtain and archive/checksum the newest usable official administrative-division snapshot.
- [ ] Rebuild `iran_cities.json` from that snapshot.
- [ ] Manually resolve unmatched/renamed cities and verify province capitals.
- [ ] Run `audit_data.py --strict` with zero unresolved semantic items before labeling the dataset authoritative.

## P1 — Enrichment quality

- [ ] Replace weak automatic English transliterations with reviewed names/aliases and document the transliteration standard.
- [ ] Re-verify coordinates independently from canonical city membership.
- [ ] Add coordinate provenance and confidence/source fields.
- [ ] Add population only with census year/source metadata.
- [ ] Add postal information only where licensing/source and geographic meaning are clear.

## P1 — API and distribution

- [x] Version API under `/api/v1` while keeping compatibility aliases.
- [x] Add pagination, normalized Persian search, filtering, health/meta endpoints, and opt-in CORS.
- [x] Split MySQL/PostgreSQL generation and fix SQL escaping.
- [x] Run production container with Gunicorn and non-root user.
- [ ] Add OpenAPI schema and contract tests.
- [ ] Add ETag/conditional requests for large list responses.
- [ ] Publish immutable data snapshots as GitHub Release assets.

## P2 — Packaging

- [x] Keep npm publishing behind validation/tests/generation.
- [x] Disable the broken PyPI publishing path.
- [ ] Build a real self-contained Python package containing the dataset and API helpers.
- [ ] Test wheel installation in a clean environment before re-enabling PyPI.

## P2 — Administrative hierarchy

Once the canonical source is refreshed:

- [ ] Publish counties, districts and rural districts as first-class entities instead of mixing their names into city data.
- [ ] Add stable parent relationships and source codes.
- [ ] Publish migration notes when official divisions change.
- [ ] Add optional province/county polygon datasets only with appropriate source/licensing metadata.

## Release gate

A release that claims current/official city coverage must satisfy all of the following:

1. An identified source snapshot and checksum are recorded.
2. Canonical membership is rebuilt from the source hierarchy.
3. Structural validation passes.
4. Strict semantic audit passes.
5. Derived formats are regenerated from exactly that canonical JSON.
6. API and Docker smoke tests pass.
7. Documentation states the actual snapshot date rather than the code release date.
