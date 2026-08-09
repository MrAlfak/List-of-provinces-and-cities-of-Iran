# 🇮🇷 Iran Provinces & Cities Dataset — JSON, CSV, GeoJSON, SQL & REST API

<div align="center">

**A source-backed dataset of 31 Iranian provinces and 1,450 cities for web apps, mobile apps, forms, checkout flows, CRMs, logistics, GIS and data projects.**

[![GitHub stars](https://img.shields.io/github/stars/MrAlfak/List-of-provinces-and-cities-of-Iran?style=for-the-badge&logo=github&label=Stars)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/MrAlfak/List-of-provinces-and-cities-of-Iran?style=for-the-badge&logo=github&label=Forks)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/network/members)
[![Tests](https://img.shields.io/github/actions/workflow/status/MrAlfak/List-of-provinces-and-cities-of-Iran/tests.yml?branch=main&style=for-the-badge&label=CI)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml)
[![Last commit](https://img.shields.io/github/last-commit/MrAlfak/List-of-provinces-and-cities-of-Iran?style=for-the-badge)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/commits/main)

**[فارسی](README.fa.md)** · **[Quick Start](QUICKSTART.md)** · **[API](docs/API.md)** · **[Use Cases](docs/USE_CASES.md)** · **[Contributing](CONTRIBUTING.md)**

⭐ **If this dataset saves you time, star the repository so you can find it again and help more developers discover it.**

</div>

---

## What you get

| Feature | Included |
|---|---|
| Provinces | **31** |
| Canonical cities | **1,450** |
| Administrative snapshot | **SCI 1402** |
| JSON | ✅ |
| Minified JSON | ✅ |
| CSV | ✅ |
| GeoJSON | ✅ geocoded subset |
| MySQL | ✅ |
| PostgreSQL | ✅ |
| REST API | ✅ |
| Persian/Farsi search normalization | ✅ |
| Stable source identifiers | ✅ `uid` + `official_code` |
| County & district hierarchy | ✅ |
| Automated validation / CI | ✅ |

This repository is designed for developers searching for **Iran cities JSON**, **Iran provinces and cities**, **Iran location data**, **Iran GeoJSON**, **Iran cities SQL**, **Persian/Farsi city data**, or an **Iran provinces and cities API**.

## Why this repository

Many Iran city lists are useful as simple static files, but this project focuses on **traceability and developer usability**:

- **Source-backed membership** instead of treating coordinates or spelling similarity as proof that a record is a city.
- **1,450 canonical city records** across all 31 provinces in the pinned SCI 1402 snapshot.
- **Multiple formats** for frontend, backend, database and GIS workflows.
- **Stable source identity** with `uid` and `official_code`.
- **County and district hierarchy** for richer address flows.
- **Versioned REST API** with pagination and normalized Persian search.
- **Reproducible importer, validator and audit pipeline** instead of opaque manual edits.
- **Docker-ready API** and automated CI checks.

## Use it in 30 seconds

### JavaScript / TypeScript

```js
const url = 'https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json';

const provinces = await fetch(url).then((response) => response.json());
const tehran = provinces.find((province) => province.province === 'تهران');

console.log(tehran.cities);
```

### Python

```python
import json
from urllib.request import urlopen

url = "https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json"
with urlopen(url) as response:
    provinces = json.load(response)

tehran = next(p for p in provinces if p["province"] == "تهران")
print([city["name"] for city in tehran["cities"]])
```

### REST API

```bash
python api_server.py
curl "http://127.0.0.1:8000/api/v1/cities?q=تهران"
```

### Database

```text
iran_cities.mysql.sql
iran_cities.postgresql.sql
```

See [`docs/USE_CASES.md`](docs/USE_CASES.md) for examples covering address selectors, ecommerce checkout, CRM, logistics, GIS and backend integrations.

## Popular use cases

- Province → city dropdowns in **React, Next.js, Vue, Angular and mobile apps**
- Iranian address forms and user-profile onboarding
- Ecommerce checkout and shipping forms
- CRM / ERP customer-address normalization
- Delivery, logistics and dispatch systems
- GIS and mapping projects using GeoJSON
- Laravel, Django, Flask, Node.js and other backend projects
- Search/autocomplete for Persian city names
- Analytics and location-based reporting
- Database seeding for MySQL and PostgreSQL

## Data files

```text
iran_cities.json                         # complete canonical 1402 dataset
iran_cities.min.json                     # minified JSON
iran_cities.csv                          # CSV derivative
iran_cities.geojson                      # geocoded subset
iran_cities.mysql.sql                    # MySQL derivative
iran_cities.postgresql.sql               # PostgreSQL derivative
```

### Example record

```json
{
  "id": 1,
  "uid": "ir:city:1402:...",
  "official_code": "1402:...",
  "name": "...",
  "english_name": null,
  "county": "...",
  "county_code": "...",
  "district": "...",
  "district_code": "...",
  "latitude": null,
  "longitude": null,
  "is_capital": false
}
```

Prefer `official_code` / `uid` for source-backed identity. Numeric `id` is retained mainly for legacy compatibility.

## Data integrity & provenance

> [!IMPORTANT]
> `iran_cities.json` is source-backed to the **Statistical Center of Iran (SCI) 1402 administrative-division snapshot** mirrored at a pinned upstream revision. It represents an **as-of-1402** baseline and does not claim that every administrative decision after 1402 is already included.

The pinned source contains **1,659** raw `CODEREC=5` rows. The importer excludes **209** source-relative municipal subareas only when the corresponding base city exists in the same province and county, leaving **1,450 independent canonical cities**.

Current strict membership audit:

- 31 provinces
- 1,450 canonical cities
- 0 missing `official_code`
- 0 duplicate `official_code`
- 0 membership/provenance blockers
- provenance status: `source-backed`

Exact source revision and SHA-256 are recorded in [`data/provenance.json`](data/provenance.json), and excluded source rows remain auditable in [`data/excluded-urban-subareas-1402.json`](data/excluded-urban-subareas-1402.json).

### Enrichment status

Coordinates and English names are enrichment—not proof of city identity. Some enrichment remains intentionally incomplete instead of being fabricated:

- 703 records without coordinate enrichment
- 703 records without English-name enrichment
- 319 legacy English transliterations flagged for review
- 1 duplicate-coordinate group flagged for review

`iran_cities.geojson` therefore contains only records with valid coordinates. Use `iran_cities.json` for the complete city membership list.

## Local development

```bash
git clone https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran.git
cd List-of-provinces-and-cities-of-Iran
python -m pip install -r requirements.txt
python scripts/validate_data.py
python scripts/audit_data.py --strict
python -m pytest tests/
python scripts/generate_all.py
```

Run the API:

```bash
python api_server.py
# or
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

## Contributing

Found a newer administrative change, typo, hierarchy problem, coordinate issue or better English name? Contributions are welcome.

- Membership/hierarchy changes should include a source and effective snapshot/date.
- Enrichment changes should cite the enrichment source independently.
- Records are not deleted merely because coordinates match or names look similar.

Start with [`CONTRIBUTING.md`](CONTRIBUTING.md) or open one of the repository issue templates.

## Help the project grow

If you use this project in an app, website, thesis, dashboard, logistics system or open-source project:

1. ⭐ **Star the repository** to keep it in your GitHub library.
2. 🍴 **Fork it** if you are building a useful extension.
3. 🐛 Open an issue when you find a data problem.
4. 🔗 Link back to the repository from projects that use the dataset.
5. 🤝 Submit sourced corrections or integrations that can help other developers.

## Search keywords

`iran cities json` · `iran provinces json` · `iran provinces and cities` · `iran city list` · `iranian cities` · `persian cities` · `farsi cities` · `iran geojson` · `iran sql database` · `iran mysql cities` · `iran postgresql cities` · `iran location data` · `iran administrative divisions` · `iran address form` · `iran city api` · `iran provinces api`

## License

- **Repository-authored code:** MIT — [`LICENSE`](LICENSE)
- **SCI 1402 source-backed dataset and derivatives:** GPL-3.0 — [`DATA_LICENSE.md`](DATA_LICENSE.md), [`LICENSE-DATA-GPL-3.0`](LICENSE-DATA-GPL-3.0)

**Version:** 2.1.0
