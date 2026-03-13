# 📦 راهنمای انتشار | Publishing Guide

این راهنما مراحل انتشار پکیج در npm و PyPI را توضیح می‌دهد.

## پیش‌نیازها | Prerequisites

### برای npm
```bash
# ثبت‌نام در npm
npm adduser

# یا ورود
npm login
```

### برای PyPI
```bash
# نصب ابزارهای لازم
pip install build twine

# ثبت‌نام در PyPI
# https://pypi.org/account/register/
```

## انتشار در npm

### 1. بررسی نهایی
```bash
# تست پکیج
npm test

# بررسی فایل‌های شامل شده
npm pack --dry-run
```

### 2. بروزرسانی نسخه
```bash
# نسخه patch (2.0.0 -> 2.0.1)
npm version patch

# نسخه minor (2.0.0 -> 2.1.0)
npm version minor

# نسخه major (2.0.0 -> 3.0.0)
npm version major
```

### 3. انتشار
```bash
# انتشار عمومی
npm publish

# انتشار با tag
npm publish --tag beta
```

### 4. تایید
```bash
# نصب از npm
npm install iran-cities-data

# بررسی صفحه npm
# https://www.npmjs.com/package/iran-cities-data
```

## انتشار در PyPI

### 1. بررسی نهایی
```bash
# اجرای تست‌ها
python -m pytest tests/

# اعتبارسنجی داده‌ها
python scripts/validate_data.py
```

### 2. بروزرسانی نسخه
در فایل‌های زیر نسخه را بروز کنید:
- `setup.py` -> `version="2.0.0"`
- `pyproject.toml` -> `version = "2.0.0"`

### 3. ساخت پکیج
```bash
# پاک‌سازی فایل‌های قبلی
rm -rf dist/ build/ *.egg-info

# ساخت پکیج
python -m build
```

### 4. بررسی پکیج
```bash
# بررسی با twine
twine check dist/*
```

### 5. انتشار در TestPyPI (اختیاری)
```bash
# انتشار در TestPyPI
twine upload --repository testpypi dist/*

# نصب از TestPyPI
pip install --index-url https://test.pypi.org/simple/ iran-cities
```

### 6. انتشار در PyPI
```bash
# انتشار نهایی
twine upload dist/*
```

### 7. تایید
```bash
# نصب از PyPI
pip install iran-cities

# بررسی صفحه PyPI
# https://pypi.org/project/iran-cities/
```

## انتشار خودکار با GitHub Actions

### تنظیم Secrets

در تنظیمات GitHub repository:

1. `Settings` -> `Secrets and variables` -> `Actions`
2. اضافه کردن secrets:
   - `NPM_TOKEN`: توکن npm
   - `PYPI_TOKEN`: توکن PyPI

### ایجاد Release

```bash
# ایجاد tag
git tag v2.0.0
git push origin v2.0.0

# یا از GitHub UI
# Releases -> Create a new release
```

پس از ایجاد release، GitHub Actions به طور خودکار:
- پکیج را در npm منتشر می‌کند
- پکیج را در PyPI منتشر می‌کند

## چک‌لیست قبل از انتشار

- [ ] تمام تست‌ها پاس شده‌اند
- [ ] اعتبارسنجی داده‌ها موفق بوده
- [ ] CHANGELOG.md بروز شده
- [ ] نسخه در تمام فایل‌ها یکسان است
- [ ] README.md کامل و بروز است
- [ ] مستندات کامل است
- [ ] فایل‌های غیرضروری در .npmignore هستند
- [ ] LICENSE فایل موجود است

## نسخه‌گذاری | Versioning

از [Semantic Versioning](https://semver.org/) استفاده می‌کنیم:

- **MAJOR** (3.0.0): تغییرات ناسازگار
- **MINOR** (2.1.0): ویژگی‌های جدید سازگار
- **PATCH** (2.0.1): رفع باگ‌ها

## پس از انتشار

### 1. بروزرسانی مستندات
```bash
# بروزرسانی README با لینک‌های جدید
# بروزرسانی CHANGELOG
```

### 2. اطلاع‌رسانی
- توییت کردن
- پست در Reddit
- اطلاع به کاربران

### 3. نظارت
- بررسی download stats
- پاسخ به issues
- بررسی feedback

## مشکلات رایج

### npm publish fails
```bash
# بررسی ورود
npm whoami

# ورود مجدد
npm login
```

### PyPI upload fails
```bash
# بررسی توکن
# بررسی نام پکیج (باید یکتا باشد)
# بررسی نسخه (نباید تکراری باشد)
```

### Version conflict
```bash
# همیشه نسخه را در همه فایل‌ها بروز کنید:
# - package.json
# - setup.py
# - pyproject.toml
```

## منابع

- [npm Publishing Guide](https://docs.npmjs.com/packages-and-modules/contributing-packages-to-the-registry)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**نکته**: همیشه قبل از انتشار، پکیج را در محیط تست بررسی کنید!
