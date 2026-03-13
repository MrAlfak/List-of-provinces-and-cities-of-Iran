# 🇮🇷 لیست کامل استان‌ها و شهرهای ایران

[![نسخه](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran)
[![لایسنس](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![زبان](https://img.shields.io/badge/language-Persian-red.svg)](README.fa.md)

این مخزن شامل **کامل‌ترین و حرفه‌ای‌ترین** دیتای استان‌ها و شهرهای ایران برای توسعه‌دهندگان است.

## ✨ ویژگی‌ها

✅ **883 شهر**: شامل تمامی شهرهای رسمی کشور  
📍 **مختصات جغرافیایی**: طول و عرض جغرافیایی دقیق برای هر شهر  
🏛️ **مرکز استان**: مشخص بودن مرکز هر استان با فیلد `is_capital`  
🌍 **چند فرمتی**: ارائه دیتا در قالب‌های JSON, SQL, CSV, و GeoJSON  
⚡ **نسخه Minified**: برای استفاده بهینه در پروژه‌های فرانت‌اِند  
🚀 **API Server**: اسکریپت آماده برای راه‌اندازی سریع API محلی  
🆔 **شناسه یکتا**: هر استان و شهر دارای ID یکتا  
🌐 **نام انگلیسی**: تمام استان‌ها و شهرها دارای نام انگلیسی  
👥 **جمعیت**: اطلاعات جمعیتی شهرها (در حال تکمیل)  
📮 **کد پستی**: کدهای پستی مراکز شهرها (در حال تکمیل)

## 📦 محتویات مخزن

```
├── iran_cities.json          # منبع اصلی دیتا (خوانا و کامل)
├── iran_cities.min.json      # نسخه فشرده برای وب
├── iran_cities.sql           # اسکریپت MySQL/PostgreSQL
├── iran_cities.csv           # مناسب برای Excel
├── iran_cities.geojson       # استاندارد GeoJSON
├── api_server.py             # سرور API ساده
├── tests/                    # تست‌های خودکار
└── docs/                     # مستندات کامل
```

## 🚀 نصب و استفاده

### 1️⃣ دانلود مستقیم


```bash
# دانلود فایل JSON
curl -O https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json

# یا با wget
wget https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json
```

### 2️⃣ استفاده در JavaScript/TypeScript

```javascript
// دانلود از CDN
fetch('https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.min.json')
  .then(response => response.json())
  .then(data => console.log(data));

// یا import مستقیم
import iranCities from './iran_cities.json';
```

### 3️⃣ استفاده در Python

```python
import json
import requests

# دانلود از اینترنت
url = 'https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json'
response = requests.get(url)
data = response.json()

# یا خواندن از فایل محلی
with open('iran_cities.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### 4️⃣ استفاده از SQL در دیتابیس

```bash
# MySQL
mysql -u username -p database_name < iran_cities.sql

# PostgreSQL
psql -U username -d database_name -f iran_cities.sql
```

### 5️⃣ راه‌اندازی API محلی

```bash
# نصب وابستگی‌ها
pip install flask flask-cors

# اجرای سرور
python api_server.py

# سرور روی پورت 8000 اجرا می‌شود
```

## 📡 API Endpoints

پس از اجرای `api_server.py`:

```
GET /api/provinces              # لیست تمام استان‌ها
GET /api/provinces/:id          # اطلاعات یک استان خاص
GET /api/cities                 # لیست تمام شهرها
GET /api/cities/:id             # اطلاعات یک شهر خاص
GET /api/search?q=تهران         # جستجو در شهرها و استان‌ها
```

## 📊 ساختار داده JSON


```json
{
  "id": 1,
  "province": "آذربایجان شرقی",
  "english_name": "East Azerbaijan",
  "phone_code": "041",
  "cities_count": 55,
  "cities": [
    {
      "id": 1,
      "name": "تبریز",
      "english_name": "Tabriz",
      "latitude": "38.0739964",
      "longitude": "46.2961952",
      "is_capital": true,
      "population": 1558693,
      "postal_code": "5138683751"
    }
  ]
}
```

## 🗺️ استفاده از GeoJSON در نقشه

```javascript
// با Leaflet
fetch('iran_cities.geojson')
  .then(response => response.json())
  .then(data => {
    L.geoJSON(data, {
      onEachFeature: function(feature, layer) {
        layer.bindPopup(feature.properties.name);
      }
    }).addTo(map);
  });

// با Mapbox
map.addSource('iran-cities', {
  type: 'geojson',
  data: 'iran_cities.geojson'
});
```

## 🧪 تست‌ها

```bash
# اجرای تست‌ها
python -m pytest tests/

# تست یکتا بودن نام‌ها
python tests/test_uniqueness.py

# تست صحت مختصات
python tests/test_coordinates.py
```

## 📈 آمار

- **31 استان**
- **883 شهر**
- **مختصات جغرافیایی دقیق**
- **کدهای تلفن استانی**
- **نام‌های فارسی و انگلیسی**

## 🤝 مشارکت

ما به دنبال کامل‌تر کردن این دیتا هستیم! اگر:

- اطلاعات جمعیتی دقیق دارید
- کدهای پستی شهرها را می‌دانید
- خطایی در داده‌ها پیدا کردید
- پیشنهاد بهبود دارید

لطفاً **Pull Request** بفرستید یا **Issue** باز کنید.

### راهنمای مشارکت

1. Fork کنید
2. برنچ جدید بسازید: `git checkout -b feature/amazing-feature`
3. تغییرات را commit کنید: `git commit -m 'Add amazing feature'`
4. Push کنید: `git push origin feature/amazing-feature`
5. Pull Request باز کنید

## 📝 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است - فایل [LICENSE](LICENSE) را ببینید.

## 🙏 تشکر

تهیه شده با ❤️ برای جامعه برنامه‌نویسی ایران

---

**آخرین بروزرسانی**: 2024  
**نسخه**: 2.0.0  
**نگهدارنده**: [@MrAlfak](https://github.com/MrAlfak)
