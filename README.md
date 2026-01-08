# لیست جامع استان‌ها و شهرهای ایران (Iran Provinces and Cities)

این مخزن شامل لیست جامع، دقیق و به‌روز استان‌ها و شهرهای ایران (۸۹۵ شهر) به همراه مختصات جغرافیایی است.

## ویژگی‌ها (Features)
- ✅ **لیست ۸۹۵ شهر**: شامل تمامی شهرهای رسمی کشور.
- 📍 **مختصات جغرافیایی**: دارای طول و عرض جغرافیایی (Latitude/Longitude) برای هر شهر.
- 🌍 **دو زبانه**: نام انگلیسی هر استان برای استفاده در Slug و API.
- ☎️ **اطلاعات مخابراتی**: پیش‌شماره تلفن هر استان.
- 📂 **فرمت‌های متنوع**: ارائه داده‌ها در قالب JSON و CSV.

## محتویات (Contents)
- **iran_cities.json**: منبع اصلی داده‌ها به فرمت JSON (شامل مختصات).
- **iran_cities.csv**: نسخه CSV داده‌ها برای استفاده در دیتابیس و اکسل.

## ساختار داده JSON
```json
{
  "province": "آذربایجان شرقی",
  "english_name": "East Azerbaijan",
  "phone_code": "041",
  "cities_count": 59,
  "cities": [
    {
      "name": "تبریز",
      "latitude": "38.0800",
      "longitude": "46.2919"
    },
    ...
  ]
}
```

## نحوه استفاده در JavaScript
```javascript
const data = require('./iran_cities.json');
const tehran = data.find(p => p.english_name === 'Tehran');
console.log(`تعداد شهرهای استان تهران: ${tehran.cities_count}`);
console.log(`مختصات تهران: ${tehran.cities[0].latitude}, ${tehran.cities[0].longitude}`);
```

## مشارکت (Contribution)
اگر شهر یا اطلاعاتی نیاز به اصلاح دارد یا فکر می‌کنید دیتای کامل‌تری وجود دارد، خوشحال می‌شویم با ارسال یک Pull Request کمک کنید.
