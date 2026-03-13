# 🎉 نسخه 2.0.0 - پروژه کامل استان‌ها و شهرهای ایران

## ✨ ویژگی‌های اصلی

### داده‌ها
- ✅ **31 استان** با اطلاعات کامل
- ✅ **883 شهر** با مختصات جغرافیایی دقیق
- ✅ **100%** نام‌های انگلیسی
- ✅ **100%** مراکز استان مشخص
- ✅ **0** خطا در اعتبارسنجی

### فرمت‌های خروجی
- 📄 **JSON** - فایل اصلی (241 KB)
- ⚡ **JSON Minified** - نسخه فشرده (148 KB، کاهش 38.8%)
- 🗄️ **SQL** - برای MySQL/PostgreSQL
- 📊 **CSV** - برای Excel
- 🗺️ **GeoJSON** - برای نقشه‌ها

### API Server
- 🚀 Flask API با 6 endpoint
- 🔍 جستجوی پیشرفته
- 🌐 پشتیبانی از CORS
- 📖 مستندات کامل

### برای توسعه‌دهندگان
- 📦 پکیج npm آماده
- 🐍 پکیج PyPI آماده
- 📘 TypeScript definitions
- 🐳 Docker support
- 🧪 تست‌های خودکار
- 📚 مستندات جامع

## 📥 نصب

### npm
```bash
npm install iran-cities-data
```

### Python
```bash
pip install iran-cities
```

### دانلود مستقیم
```bash
curl -O https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json
```

## 🚀 استفاده سریع

### JavaScript
```javascript
const iranCities = require('iran-cities-data');
console.log(iranCities); // تمام استان‌ها و شهرها
```

### Python
```python
import json
with open('iran_cities.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### API Server
```bash
python api_server.py
# سرور روی http://localhost:8000 اجرا می‌شود
```

## 📊 آمار

| مورد | تعداد |
|------|-------|
| استان‌ها | 31 |
| شهرها | 883 |
| فایل‌های پروژه | 67 |
| تست‌ها | 9 (همه پاس) |
| فرمت‌های خروجی | 5 |
| خطوط کد | ~6000 |

## 🔄 تغییرات نسبت به نسخه قبل

### افزوده شده
- ✅ ID یکتا برای تمام استان‌ها و شهرها
- ✅ نام‌های انگلیسی برای تمام شهرها
- ✅ 4 فرمت خروجی جدید (SQL, CSV, GeoJSON, Minified)
- ✅ API Server کامل
- ✅ TypeScript definitions
- ✅ اسکریپت‌های اعتبارسنجی و آمار
- ✅ مستندات کامل دوزبانه
- ✅ تست‌های خودکار
- ✅ Docker support
- ✅ CI/CD با GitHub Actions

### اصلاح شده
- ✅ حذف 12 شهر تکراری
- ✅ اصلاح مختصات اشتباه
- ✅ تعیین مرکز استان هرمزگان

## 📖 مستندات

- [راهنمای کامل (فارسی)](README.fa.md)
- [راهنمای کامل (انگلیسی)](README.md)
- [مستندات API](docs/API.md)
- [راهنمای توسعه](docs/DEVELOPMENT.md)
- [راهنمای شروع سریع](QUICKSTART.md)
- [راهنمای انتشار](PUBLISHING.md)

## 🤝 مشارکت

این پروژه Open Source است و از مشارکت شما استقبال می‌کنیم!

- 🐛 [گزارش باگ](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/issues/new?template=bug_report.md)
- ✨ [درخواست ویژگی](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/issues/new?template=feature_request.md)
- 📝 [اصلاح داده‌ها](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/issues/new?template=data_correction.md)

## 📝 لایسنس

MIT License - استفاده رایگان برای همه!

## 🙏 تشکر

ساخته شده با ❤️ برای جامعه برنامه‌نویسی ایران

---

**نسخه**: 2.0.0  
**تاریخ انتشار**: 2024-01-15  
**وضعیت**: Production Ready ✅
