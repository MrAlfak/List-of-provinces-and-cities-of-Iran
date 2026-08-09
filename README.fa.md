# 🇮🇷 داده استان‌ها و شهرهای ایران

[![Tests](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml/badge.svg)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml)
[![Code License](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE)
[![Data License](https://img.shields.io/badge/data-GPL--3.0-blue.svg)](DATA_LICENSE.md)

فارسی | [English](README.md)

یک دیتاست توسعه‌دهنده‌محور برای شهرهای ایران با عضویت منبع‌دار، خروجی‌های JSON/CSV/GeoJSON/SQL، API فقط‌خواندنی، اعتبارسنجی، provenance و pipeline بازسازی قابل تکرار.

> [!IMPORTANT]
> **وضعیت دیتاست اصلی:** فایل `iran_cities.json` بر اساس **snapshot تقسیمات کشوری سال ۱۴۰۲ مرکز آمار ایران** بازسازی شده است. منبع خام ۱٬۶۵۹ ردیف `CODEREC=5` دارد؛ ۲۰۹ ردیف که به‌صورت منبع‌محور زیرناحیه/منطقه شهری تشخیص داده می‌شوند فقط زمانی حذف می‌شوند که شهر پایه در همان استان و شهرستان وجود داشته باشد. نتیجه، **۱٬۴۵۰ شهر مستقل در ۳۱ استان** است. این دیتاست «تا سال ۱۴۰۲» منبع‌دار است و ادعا نمی‌کند تغییرات اداری بعد از آن را پوشش می‌دهد.

## وضعیت صحت داده

دیتاست فعلی audit سخت‌گیرانه عضویت را پاس می‌کند:

- ۳۱ استان
- ۱٬۴۵۰ شهر اصلی
- ۰ رکورد بدون `official_code`
- ۰ `official_code` تکراری
- ۰ blocker مربوط به عضویت یا provenance
- وضعیت provenance: `source-backed`
- checksum و commit ثابت منبع در [`data/provenance.json`](data/provenance.json) ثبت شده است.

کیفیت enrichment جداگانه سنجیده می‌شود. در حال حاضر **۷۰۳ شهر فاقد مختصات و نام انگلیسی تکمیلی هستند**، ۳۱۹ نام انگلیسی قدیمی به‌عنوان transliteration ضعیف/ماشینی علامت خورده‌اند و یک گروه مختصات تکراری برای بررسی باقی مانده است. هیچ‌کدام از این موارد برای تصمیم «شهر بودن یا نبودن» استفاده نمی‌شوند.

## منبع و قابلیت بازتولید

عضویت شهرها با [`scripts/rebuild_from_amar_1402.py`](scripts/rebuild_from_amar_1402.py) از snapshot پین‌شده ۱۴۰۲ بازسازی می‌شود:

```text
ناشر: مرکز آمار ایران
صفحه رسمی معرفی‌شده در منبع بالادستی: https://amar.org.ir/geo
Mirror: sajaddp/list-of-cities-in-Iran
Pinned commit: 474942269f75ec247e1af5684f5e3eca9f304431
Pinned source path: offical/list.json
Snapshot: 1402
```

checksum دقیق، تعداد رکوردها و سیاست refresh در [`data/provenance.json`](data/provenance.json) ثبت شده است. ۲۰۹ ردیف حذف‌شده نیز برای audit در [`data/excluded-urban-subareas-1402.json`](data/excluded-urban-subareas-1402.json) نگهداری می‌شوند.

بازسازی داده دیگر با هر push اجرا نمی‌شود. برای بازسازی، workflow **Tests** را به‌صورت دستی با `rebuild_1402=true` اجرا کنید یا importer را محلی روی فایل پین‌شده اجرا کنید. importer سه invariant سخت دارد: ۱٬۶۵۹ ردیف خام، ۲۰۹ زیرناحیه حذف‌شده و ۱٬۴۵۰ شهر نهایی؛ اگر منبع یا قاعده عوض شود، build متوقف می‌شود.

## تغییرات مهم نسخه ۲.۱

- حذف pipeline حلقوی که JSON خود مخزن را به‌عنوان منبع دوباره مصرف می‌کرد.
- جایگزینی لیست دستی حذف رکورد با طبقه‌بندی منبع‌محور و محافظه‌کارانه.
- حفظ ID عددی قدیمی فقط در match بدون ابهام؛ `uid` و `official_code` منبع‌دار شناسه‌های پایدار هستند.
- اضافه‌شدن شهرستان و بخش به ساختار شهرها.
- جداسازی validation ساختاری، audit عضویت و audit enrichment.
- امن‌ترشدن API با `/api/v1`، pagination، نرمال‌سازی فارسی، CORS اختیاری، health/meta و debug خاموش.
- تولید جداگانه SQL برای MySQL و PostgreSQL با escaping صحیح.
- GeoJSON فقط برای شهرهای دارای مختصات معتبر تولید می‌شود و مختصات ساختگی ایجاد نمی‌کند.
- اجرای Docker با Gunicorn، کاربر non-root و healthcheck واقعی.
- CI روی invariantهای ۳۱ استان / ۱٬۴۵۰ شهر، تست‌ها، تولید خروجی‌ها و smoke-test Docker کنترل دارد.

## فایل‌های اصلی

```text
iran_cities.json                         # دیتاست اصلی منبع‌دار ۱۴۰۲ - ۱٬۴۵۰ شهر
iran_cities.min.json                     # JSON فشرده
iran_cities.csv                          # خروجی CSV
iran_cities.geojson                      # فقط زیرمجموعه دارای مختصات
iran_cities.mysql.sql                    # خروجی MySQL
iran_cities.postgresql.sql               # خروجی PostgreSQL
api_server.py                            # API فقط‌خواندنی
scripts/rebuild_from_amar_1402.py        # importer پین‌شده ۱۴۰۲
scripts/rebuild_from_divisions.py        # importer عمومی تقسیمات نرمال‌شده
scripts/validate_data.py                 # اعتبارسنجی ساختاری
scripts/audit_data.py                    # audit عضویت/enrichment
scripts/generate_all.py                  # تولید خروجی‌های مشتق‌شده
data/provenance.json                     # منبع، checksum، آمار و سیاست داده
data/audit-report.json                   # گزارش audit ثبت‌شده
data/excluded-urban-subareas-1402.json   # ۲۰۹ زیرناحیه حذف‌شده
DATA_LICENSE.md                          # مجوز و attribution داده
```

## شروع سریع

```bash
git clone https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran.git
cd List-of-provinces-and-cities-of-Iran
python -m pip install -r requirements.txt
python scripts/validate_data.py
python scripts/audit_data.py --strict
python -m pytest tests/
```

برای بازتولید خروجی‌ها:

```bash
python scripts/generate_all.py
```

## API

اجرای محلی:

```bash
python api_server.py
```

اجرای مشابه production:

```bash
docker compose up --build
```

Endpointهای اصلی:

```text
GET /health
GET /api/v1/meta
GET /api/v1/provinces
GET /api/v1/provinces/<id>
GET /api/v1/cities?page=1&per_page=100&province_id=<id>&q=<query>
GET /api/v1/cities/<id>
GET /api/v1/search?q=<query>
```

مسیرهای قدیمی `/api/...` برای سازگاری باقی مانده‌اند. CORS فقط با تنظیم صریح `CORS_ORIGINS` فعال می‌شود.

## مدل داده

```json
{
  "id": 1,
  "uid": "ir:province:1402:<province-code>",
  "official_code": "1402:<province-code>",
  "province": "...",
  "cities": [
    {
      "id": 1,
      "uid": "ir:city:1402:<province>:<county>:<district>:<city>",
      "official_code": "1402:<province>:<county>:<district>:<city>",
      "name": "...",
      "county": "...",
      "county_code": "...",
      "district": "...",
      "district_code": "...",
      "latitude": null,
      "longitude": null,
      "english_name": null
    }
  ]
}
```

`official_code` و سلسله‌مراتب منبع، عضویت رکورد را مشخص می‌کنند. مختصات و نام انگلیسی enrichment اختیاری هستند و می‌توانند `null` باشند.

## نکته GeoJSON

`iran_cities.geojson` فقط شهرهایی را شامل می‌شود که مختصات معتبر دارند. metadata فایل تعداد کل شهرهای canonical، تعداد featureهای geocoded و تعداد رکوردهای بدون مختصات را گزارش می‌کند. برای فهرست کامل ۱٬۴۵۰ شهر از `iran_cities.json` استفاده کنید.

## اصلاح داده

برای تغییر عضویت یا سلسله‌مراتب، منبع و تاریخ/snapshot ارائه کنید. یک رکورد فقط به دلیل مختصات یکسان، شباهت نوشتاری یا alias بودن حذف نمی‌شود. تغییرات اداری جدیدتر باید از snapshot جدیدتر یا delta منبع‌دار و reviewشده وارد شوند.

## انتشار

npm قبل از انتشار validate، test و regenerate می‌شود. PyPI تا زمان ساخت wheel مستقل و تست clean-install در CI غیرفعال باقی می‌ماند.

## مجوز

- **کد تولیدشده در این مخزن:** MIT — فایل [`LICENSE`](LICENSE).
- **دیتاست منبع‌دار ۱۴۰۲ و خروجی‌های داده‌ای مشتق‌شده:** GPL-3.0 — فایل‌های [`DATA_LICENSE.md`](DATA_LICENSE.md) و [`LICENSE-DATA-GPL-3.0`](LICENSE-DATA-GPL-3.0).

**نسخه:** ۲.۱.۰
