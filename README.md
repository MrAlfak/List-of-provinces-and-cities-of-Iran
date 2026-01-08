# لیست جامع استان‌ها و شهرهای ایران (Iran Provinces and Cities)

این مخزن شامل کامل‌ترین و حرفه‌ای‌ترین دیتای استان‌ها و شهرهای ایران برای توسعه‌دهندگان است.

## ویژگی‌ها (Features)
- ✅ **۸۹۵ شهر**: شامل تمامی شهرهای رسمی کشور.
- 📍 **مختصات جغرافیایی**: طول و عرض جغرافیایی دقیق برای هر شهر.
- 🏛️ **مرکز استان**: مشخص بودن مرکز هر استان با فیلد `is_capital`.
- 🌍 **چند فرمتی**: ارائه دیتا در قالب‌های JSON, SQL, CSV, و GeoJSON.
- ⚡ **نسخه Minified**: برای استفاده بهینه در پروژه‌های فرانت‌اِند.
- 🚀 **API Server**: اسکریپت آماده برای راه‌اندازی سریع API محلی.

## محتویات مخزن (Repository Contents)
- `iran_cities.json`: منبع اصلی دیتا (خوانا).
- `iran_cities.min.json`: نسخه فشرده برای وب.
- `iran_cities.sql`: اسکریپت ساخت جداول و درج دیتا در MySQL/PostgreSQL.
- `iran_cities.csv`: مناسب برای اکسل و تحلیل داده.
- `iran_cities.geojson`: استاندارد جغرافیایی برای نمایش در نقشه‌ها (Leaflet, Mapbox).
- `api_server.py`: سرور API ساده با پایتون.

## نحوه استفاده (Usage)

### ۱. استفاده از SQL در دیتابیس
فایل `iran_cities.sql` شامل دستورات `CREATE TABLE` و `INSERT` است که دو جدول `provinces` و `cities` را با روابط کلید خارجی ایجاد می‌کند.

### ۲. راه‌اندازی API محلی
اگر پایتون نصب دارید، دستور زیر را اجرا کنید:
```bash
python api_server.py
```
سپس می‌توانید از آدرس‌های زیر استفاده کنید:
- لیست کل استان‌ها: `http://localhost:8000/api/provinces`
- دیتای یک استان خاص: `http://localhost:8000/api/province/Tehran`

### ۳. استفاده از GeoJSON در نقشه
فایل `iran_cities.geojson` را می‌توانید مستقیماً در کتابخانه‌هایی مثل Leaflet بارگذاری کنید:
```javascript
L.geoJSON(iranCitiesData).addTo(map);
```

## ساختار داده JSON
```json
{
  "province": "آذربایجان شرقی",
  "english_name": "East Azerbaijan",
  "phone_code": "041",
  "cities": [
    {
      "name": "تبریز",
      "latitude": "38.0800",
      "longitude": "46.2919",
      "is_capital": true
    }
  ]
}
```

## مشارکت (Contribution)
ما به دنبال کامل‌تر کردن این دیتا هستیم (مثلاً افزودن جمعیت یا شهرستان‌ها). اگر دیتای دقیقی دارید، Pull Request بفرستید!

---
تهیه شده با ❤️ برای جامعه برنامه‌نویسی ایران.
