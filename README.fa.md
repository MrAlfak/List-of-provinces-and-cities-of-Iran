# 🇮🇷 داده استان‌ها و شهرهای ایران

[![Tests](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml/badge.svg)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

فارسی | [English](README.md)

یک دیتاست توسعه‌دهنده‌محور برای اطلاعات مکانی ایران، همراه با JSON، CSV، GeoJSON، تولیدکننده SQL، API خواندنی، ابزارهای اعتبارسنجی و مسیر مشخص برای ثبت منبع داده.

> [!WARNING]
> **وضعیت داده:** فایل فعلی `iran_cities.json` یک دیتاست **قدیمی و هنوز تأییدنشده به‌عنوان مرجع رسمی** است. نسخه‌های قبلی اشتباهاً همه رکوردها را «شهر رسمی» معرفی می‌کردند. در داده قدیمی مواردی از مخلوط‌شدن واحدهای اداری/پایانه‌های مرزی با شهرها و همچنین نام‌های انگلیسی ماشینی کم‌کیفیت وجود دارد. تا قبل از بازسازی از یک snapshot مشخص تقسیمات کشوری و عبور از audit سخت‌گیرانه، از این فایل به‌عنوان مرجع قانونی یا رسمی استفاده نکنید.

## تغییرات مهم نسخه ۲.۱

- حذف چرخه اشتباه که JSON همین مخزن را دوباره به‌عنوان منبع بالادستی دانلود می‌کرد.
- حذف لیست دستی و خطرناک برای پاک‌کردن «تکراری‌ها»؛ اکنون فقط duplicate کاملاً یکسان قابل حذف خودکار است.
- اضافه‌شدن pipeline بازسازی بر اساس نوع رسمی تقسیمات کشوری (`divisionType=5` برای شهر).
- حفظ ID عددی قبلی تا حد امکان و اضافه‌شدن `uid` و `official_code` پایدار برای داده منبع‌دار.
- جداسازی اعتبارسنجی ساختاری از ممیزی معنایی و کیفیت enrichment.
- امن‌ترشدن API: نسخه `/api/v1`، pagination، نرمال‌سازی فارسی، CORS اختیاری، health/meta و حذف debug پیش‌فرض.
- تولید SQL واقعی و جداگانه برای MySQL و PostgreSQL با escaping صحیح.
- اجرای API داخل Docker با Gunicorn، کاربر non-root و healthcheck واقعی.
- CI برای validator، تست‌ها، audit، ساخت خروجی‌ها و smoke-test کانتینر.

## فایل‌های اصلی

```text
iran_cities.json               # دیتاست قدیمی سازگاری / خروجی اصلی پس از rebuild تأییدشده
iran_cities.min.json           # JSON فشرده مشتق‌شده
iran_cities.csv                # CSV مشتق‌شده
iran_cities.geojson            # GeoJSON مشتق‌شده
api_server.py                   # API فقط خواندنی
scripts/rebuild_from_divisions.py
scripts/validate_data.py
scripts/audit_data.py
scripts/generate_all.py
data/provenance.json            # وضعیت و سیاست منبع داده
```

فایل‌های SQL به‌صورت قابل بازتولید ساخته می‌شوند:

```bash
python scripts/generate_sql.py --dialect both
# iran_cities.mysql.sql
# iran_cities.postgresql.sql
```

## شروع سریع

```bash
git clone https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran.git
cd List-of-provinces-and-cities-of-Iran
python -m pip install -r requirements.txt
python scripts/validate_data.py
python -m pytest tests/
python scripts/audit_data.py
```

Audit معمولی روی دیتاست legacy فقط گزارش می‌دهد. دیتاست جدیدی که از منبع تقسیمات کشوری بازسازی شده باید حالت strict را هم پاس کند:

```bash
python scripts/audit_data.py --input iran_cities.rebuilt.json --strict
```

## بازسازی از تقسیمات کشوری

پاسخ به سؤال **«آیا این رکورد واقعاً شهر است؟»** باید از منبع مشخص تقسیمات کشوری بیاید، نه از مختصات، نتیجه نقشه یا شباهت نام.

Importer ورودی CSV نرمال‌شده UTF-8 با ستون‌های زیر را می‌پذیرد:

```text
id,parentCountryDivisionId,name,code,divisionType
```

که در آن `divisionType=5` یعنی شهر.

```bash
python scripts/rebuild_from_divisions.py \
  --divisions-csv /path/to/divisions.csv \
  --legacy-json iran_cities.json \
  --output iran_cities.rebuilt.json

python scripts/validate_data.py --input iran_cities.rebuilt.json
python scripts/audit_data.py --input iran_cities.rebuilt.json --strict
```

جزئیات بیشتر در [`data/README.md`](data/README.md) و [`data/provenance.json`](data/provenance.json) آمده است. فایل تقسیمات کشوری سال ۱۳۹۸ مرکز آمار ایران یک baseline بازتولیدپذیر است، اما برای انتشار جدید باید در صورت دسترسی از snapshot رسمی جدیدتر استفاده شود.

## API

برای توسعه محلی:

```bash
python api_server.py
```

برای اجرای مشابه production:

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

مسیرهای قدیمی `/api/...` برای سازگاری باقی مانده‌اند. CORS فقط در صورت تنظیم صریح `CORS_ORIGINS` فعال می‌شود.

## مدل داده

در snapshot منبع‌دار، علاوه بر فیلدهای قبلی می‌توان شناسه پایدار و سلسله‌مراتب را داشت:

```json
{
  "id": 1,
  "uid": "ir:province:<source-code>",
  "official_code": "<source-code>",
  "province": "...",
  "cities": [
    {
      "id": 1,
      "uid": "ir:city:<source-code>",
      "official_code": "<source-code>",
      "name": "...",
      "county": "...",
      "district": "...",
      "latitude": null,
      "longitude": null
    }
  ]
}
```

مختصات و نام انگلیسی enrichment هستند و تا زمان تأیید مستقل می‌توانند `null` باشند.

## اصلاح داده

برای هر اصلاح داده، منبع و تاریخ/snapshot پشتیبان تغییر را ارائه کنید. صرفاً به دلیل یکسان‌بودن مختصات، شباهت نوشتاری یا alias بودن، یک رکورد را حذف نکنید.

## انتشار

پکیج npm قبل از انتشار اعتبارسنجی، تست و بازتولید می‌شود. انتشار PyPI عمداً غیرفعال شده تا زمانی که wheel مستقل و قابل نصب ساخته و در CI تست شود.

## مجوز

کد و محتوای تولیدشده در خود مخزن تحت MIT است؛ منبع‌های داده بالادستی ممکن است شرایط و مجوز جداگانه داشته باشند و باید قبل از import ثبت شوند.

**نسخه:** ۲.۱.۰
