# Data licensing and attribution

The **software/code** in this repository remains licensed under the MIT License in [`LICENSE`](LICENSE).

The source-backed **1402 administrative-division dataset and data derivatives** are built from the Statistical Center of Iran country-division snapshot redistributed by [`sajaddp/list-of-cities-in-Iran`](https://github.com/sajaddp/list-of-cities-in-Iran) under **GNU GPL v3.0**.

## Source snapshot

- Publisher represented by the upstream snapshot: Statistical Center of Iran (مرکز آمار ایران)
- Official source page identified by the upstream project: `https://amar.org.ir/geo`
- Mirror repository: `sajaddp/list-of-cities-in-Iran`
- Pinned mirror commit: `474942269f75ec247e1af5684f5e3eca9f304431`
- Pinned source path: `offical/list.json`
- Snapshot year: 1402 (2023/2024 administrative snapshot)

The complete GPL v3 license text used for redistributed data is stored in `LICENSE-DATA-GPL-3.0` and is copied from the pinned upstream revision during the reproducible rebuild.

## Files treated as data / data derivatives

This notice applies to the canonical dataset and generated data artifacts, including:

- `iran_cities.json`
- `iran_cities.min.json`
- `iran_cities.csv`
- `iran_cities.geojson`
- generated MySQL/PostgreSQL data exports
- `data/excluded-urban-subareas-1402.json`

Code, tests, API implementation, build scripts, and documentation authored in this repository remain MIT unless a file contains a more specific notice.

## Important provenance distinction

City **membership** comes from the pinned 1402 administrative snapshot and the documented urban-subarea exclusion rule. Legacy coordinates and English names are retained only as optional enrichment where an unambiguous city match exists. Those enrichment values are not used to decide whether a record is a city.

The canonical dataset is source-backed **as of 1402**, not a claim that no later administrative changes occurred. Newer Cabinet/Interior Ministry changes require a later source snapshot or an explicitly reviewed delta before inclusion.
