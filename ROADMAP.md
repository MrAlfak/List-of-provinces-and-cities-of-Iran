# 🗺️ Roadmap

## Current baseline — completed in v2.1 work

The repository now has a source-backed canonical membership baseline for the **SCI 1402 administrative snapshot**:

- 31 provinces
- 1,450 independent city records
- pinned source revision + SHA-256 provenance
- source-relative urban-subarea exclusion audit trail
- stable `uid` / `official_code`
- county/district hierarchy
- strict membership audit with zero blockers
- MySQL/PostgreSQL/CSV/minified JSON generation
- GeoJSON geocoded subset with explicit missing-coordinate metadata
- versioned read-only API and hardened Docker runtime
- Python 3.10/3.12 + Docker CI
- code/data licensing documented separately

## Priority 1 — newer administrative snapshot

The canonical membership is **as of 1402**. The next data-integrity milestone is not a new API feature; it is obtaining and reviewing a newer official/traceable country-divisions snapshot or sourced delta.

Required work:

- identify newer official publication(s) after 1402;
- archive/pin source URL, date, checksum, and license;
- diff by source identifiers/hierarchy rather than coordinates;
- preserve compatibility IDs only on unambiguous matches;
- run strict membership audit and regenerate every derivative;
- document additions, removals, renames, county/district moves and effective dates.

## Priority 2 — enrichment quality

Membership is no longer blocked by enrichment debt. Current audit debt includes missing coordinates/English names and weak historical transliterations.

Planned work:

- source and verify coordinates independently of city membership;
- replace weak automatic transliterations with reviewed English names;
- review duplicate coordinate groups instead of deleting records automatically;
- add provenance/confidence fields for enrichment sources;
- optionally add population/postal enrichment only from identified sources.

`audit_data.py --strict-enrichment` can be used when a downstream consumer requires complete enrichment.

## Priority 3 — package/release quality

- build a self-contained Python package/wheel with canonical data bundled correctly;
- clean-install test the Python package in CI before re-enabling PyPI;
- verify npm package contents/license notices against the dual-license data model;
- generate release manifests/checksums for all data artifacts;
- document schema compatibility and migration expectations.

## Priority 4 — API scale only after data/release quality

Potential later additions:

- caching / ETag / conditional requests;
- rate limiting for a hosted service;
- richer county/district filters;
- OpenAPI schema;
- optional spatial queries when coordinate coverage is sufficiently verified.

GraphQL, AI-powered search, and other feature expansion remain lower priority than data provenance, enrichment quality, and reproducible releases.

---

# نقشه راه فارسی

## وضعیت فعلی

baseline منبع‌دار تقسیمات کشوری **۱۴۰۲** تکمیل شده است: ۳۱ استان، ۱٬۴۵۰ شهر مستقل، provenance پین‌شده، شناسه‌های منبع‌دار، audit سخت‌گیرانه بدون blocker و CI کامل.

## اولویت بعدی

اولویت بعدی پیدا کردن snapshot رسمی/قابل‌ردیابی **جدیدتر از ۱۴۰۲** و اعمال تغییرات اداری جدید با diff منبع‌محور است؛ نه اضافه‌کردن قابلیت‌های نمایشی جدید.

پس از آن، تکمیل enrichmentها مثل مختصات و نام انگلیسی، سپس packaging/release قابل اعتماد و در نهایت توسعه بیشتر API انجام می‌شود.
