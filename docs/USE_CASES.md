# Iran Cities Dataset — Practical Use Cases

This page shows practical ways to use the **Iran provinces and cities dataset** in web, mobile, backend, ecommerce, logistics, CRM and GIS projects.

Canonical membership currently represents the source-backed SCI 1402 snapshot: **31 provinces / 1,450 cities**.

## 1. Province → city selector

Common for signup forms, profile forms, checkout pages and address books.

```js
const DATA_URL = 'https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json';

const provinces = await fetch(DATA_URL).then((response) => response.json());

const provinceOptions = provinces.map(({ id, province }) => ({
  value: id,
  label: province,
}));

function citiesForProvince(provinceId) {
  return provinces.find((item) => item.id === provinceId)?.cities ?? [];
}
```

Works well as a data source for React, Next.js, Vue, Angular, Svelte and native/mobile UI selectors.

## 2. Persian city autocomplete

Use the bundled API when you need normalized Persian search rather than loading the entire JSON in the browser.

```bash
python api_server.py
curl "http://127.0.0.1:8000/api/v1/cities?q=اصفهان"
```

The API normalizes common Persian/Arabic character variants and spacing differences before searching.

## 3. Ecommerce checkout

Typical flow:

```text
Country: Iran
  ↓
Province
  ↓
City
  ↓
Street / plaque / postal details
```

Store `official_code` or `uid` as the durable source-backed location identity and keep the displayed Persian name separately.

This is useful for:

- ecommerce checkout
- shipping-address forms
- customer profiles
- marketplace seller addresses
- invoice/billing addresses

## 4. CRM / ERP customer locations

Use the administrative hierarchy to standardize addresses:

```json
{
  "province": "...",
  "county": "...",
  "district": "...",
  "city": "...",
  "official_code": "1402:..."
}
```

This is more robust than saving a free-text city name only.

## 5. Logistics, delivery and dispatch

The dataset can act as the location reference layer for:

- delivery zones
- courier onboarding
- warehouse/customer routing metadata
- province/city reporting
- dispatch filters
- service-coverage forms

Coordinate enrichment is incomplete for some cities, so do not assume every canonical city currently has a GeoJSON point.

## 6. GIS and mapping

Use:

```text
iran_cities.geojson
```

for currently geocoded city records.

Use:

```text
iran_cities.json
```

when complete canonical membership is more important than coordinates.

## 7. MySQL seed data

```text
iran_cities.mysql.sql
```

Useful for Laravel, PHP, Node.js or other applications that need an initial Iranian province/city lookup database.

## 8. PostgreSQL seed data

```text
iran_cities.postgresql.sql
```

Useful for Django, FastAPI, Rails, Node.js and general PostgreSQL-backed systems.

## 9. Python data processing

```python
import json
from pathlib import Path

provinces = json.loads(Path("iran_cities.json").read_text(encoding="utf-8"))

cities = [
    {
        "province": province["province"],
        **city,
    }
    for province in provinces
    for city in province["cities"]
]

print(len(cities))  # 1450 in the pinned 1402 snapshot
```

## 10. Frontend static-data use

For lightweight apps, the repository can be consumed as static JSON without running the API:

```js
const url = 'https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.min.json';
const data = await fetch(url).then((response) => response.json());
```

For production systems, consider pinning a release/commit rather than always tracking `main` so a future data-version change is explicit in your deployment.

## 11. Search and analytics

Flatten the canonical data into rows and index fields such as:

- province
- county
- district
- city name
- official code
- source-backed UID

This works for internal dashboards, Elasticsearch/OpenSearch indexing, autocomplete and reporting pipelines.

## 12. Data correction workflow

If your application detects a mismatch with a newer administrative decision, open a sourced data-correction issue. Membership changes should include an official/traceable source and effective date rather than relying on map coordinates or spelling similarity.

## Related search terms

Iran cities JSON · Iran provinces JSON · Iran city list · Iran provinces and cities API · Iranian cities database · Persian city list · Farsi cities · Iran GeoJSON · Iran MySQL database · Iran PostgreSQL seed · Iran address form · Iran checkout city selector · Iran location data · Iran administrative divisions
