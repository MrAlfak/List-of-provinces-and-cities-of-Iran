# 🇮🇷 دیتاست استان‌ها و شهرهای ایران — JSON، CSV، GeoJSON، SQL و REST API

<div align="center">

**دیتاست منبع‌دار ۳۱ استان و ۱٬۴۵۰ شهر ایران برای وب‌سایت، اپلیکیشن، فرم آدرس، فروشگاه اینترنتی، CRM، لجستیک، GIS و پروژه‌های داده.**

[![GitHub stars](https://img.shields.io/github/stars/MrAlfak/List-of-provinces-and-cities-of-Iran?style=for-the-badge&logo=github&label=Stars)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/MrAlfak/List-of-provinces-and-cities-of-Iran?style=for-the-badge&logo=github&label=Forks)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/network/members)
[![Tests](https://img.shields.io/github/actions/workflow/status/MrAlfak/List-of-provinces-and-cities-of-Iran/tests.yml?branch=main&style=for-the-badge&label=CI)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/actions/workflows/tests.yml)
[![Last commit](https://img.shields.io/github/last-commit/MrAlfak/List-of-provinces-and-cities-of-Iran?style=for-the-badge)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/commits/main)

**فارسی** · **[English](README.md)** · **[شروع سریع](QUICKSTART.md)** · **[API](docs/API.md)** · **[کاربردها](docs/USE_CASES.md)** · **[مشارکت](CONTRIBUTING.md)**

⭐ **اگر این دیتاست برای پروژه‌ات مفید بود، Star بزن تا هم بعداً راحت پیدایش کنی و هم توسعه‌دهنده‌های بیشتری آن را ببینند.**

</div>

---

## چه چیزی دریافت می‌کنی؟

| قابلیت | وضعیت |
|---|---|
| استان‌ها | **۳۱** |
| شهرهای canonical | **۱٬۴۵۰** |
| snapshot تقسیمات کشوری | **مرکز آمار ایران - ۱۴۰۲** |
| JSON | ✅ |
| JSON فشرده | ✅ |
| CSV | ✅ |
| GeoJSON | ✅ زیرمجموعه دارای مختصات |
| MySQL | ✅ |
| PostgreSQL | ✅ |
| REST API | ✅ |
| جستجوی نرمال‌شده فارسی | ✅ |
| شناسه پایدار منبع | ✅ `uid` و `official_code` |
| شهرستان و بخش | ✅ |
| تست و CI | ✅ |

این پروژه برای جستجوهایی مثل **لیست شهرهای ایران JSON**، **لیست استان و شهر ایران**، **API شهرهای ایران**، **GeoJSON ایران**، **SQL شهرهای ایران**، **دیتابیس شهرهای ایران** و **Iran cities JSON** طراحی شده است.

## چرا این پروژه؟

- عضویت شهرها از منبع تقسیمات کشوری می‌آید، نه از حدس براساس مختصات یا شباهت نام.
- **۱٬۴۵۰ شهر مستقل** در تمام ۳۱ استان برای snapshot پین‌شده ۱۴۰۲.
- خروجی آماده برای frontend، backend، database و GIS.
- شناسه‌های `uid` و `official_code` برای هویت منبع‌دار.
- اطلاعات شهرستان و بخش برای فرم‌های آدرس دقیق‌تر.
- REST API نسخه‌بندی‌شده با pagination و نرمال‌سازی جستجوی فارسی.
- importer، validator و audit قابل بازتولید.
- Docker و CI آماده.

## استفاده در ۳۰ ثانیه

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

### دیتابیس

```text
iran_cities.mysql.sql
iran_cities.postgresql.sql
```

برای مثال‌های بیشتر از فرم آدرس، فروشگاه، CRM، لجستیک و GIS فایل [`docs/USE_CASES.md`](docs/USE_CASES.md) را ببین.

## کاربردهای رایج

- dropdown استان ← شهر در React، Next.js، Vue، Angular و اپ‌های موبایل
- فرم ثبت آدرس و پروفایل کاربر
- checkout و ارسال سفارش فروشگاه‌های اینترنتی
- CRM و ERP
- سیستم‌های پخش، ارسال، لجستیک و dispatch
- نقشه و GIS با GeoJSON
- Laravel، Django، Flask، Node.js و backendهای دیگر
- autocomplete و جستجوی نام شهرهای فارسی
- گزارش‌گیری و تحلیل مکانی
- seed دیتابیس MySQL و PostgreSQL

## فایل‌های داده

```text
iran_cities.json                         # فهرست کامل canonical
iran_cities.min.json                     # JSON فشرده
iran_cities.csv                          # CSV
iran_cities.geojson                      # زیرمجموعه geocoded
iran_cities.mysql.sql                    # MySQL
iran_cities.postgresql.sql               # PostgreSQL
```

برای هویت منبع‌دار، `official_code` و `uid` را به `id` عددی ترجیح بده؛ `id` بیشتر برای سازگاری نسخه‌های قبلی حفظ شده است.

## صحت و منبع داده

> [!IMPORTANT]
> `iran_cities.json` بر اساس **snapshot تقسیمات کشوری سال ۱۴۰۲ مرکز آمار ایران** ساخته شده است و وضعیت «تا ۱۴۰۲» را نشان می‌دهد؛ تغییرات اداری بعد از آن فقط با snapshot یا delta منبع‌دار جدید وارد می‌شوند.

منبع خام **۱٬۶۵۹** ردیف `CODEREC=5` دارد. importer فقط **۲۰۹** زیرناحیه شهری را زمانی کنار می‌گذارد که شهر پایه در همان استان و شهرستان وجود داشته باشد؛ خروجی نهایی **۱٬۴۵۰ شهر canonical** است.

وضعیت audit سخت‌گیرانه فعلی:

- ۳۱ استان
- ۱٬۴۵۰ شهر
- ۰ `official_code` گمشده
- ۰ `official_code` تکراری
- ۰ blocker عضویت/provenance
- وضعیت: `source-backed`

commit منبع و SHA-256 دقیق در [`data/provenance.json`](data/provenance.json) ثبت شده و ۲۰۹ ردیف کنارگذاشته‌شده در [`data/excluded-urban-subareas-1402.json`](data/excluded-urban-subareas-1402.json) قابل بررسی‌اند.

### وضعیت اطلاعات تکمیلی

مختصات و نام انگلیسی enrichment هستند و برای تعیین شهر بودن استفاده نمی‌شوند. فعلاً بخشی از enrichment عمداً خالی مانده تا مقدار ساختگی وارد نشود:

- ۷۰۳ شهر بدون مختصات
- ۷۰۳ شهر بدون نام انگلیسی تکمیلی
- ۳۱۹ transliteration قدیمی ضعیف برای review
- ۱ گروه مختصات تکراری برای review

بنابراین `iran_cities.geojson` فقط شهرهای دارای مختصات معتبر را شامل می‌شود؛ برای فهرست کامل از `iran_cities.json` استفاده کن.

## توسعه محلی

```bash
git clone https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran.git
cd List-of-provinces-and-cities-of-Iran
python -m pip install -r requirements.txt
python scripts/validate_data.py
python scripts/audit_data.py --strict
python -m pytest tests/
python scripts/generate_all.py
```

API:

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

## کمک به رشد پروژه

اگر از این دیتاست در اپ، سایت، پایان‌نامه، داشبورد، فروشگاه، CRM یا سیستم لجستیک استفاده می‌کنی:

1. ⭐ پروژه را **Star** کن.
2. 🍴 برای توسعه‌های جدید Fork بگیر.
3. 🐛 خطاهای داده را با Issue گزارش کن.
4. 🔗 در پروژه‌ای که از دیتاست استفاده می‌کند به این مخزن لینک بده.
5. 🤝 اصلاحات منبع‌دار و integrationهای مفید را PR کن.

## کلیدواژه‌ها

`لیست شهرهای ایران` · `لیست استان های ایران` · `دیتابیس شهرهای ایران` · `JSON شهرهای ایران` · `API شهرهای ایران` · `GeoJSON ایران` · `SQL شهرهای ایران` · `iran cities json` · `iran provinces json` · `iranian cities` · `persian cities` · `farsi cities` · `iran location data` · `iran administrative divisions`

## مجوز

- **کد مخزن:** MIT — [`LICENSE`](LICENSE)
- **دیتاست منبع‌دار ۱۴۰۲ و مشتقات:** GPL-3.0 — [`DATA_LICENSE.md`](DATA_LICENSE.md)، [`LICENSE-DATA-GPL-3.0`](LICENSE-DATA-GPL-3.0)

**نسخه:** ۲.۱.۰
