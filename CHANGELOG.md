# 📝 تاریخچه تغییرات | Changelog

تمام تغییرات مهم این پروژه در این فایل مستند می‌شود.

فرمت بر اساس [Keep a Changelog](https://keepachangelog.com/fa/1.0.0/) است.

## [Unreleased]

### Data integrity / منبع داده
- بازسازی دیتاست اصلی از snapshot تقسیمات کشوری **۱۴۰۲** مرکز آمار ایران با منبع mirror پین‌شده.
- پردازش ۱٬۶۵۹ ردیف خام `CODEREC=5` و جداسازی منبع‌محور ۲۰۹ زیرناحیه/منطقه شهری؛ خروجی نهایی **۱٬۴۵۰ شهر مستقل در ۳۱ استان**.
- ثبت `official_code` و `uid` برای همه شهرهای canonical و اضافه‌شدن شهرستان/بخش به ساختار داده.
- ثبت SHA-256 منبع، commit پین‌شده، تعدادها و سیاست refresh در `data/provenance.json`.
- نگهداری audit trail برای ۲۰۹ ردیف کنارگذاشته‌شده در `data/excluded-urban-subareas-1402.json`.
- اصلاح matching داده قدیمی به‌صورت county-aware و single-use برای جلوگیری از reuse یک ID برای دو شهر هم‌نام.
- جداسازی audit عضویت از enrichment؛ `audit_data.py --strict` اکنون منبع/عضویت را gate می‌کند و `--strict-enrichment` برای کیفیت تکمیلی است.
- ثبت وضعیت فعلی enrichment: ۷۰۳ شهر بدون مختصات/نام انگلیسی، ۳۱۹ transliteration ضعیف و یک گروه مختصات تکراری؛ هیچ‌کدام blocker عضویت نیستند.

### Validation / CI
- یکتایی نام شهر در سطح شهرستان و یکتایی سراسری `id`، `uid` و `official_code`.
- تست regression برای زیرناحیه‌های شماره‌دار و نام‌دار، نام‌های همسان در شهرستان‌های متفاوت و enrichment اختیاری.
- CI روی Python 3.10/3.12، strict membership audit، ساخت artifactها، invariantهای ۳۱ استان/۱٬۴۵۰ شهر و Docker smoke-test.
- rebuild منبع ۱۴۰۲ از pushهای عادی جدا و به workflow دستی قابل بازتولید تبدیل شد.

### Formats / runtime
- GeoJSON اکنون فقط زیرمجموعه دارای مختصات معتبر را صادر می‌کند و تعداد رکوردهای بدون مختصات را در metadata گزارش می‌دهد.
- SQL جداگانه MySQL/PostgreSQL با escaping صحیح.
- API نسخه‌بندی‌شده، pagination، جستجوی فارسی نرمال‌شده، CORS opt-in، `/health` و `/api/v1/meta`.
- Docker با Gunicorn و کاربر non-root.

### Licensing
- کد پروژه تحت MIT باقی مانده است.
- دیتاست منبع‌دار ۱۴۰۲ و مشتقات داده‌ای با attribution و متن مجوز GPL-3.0 جداگانه مستند شده‌اند (`DATA_LICENSE.md`, `LICENSE-DATA-GPL-3.0`).

## [2.0.0] - 2024-01-15

### Added
- شناسه‌های عددی، نام انگلیسی، مختصات و فیلدهای enrichment برای دیتاست legacy اولیه.
- JSON/CSV/GeoJSON/SQL generators، Flask API، Docker و workflowهای اولیه.

### Historical note
نسخه ۲.۰ همه ۸۸۳ رکورد legacy را «شهر» معرفی می‌کرد و برخی حذف‌ها را با لیست دستی/فرض‌های ضعیف انجام می‌داد. این فرض‌ها در تغییرات Unreleased جایگزین شده‌اند و نباید به‌عنوان وضعیت فعلی دیتاست تفسیر شوند.

## [1.0.0] - قبل از 2024

- داده‌های اولیه استان‌ها و مکان‌ها، مختصات و کدهای تلفن استانی.

---

**Versioning note:** تغییرات schema/source ممکن است نیازمند انتشار نسخه جدید باشند؛ مصرف‌کنندگان باید `official_code`/`uid` را برای هویت منبع‌دار و `id` عددی را برای سازگاری legacy در نظر بگیرند.
