# 📝 تاریخچه تغییرات | Changelog

تمام تغییرات مهم این پروژه در این فایل مستند می‌شود.

فرمت بر اساس [Keep a Changelog](https://keepachangelog.com/fa/1.0.0/) است.

## [2.0.0] - 2024-01-15

### ✨ افزوده شده (Added)

#### داده‌ها
- اضافه شدن ID یکتا به تمام استان‌ها و شهرها
- اضافه شدن نام انگلیسی به تمام شهرها (883 شهر)
- اضافه شدن فیلدهای `population` و `postal_code` (برای تکمیل آینده)
- اضافه شدن فیلد `is_capital` برای مشخص کردن مراکز استان

#### فرمت‌های خروجی
- فایل JSON فشرده (`iran_cities.min.json`) با کاهش 38.8% حجم
- فایل SQL برای MySQL/PostgreSQL
- فایل CSV برای Excel
- فایل GeoJSON برای نقشه‌ها

#### API
- سرور Flask با 6 endpoint
- جستجوی پیشرفته در شهرها و استان‌ها
- پشتیبانی از CORS
- مستندات کامل API

#### اسکریپت‌ها
- `scripts/fix_and_enhance_data.py` - دانلود و اصلاح داده‌ها
- `scripts/add_english_names.py` - اضافه کردن نام‌های انگلیسی
- `scripts/remove_duplicates.py` - حذف تکراری‌ها
- `scripts/generate_sql.py` - تولید SQL
- `scripts/generate_csv.py` - تولید CSV
- `scripts/generate_geojson.py` - تولید GeoJSON
- `scripts/generate_minified.py` - تولید نسخه فشرده
- `scripts/generate_all.py` - تولید همه فرمت‌ها
- `scripts/validate_data.py` - اعتبارسنجی داده‌ها
- `scripts/stats.py` - نمایش آمار

#### تست‌ها
- `tests/test_uniqueness.py` - تست یکتا بودن
- `tests/test_coordinates.py` - تست مختصات
- پیکربندی pytest
- CI/CD با GitHub Actions

#### نمونه‌ها
- صفحه HTML تعاملی با نقشه
- نمونه‌های Python کامل
- نمونه‌های JavaScript کامل

#### مستندات
- README دوزبانه (فارسی/انگلیسی)
- راهنمای مشارکت (CONTRIBUTING.md)
- راهنمای توسعه (docs/DEVELOPMENT.md)
- مستندات API (docs/API.md)
- راهنمای شروع سریع (QUICKSTART.md)
- نقشه راه (ROADMAP.md)
- خط‌مشی امنیتی (SECURITY.md)
- قوانین رفتاری (CODE_OF_CONDUCT.md)
- راهنمای انتشار (PUBLISHING.md)
- راهنمای npm (NPM_README.md)
- گزارش نهایی (FINAL_REPORT.md)
- چک‌لیست کامل (COMPLETE_CHECKLIST.md)
- خلاصه پروژه (PROJECT_SUMMARY.md)
- خلاصه نهایی (SUMMARY.md)
- لیست بهبودها (IMPROVEMENTS.md)

#### پیکربندی
- Docker support (Dockerfile, docker-compose.yml)
- TypeScript definitions (index.d.ts)
- تنظیمات npm (package.json بهبود یافته)
- تنظیمات PyPI (setup.py, pyproject.toml)
- Makefile با دستورات کامل
- GitHub Actions برای CI/CD
- GitHub Issue Templates
- GitHub Pull Request Template
- .gitattributes برای line endings
- .npmignore برای npm package
- .dockerignore برای Docker
- MANIFEST.in برای Python package
- CITATION.cff برای استناد علمی

### 🔧 تغییر یافته (Changed)
- بهبود ساختار پروژه
- بهبود مستندات
- بهبود نام‌گذاری فایل‌ها
- بهبود کیفیت کد
- بهبود Makefile با دستورات بیشتر

### 🐛 رفع شده (Fixed)
- اصلاح مختصات اشتباه (مثلاً کفشکنان)
- تعیین مرکز استان هرمزگان (بندر عباس)
- حذف 12 شهر تکراری
- اصلاح تعداد شهرها در README (895 -> 883)

### 🗑️ حذف شده (Removed)
- حذف شهرهای تکراری (12 شهر)

---

## [1.0.0] - قبل از 2024

### ✨ افزوده شده
- داده‌های اولیه استان‌ها و شهرها
- مختصات جغرافیایی
- کدهای تلفن استانی
- فایل JSON اصلی

---

## نوع تغییرات | Types of Changes

- ✨ **افزوده شده (Added)**: ویژگی‌های جدید
- 🔧 **تغییر یافته (Changed)**: تغییرات در ویژگی‌های موجود
- ❌ **منسوخ شده (Deprecated)**: ویژگی‌هایی که به زودی حذف می‌شوند
- 🗑️ **حذف شده (Removed)**: ویژگی‌های حذف شده
- 🐛 **رفع شده (Fixed)**: رفع باگ‌ها
- 🔒 **امنیتی (Security)**: رفع آسیب‌پذیری‌های امنیتی

---

## نسخه‌های آینده | Future Versions

### [2.1.0] - برنامه‌ریزی شده
- [ ] تکمیل جمعیت شهرها
- [ ] اضافه کردن کدهای پستی
- [ ] بررسی و اصلاح نام‌های انگلیسی auto-transliterated
- [ ] اضافه کردن شهرستان‌ها

### [3.0.0] - آینده
- [ ] اضافه کردن روستاها
- [ ] GraphQL API
- [ ] Authentication
- [ ] Rate Limiting
- [ ] Caching
- [ ] Real-time Updates

---

**نکته**: این پروژه از [Semantic Versioning](https://semver.org/) پیروی می‌کند.

**فرمت**: این فایل از [Keep a Changelog](https://keepachangelog.com/) پیروی می‌کند.
