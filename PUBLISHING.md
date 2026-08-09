# Publishing | راهنمای انتشار

## Release gate

Do not publish a release merely because the code tests pass. Data and code have separate freshness/quality requirements.

Before an npm/GitHub release:

```bash
python -m pip install -r requirements.txt
python scripts/validate_data.py
python -m pytest tests/
python scripts/audit_data.py
python scripts/generate_all.py
npm pack --dry-run
```

If the release claims **official/current city coverage**, also require:

```bash
python scripts/audit_data.py --strict
```

and verify that `data/provenance.json` records the source publisher, snapshot date/year, checksum, source URL/archive identifier, import command and validation result.

## npm

The npm package is the supported package-registry distribution for v2.1.

1. Update `package.json` and `CHANGELOG.md` together.
2. Run the release gate above.
3. Create a GitHub Release.
4. `.github/workflows/publish.yml` validates again and runs `npm publish` using `NPM_TOKEN`.

`npm publish` runs `prepack`, which regenerates:

```text
iran_cities.min.json
iran_cities.csv
iran_cities.geojson
iran_cities.mysql.sql
iran_cities.postgresql.sql
```

The SQL artifacts are generated at package time so a stale checked-in SQL dump cannot drift from the JSON source.

## PyPI

**PyPI publishing is disabled in v2.1.** The previous configuration could build metadata without guaranteeing that the installed wheel contained a usable dataset. Re-enable PyPI only after:

- a real importable Python package owns the data files;
- wheel/sdist contents are explicitly controlled;
- installation into a clean virtual environment is tested in CI;
- an import/use smoke test passes from the installed wheel, not from the repository checkout.

## Versioning

Use semantic versioning for code/schema behavior. Dataset snapshot dates are separate metadata and must not be inferred from the package version or code release date.

- PATCH: compatible code/data-quality fixes that do not change public schema semantics.
- MINOR: backward-compatible fields/endpoints/tooling.
- MAJOR: incompatible schema/API behavior.

A change in the official administrative snapshot should always be documented in provenance and release notes even if the package semver change is only minor/patch.
