# لیست استان‌ها و شهرهای ایران (Iran Provinces and Cities)

این مخزن شامل لیست جامع و به‌روز استان‌ها و شهرهای ایران در قالب فرمت‌های استاندارد JSON و CSV است.

## ویژگی‌ها (Features)
- ✅ **لیست کامل**: شامل ۳۱ استان و تمامی شهرهای مهم.
- 🌍 **دو زبانه**: نام انگلیسی هر استان برای استفاده در Slug و API.
- ☎️ **اطلاعات مخابراتی**: پیش‌شماره تلفن هر استان.
- 📂 **فرمت‌های متنوع**: ارائه داده‌ها در قالب JSON و CSV.

## محتویات (Contents)
- **iran_cities.json**: منبع اصلی داده‌ها به فرمت JSON.
- **iran_cities.csv**: نسخه CSV داده‌ها برای استفاده در دیتابیس و اکسل.

## ساختار داده JSON
```json
{
  "province": "نام استان",
  "english_name": "Province Name",
  "phone_code": "0XX",
  "cities": ["شهر ۱", "شهر ۲"]
}
```

## نحوه استفاده در JavaScript
```javascript
const data = require('./iran_cities.json');
const tehran = data.find(p => p.english_name === 'Tehran');
console.log(`پیش‌شماره تهران: ${tehran.phone_code}`);
```

## مشارکت (Contribution)
اگر شهر یا اطلاعاتی نیاز به اصلاح دارد، خوشحال می‌شویم با ارسال یک Pull Request کمک کنید.
