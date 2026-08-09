# 🇮🇷 داده استان‌ها و شهرهای ایران

[![Tests](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml/badge.svg)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml)
[![Code License](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE)
[![Data License](https://img.shields.io/badge/data-GPL--3.0-blue.svg)](DATA_LICENSE.md)

فارسی | [English](README.md)

دیتاست توسعه‌دهنده‌محور شهرهای ایران با عضویت منبع‌دار، خروجی‌های JSON/CSV/GeoJSON/SQL، API فقط‌خواندنی، اعتبارسنجی، provenance و بازسازی قابل تکرار.

> [!IMPORTANT]
> **وضعیت دیتاست اصلی:** `iran_cities.json` بر اساس **snapshot تقسیمات کشوری سال ۱۴۰۲ مرکز آمار ایران** بازسازی شده است. منبع خام ۱٬۶۵۹ ردیف `CODEREC=5` دارد؛ ۲۰۹ زیرناحیه/منطقه شهری فقط زمانی کنار گذاشته می‌شوند که شهر پایه در همان استان و شهرستان وجود داشته باشد. نتیجه **۱٬۴۵۰ شهر مستقل در ۳۱ استان** است. این snapshot «تا ۱۴۰۲» منبع‌دار است و پوشش تغییرات اداری بعد از آن را ادعا نمی‌کند.

## وضعیت صحت

- ۳۱ استان / ۱٬۴۵۰ شهر canonical
- ۰ رکورد بدون `official_code`
- ۰ `official_code` تکراری
- ۰ blocker عضویت/provenance
- وضعیت provenance: `source-backed`
- checksum و commit پین‌شده منبع در [`data/provenance.json`](data/provenance.json)

Enrichment جداگانه سنجیده می‌شود: **۷۰۳ شهر فعلاً مختصات و نام انگلیسی تکمیلی ندارند**، ۳۱۹ transliteration انگلیسی قدیمی ضعیف علامت خورده و یک گروه مختصات تکراری برای بررسی باقی مانده است. این موارد برای تشخیص «شهر بودن» استفاده نمی‌شوند.

## منبع

```text
ناشر: مرکز آمار ایران
صفحه رسمی معرفی‌شده در منبع بالادستی: https://amar.org.ir/geo
Mirror: sajaddp/list-of-cities-in-Iran
Pinned commit: 474942269f75ec247e1af5684f5e3eca9f304431
Pinned path: offical/list.json
Snapshot: 1402
```

بازسازی با [`scripts/rebuild_from_amar_1402.py`](scripts/rebuild_from_amar_1402.py) انجام می‌شود. checksum، آمار و سیاست refresh در [`data/provenance.json`](data/provenance.json) و ۲۰۹ ردیف کنارگذاشته‌شده در [`data/excluded-urban-subareas-1402.json`](data/excluded-urban-subareas-1402.json) ثبت شده‌اند.

Rebuild با هر push اجرا نمی‌شود؛ workflow **Tests** را دستی با `rebuild_1402=true` اجرا کنید. importer اگر تعداد ۱٬۶۵۹ ردیف خام، ۲۰۹ حذف یا ۱٬۴۵۰ شهر نهایی تغییر غیرمنتظره کند، متوقف می‌شود.

## بهبودهای اصلی نسخه ۲.۱

- حذف self-download و لیست دستی خطرناک حذف رکوردها.
- حفظ ID قدیمی فقط در match بدون ابهام؛ `uid` و `official_code` هویت منبع‌دار هستند.
- اضافه‌شدن شهرستان و بخش.
- جداسازی validation ساختاری، audit عضویت و audit enrichment.
- API نسخه‌بندی‌شده و امن‌تر، SQL جداگانه MySQL/PostgreSQL، Docker با Gunicorn/non-root.
- GeoJSON فقط برای رکوردهای دارای مختصات معتبر.
- CI برای invariantهای ۳۱ استان/۱٬۴۵۰ شهر، تست‌ها، تولید artifact و Docker health.

## فایل‌های مهم

```text
iran_cities.json                         # دیتاست اصلی ۱۴۰۲ - ۱٬۴۵۰ شهر
iran_cities.min.json                     # JSON فشرده
iran_cities.csv                          # CSV
iran_cities.geojson                      # زیرمجموعه geocoded
iran_cities.mysql.sql                    # MySQL
iran_cities.postgresql.sql               # PostgreSQL
scripts/rebuild_from_amar_1402.py        # importer پین‌شده
scripts/validate_data.py                 # validation ساختاری
scripts/audit_data.py                    # audit عضویت/enrichment
data/provenance.json                     # منبع و checksum
data/audit-report.json                   # گزارش audit
data/excluded-urban-subareas-1402.json   # ۲۰۹ ردیف کنارگذاشته‌شده
DATA_LICENSE.md                          # مجوز داده
```

## شروع سریع

```bash
python -m pip install -r requirements.txt
python scripts/validate_data.py
python scripts/audit_data.py --strict
python -m pytest tests/
python scripts/generate_all.py
```

## API

```bash
python api_server.py
# یا
docker compose up --build
```

```text
GET /health
GET /api/v1/meta
GET /api/v1/provinces
GET /api/v1/provinces/<id>
GET /api/v1/cities?page=1&per_page=100&province_id=<id>&q=<query>
GET /api/v1/cities/<id>
GET /api/v1/search?q=<query>
```

مختصات و نام انگلیسی اختیاری‌اند و می‌توانند `null` باشند. برای هویت منبع‌دار از `official_code` / `uid` استفاده کنید؛ `id` عددی بیشتر برای سازگاری legacy حفظ شده است.

## GeoJSON

`iran_cities.geojson` فقط شهرهای دارای مختصات معتبر را شامل می‌شود. برای فهرست کامل ۱٬۴۵۰ شهر از `iran_cities.json` استفاده کنید.

## تازگی داده و اصلاحات

هر تغییر عضویت/سلسله‌مراتب باید منبع و تاریخ/snapshot داشته باشد. رکوردی صرفاً به دلیل مختصات یکسان یا شباهت نام حذف نمی‌شود. تغییرات بعد از ۱۴۰۲ باید از snapshot جدیدتر یا delta منبع‌دار reviewشده وارد شوند.

## مجوز

- **کد مخزن:** MIT — [`LICENSE`](LICENSE)
- **دیتاست منبع‌دار ۱۴۰۲ و مشتقات:** GPL-3.0 — [`DATA_LICENSE.md`](DATA_LICENSE.md)، [`LICENSE-DATA-GPL-3.0`](LICENSE-DATA-GPL-3.0)

**نسخه:** ۲.۱.۰
