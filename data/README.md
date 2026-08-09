# Data provenance and refresh policy

`iran_cities.json` is the canonical **source-backed 1402 snapshot** produced from the Statistical Center of Iran administrative-division export mirrored at a pinned upstream revision.

## Current canonical snapshot

- Publisher represented by the source: Statistical Center of Iran (SCI / مرکز آمار ایران)
- Snapshot year: **1402**
- Official source page identified by the upstream project: `https://amar.org.ir/geo`
- Mirror repository: `sajaddp/list-of-cities-in-Iran`
- Pinned mirror commit: `474942269f75ec247e1af5684f5e3eca9f304431`
- Source path: `offical/list.json`
- Raw `CODEREC=5` rows: **1,659**
- Source-relative municipal subareas excluded: **209**
- Canonical independent cities: **1,450**
- Provinces: **31**

The exact source SHA-256 is recorded in [`provenance.json`](provenance.json).

## Canonical membership rule

A `CODEREC=5` row is treated as a city unless it is a numbered/named municipal subarea whose derived base resolves to another `CODEREC=5` city in the **same province and county**. This rule removes rows such as municipal subdivisions without maintaining a manual deletion list.

The importer has hard invariants for the pinned snapshot: 1,659 raw rows, 209 excluded subareas, and 1,450 canonical cities. If those values unexpectedly change, rebuilding stops for review.

The complete exclusion audit trail is stored in [`excluded-urban-subareas-1402.json`](excluded-urban-subareas-1402.json).

## Membership vs enrichment

City membership and hierarchy come from the administrative source. These fields are optional enrichment and **do not prove identity or city status**:

- latitude / longitude
- English transliteration
- population
- postal code

The current checked-in audit reports zero membership/provenance blockers. Some enrichment remains incomplete or low-confidence; see [`audit-report.json`](audit-report.json).

## Rebuild workflow

The pinned importer is:

```bash
python scripts/rebuild_from_amar_1402.py \
  --source-json /path/to/pinned/offical/list.json \
  --legacy-json iran_cities.json \
  --output iran_cities.json \
  --provenance data/provenance.json \
  --excluded-report data/excluded-urban-subareas-1402.json

python scripts/validate_data.py
python scripts/audit_data.py --strict
python scripts/generate_all.py
```

The repository's **Tests** GitHub Actions workflow also exposes a manual `rebuild_1402=true` option. Rebuilds are intentionally explicit, not performed on every push.

## Refreshing beyond 1402

This repository must not label the 1402 snapshot as current for later years. To incorporate newer administrative decisions:

1. Obtain a newer official or clearly traceable administrative-division snapshot.
2. Record publisher, source URL/archive identifier, snapshot date/year, checksum, and license.
3. Pin the exact revision when a mirror is necessary.
4. Update the importer or add a reviewed source delta without using coordinates/name similarity as membership evidence.
5. Preserve existing compatibility IDs only for unambiguous matches.
6. Run structural validation and `audit_data.py --strict`.
7. Regenerate all derived outputs and update provenance.

## Licensing

Repository-authored code remains MIT. The 1402 source-backed dataset and its data derivatives are distributed under GPL-3.0 in accordance with the pinned upstream mirror; see [`../DATA_LICENSE.md`](../DATA_LICENSE.md) and [`../LICENSE-DATA-GPL-3.0`](../LICENSE-DATA-GPL-3.0).

---

# سیاست منبع و بازسازی داده

فایل `iran_cities.json` اکنون snapshot منبع‌دار تقسیمات کشوری **سال ۱۴۰۲** است. منبع خام ۱٬۶۵۹ ردیف `CODEREC=5` دارد که با یک قاعده منبع‌محور، ۲۰۹ زیرناحیه شهری از آن جدا شده و **۱٬۴۵۰ شهر مستقل در ۳۱ استان** باقی مانده است.

عضویت و سلسله‌مراتب از منبع تقسیمات کشوری می‌آید؛ مختصات، نام انگلیسی، جمعیت و کدپستی فقط enrichment هستند. گزارش `audit-report.json` برای عضویت هیچ blocker ندارد، اما کیفیت enrichment همچنان جداگانه قابل بهبود است.

برای تغییرات بعد از ۱۴۰۲ باید snapshot یا delta جدیدِ منبع‌دار، checksum، مجوز و تاریخ آن ثبت شود؛ داده ۱۴۰۲ نباید به‌عنوان snapshot جاری سال‌های بعد معرفی شود.
