# 🤝 راهنمای مشارکت | Contributing Guide

[فارسی](#فارسی) | [English](#english)

---

## فارسی

از اینکه می‌خواهید در این پروژه مشارکت کنید متشکریم! 🙏

### چگونه مشارکت کنیم؟

#### 1. گزارش باگ یا خطا

اگر خطایی در داده‌ها پیدا کردید:
- یک Issue جدید باز کنید
- عنوان واضح و توضیحات کامل بنویسید
- اگر ممکن است، اسکرین‌شات یا مثال ارائه دهید

#### 2. پیشنهاد ویژگی جدید

- ابتدا یک Issue باز کنید و پیشنهاد خود را توضیح دهید
- منتظر بازخورد باشید
- سپس شروع به پیاده‌سازی کنید

#### 3. اصلاح داده‌ها

اگر می‌خواهید داده‌ها را تکمیل یا اصلاح کنید:

```bash
# 1. Fork کنید
# 2. Clone کنید
git clone https://github.com/YOUR_USERNAME/List-of-provinces-and-cities-of-Iran.git

# 3. برنچ جدید بسازید
git checkout -b fix/city-name-correction

# 4. تغییرات را اعمال کنید
# فایل iran_cities.json را ویرایش کنید

# 5. تست‌ها را اجرا کنید
python tests/test_uniqueness.py
python tests/test_coordinates.py

# 6. Commit کنید
git add iran_cities.json
git commit -m "Fix: اصلاح نام شهر تبریز"

# 7. Push کنید
git push origin fix/city-name-correction

# 8. Pull Request باز کنید
```

### استانداردهای داده

#### فرمت JSON

```json
{
  "id": 1,
  "name": "نام شهر",
  "english_name": "City Name",
  "latitude": "38.0739964",
  "longitude": "46.2961952",
  "is_capital": false,
  "population": 1500000,
  "postal_code": "1234567890"
}
```

#### قوانین:
- ✅ نام‌های فارسی باید صحیح و استاندارد باشند
- ✅ نام‌های انگلیسی باید transliteration صحیح باشند
- ✅ مختصات جغرافیایی باید دقیق باشند (7 رقم اعشار)
- ✅ هر استان فقط یک مرکز استان دارد (`is_capital: true`)
- ✅ ID ها باید یکتا باشند

### تست‌ها

قبل از ارسال Pull Request، حتماً تست‌ها را اجرا کنید:

```bash
# تست یکتا بودن
python tests/test_uniqueness.py

# تست مختصات
python tests/test_coordinates.py

# تست همه
python -m pytest tests/
```

### Code Style

- از UTF-8 encoding استفاده کنید
- فایل JSON باید indent با 2 space داشته باشد
- کامنت‌های فارسی در کدهای Python مجاز است

---

## English

Thank you for wanting to contribute to this project! 🙏

### How to Contribute?

#### 1. Report Bugs

If you find errors in the data:
- Open a new Issue
- Write a clear title and complete description
- Provide screenshots or examples if possible

#### 2. Suggest New Features

- First open an Issue and explain your suggestion
- Wait for feedback
- Then start implementation

#### 3. Fix Data

If you want to complete or fix the data:

```bash
# 1. Fork the repository
# 2. Clone it
git clone https://github.com/YOUR_USERNAME/List-of-provinces-and-cities-of-Iran.git

# 3. Create a new branch
git checkout -b fix/city-name-correction

# 4. Make changes
# Edit iran_cities.json file

# 5. Run tests
python tests/test_uniqueness.py
python tests/test_coordinates.py

# 6. Commit
git add iran_cities.json
git commit -m "Fix: Correct Tabriz city name"

# 7. Push
git push origin fix/city-name-correction

# 8. Open Pull Request
```

### Data Standards

#### JSON Format

```json
{
  "id": 1,
  "name": "نام شهر",
  "english_name": "City Name",
  "latitude": "38.0739964",
  "longitude": "46.2961952",
  "is_capital": false,
  "population": 1500000,
  "postal_code": "1234567890"
}
```

#### Rules:
- ✅ Persian names must be correct and standard
- ✅ English names must be proper transliterations
- ✅ Geographic coordinates must be precise (7 decimal places)
- ✅ Each province has only one capital (`is_capital: true`)
- ✅ IDs must be unique

### Tests

Before submitting a Pull Request, make sure to run tests:

```bash
# Test uniqueness
python tests/test_uniqueness.py

# Test coordinates
python tests/test_coordinates.py

# Test all
python -m pytest tests/
```

### Code Style

- Use UTF-8 encoding
- JSON file should be indented with 2 spaces
- Persian comments in Python code are allowed

---

## 📞 Contact

- GitHub Issues: [Open an issue](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/issues)
- Email: [Your email if you want]

Thank you for your contribution! 🎉
