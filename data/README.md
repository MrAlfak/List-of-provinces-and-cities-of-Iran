# Data provenance and refresh policy

> **Important:** `iran_cities.json` is currently a legacy compatibility dataset. It must not be presented as an authoritative or complete registry of Iran's official cities until it is rebuilt from an identified administrative-division source snapshot and the resulting audit passes.

## What is canonical?

City membership and administrative hierarchy must come from a country-divisions source issued by, or traceable to, an official publisher. Coordinates, map-search results, postal data, aliases, and English transliterations are **enrichment only**; none of them prove that a record is legally a city.

The repository now supports the normalized division schema:

```text
id,parentCountryDivisionId,name,code,divisionType
```

with `divisionType=5` representing a city. `scripts/rebuild_from_divisions.py` walks the hierarchy to the province/county/district, preserves existing numeric IDs where possible, adds stable source-backed `uid`/`official_code` fields, and joins legacy coordinates only as enrichment.

## Rebuild workflow

```bash
python scripts/rebuild_from_divisions.py \
  --divisions-csv /path/to/official-or-normalized-divisions.csv \
  --legacy-json iran_cities.json \
  --output iran_cities.rebuilt.json

python scripts/validate_data.py --input iran_cities.rebuilt.json
python scripts/audit_data.py --input iran_cities.rebuilt.json --strict
```

Before replacing the published dataset, record the publisher, snapshot date/year, checksum, source URL/archive identifier, and import command in `data/provenance.json`.

## Supported reproducible baseline

A reproducible historical baseline is the Statistical Center of Iran (SCI) 1398 country-divisions spreadsheet (`GEO98.xlsx`). The MIT-licensed `Hameds/IranCountryDivisions` project documents a normalized representation of that SCI file and the division-type mapping used by the importer. This is a **baseline**, not a claim that 1398 data is current in 2026. Prefer a newer official snapshot whenever one is available.

## Legacy data

The old dataset was assembled before this provenance policy. Known classes of problems include administrative areas and border facilities mixed into the city list, duplicate/alias confusion, low-quality automatic English transliteration, and coordinates used as implicit evidence of identity. These issues are audited rather than silently hidden.

---

# سیاست منبع و بازسازی داده

> **مهم:** فایل `iran_cities.json` فعلاً یک دیتاست قدیمی برای سازگاری است و تا زمانی که از یک snapshot مشخصِ تقسیمات کشوری بازسازی و ممیزی نشود، نباید به‌عنوان «فهرست کامل و رسمی شهرهای ایران» معرفی شود.

عضویت یک رکورد در فهرست شهرها باید از منبع تقسیمات کشوری و نوع موجودیت «شهر» بیاید. مختصات، نتیجه جستجوی نقشه، کدپستی، نام انگلیسی یا شباهت نام فقط اطلاعات تکمیلی هستند و اثبات نمی‌کنند یک رکورد شهر رسمی است.

برای انتشار snapshot جدید، منبع، سال/تاریخ، checksum، آدرس یا شناسه آرشیو و دستور import را در `data/provenance.json` ثبت کنید و سپس validator و audit را اجرا کنید.
