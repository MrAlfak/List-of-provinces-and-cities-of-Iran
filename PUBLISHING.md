# Publishing guide

Releases must publish a **validated source-backed dataset**, not simply whatever happens to be checked into the repository.

## Required pre-release checks

```bash
python -m pip install -r requirements.txt
python scripts/validate_data.py
python scripts/audit_data.py --strict
python -m pytest tests/
python scripts/generate_all.py
```

For the current 1402 baseline, CI additionally verifies:

- 31 provinces
- 1,450 canonical city records
- complete, globally unique `official_code` values
- provenance status `source-backed`
- MySQL/PostgreSQL generation and SQL escaping regression
- Docker build and `/health` smoke test

## Data provenance

Before a release that changes canonical membership, verify and record:

- publisher / official source page;
- snapshot date/year;
- pinned revision when a mirror is used;
- source SHA-256;
- importer/rebuild command;
- exclusion/delta audit trail;
- strict membership audit result;
- source/data license.

The current pinned baseline is documented in `data/provenance.json` and `DATA_LICENSE.md`.

## Rebuilding 1402

The 1402 rebuild is explicit. Use the **Tests** workflow with `rebuild_1402=true` or run `scripts/rebuild_from_amar_1402.py` against the exact pinned source revision. Do not change the pinned source or expected counts silently.

## Derived release artifacts

The canonical JSON is `iran_cities.json`. Derived outputs include:

- `iran_cities.min.json`
- `iran_cities.csv`
- `iran_cities.geojson` — geocoded subset only
- `iran_cities.mysql.sql`
- `iran_cities.postgresql.sql`

GeoJSON must not fabricate points for cities without coordinate enrichment.

## Licensing notices

- Repository-authored software/code: MIT (`LICENSE`).
- Current source-backed 1402 dataset and its data derivatives: GPL-3.0 (`DATA_LICENSE.md`, `LICENSE-DATA-GPL-3.0`).

Any npm or other data-bearing package must include the relevant data-license notice and attribution.

## npm

The npm path remains supported only when validation, strict membership audit, tests and artifact generation pass before publishing.

## PyPI

PyPI publishing remains disabled. Re-enable only after the repository contains a self-contained Python package/wheel that bundles the intended data files, includes all license notices, and passes a clean-install import/data-access test in CI.

## Versioning

A newer administrative snapshot or membership-changing sourced delta should be treated as a meaningful data release. Document additions/removals/renames/moves and preserve compatibility IDs only when the identity mapping is unambiguous.
