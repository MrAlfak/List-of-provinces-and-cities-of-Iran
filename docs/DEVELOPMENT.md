# 🛠️ Development Guide | راهنمای توسعه

[فارسی](#فارسی) | [English](#english)

---

## فارسی

### پیش‌نیازها

- Python 3.7+
- pip
- Git

### نصب محیط توسعه

```bash
# Clone repository
git clone https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran.git
cd List-of-provinces-and-cities-of-Iran

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### ساختار پروژه

```
List-of-provinces-and-cities-of-Iran/
├── iran_cities.json          # داده اصلی
├── iran_cities.min.json      # نسخه فشرده
├── iran_cities.sql           # فایل SQL
├── iran_cities.csv           # فایل CSV
├── iran_cities.geojson       # فایل GeoJSON
├── api_server.py             # سرور API
├── requirements.txt          # وابستگی‌های Python
├── package.json              # تنظیمات npm
├── Makefile                  # دستورات make
├── README.md                 # مستندات اصلی
├── README.fa.md              # مستندات فارسی
├── LICENSE                   # مجوز MIT
├── CHANGELOG.md              # تاریخچه تغییرات
├── CONTRIBUTING.md           # راهنمای مشارکت
├── .gitignore                # فایل‌های نادیده گرفته شده
├── scripts/                  # اسکریپت‌های کمکی
│   ├── generate_sql.py
│   ├── generate_csv.py
│   ├── generate_geojson.py
│   ├── generate_minified.py
│   ├── generate_all.py
│   └── fix_and_enhance_data.py
├── tests/                    # تست‌ها
│   ├── test_uniqueness.py
│   └── test_coordinates.py
├── examples/                 # نمونه‌های استفاده
│   ├── index.html
│   ├── example.py
│   ├── example.js
│   └── README.md
└── docs/                     # مستندات
    ├── API.md
    └── DEVELOPMENT.md
```

### دستورات مفید

```bash
# نصب وابستگی‌ها
make install

# اجرای تست‌ها
make test

# تولید تمام فرمت‌ها
make generate

# اجرای API server
make run

# پاک‌سازی فایل‌های تولید شده
make clean
```

### توسعه

#### 1. اضافه کردن شهر جدید

فایل `iran_cities.json` را ویرایش کنید:

```json
{
  "id": 999,
  "name": "نام شهر",
  "english_name": "City Name",
  "latitude": "35.1234567",
  "longitude": "51.1234567",
  "is_capital": false,
  "population": 100000,
  "postal_code": "1234567890"
}
```

#### 2. اجرای تست‌ها

```bash
# تست یکتا بودن
python tests/test_uniqueness.py

# تست مختصات
python tests/test_coordinates.py

# تست همه
python -m pytest tests/ -v
```

#### 3. تولید فایل‌های خروجی

```bash
# تولید همه فرمت‌ها
python scripts/generate_all.py

# یا تک تک
python scripts/generate_sql.py
python scripts/generate_csv.py
python scripts/generate_geojson.py
python scripts/generate_minified.py
```

#### 4. اصلاح و بهبود داده‌ها

```bash
# دانلود، اصلاح و ذخیره داده‌ها
python scripts/fix_and_enhance_data.py
```

### قوانین کدنویسی

#### Python
- از PEP 8 پیروی کنید
- از type hints استفاده کنید
- docstring برای توابع بنویسید
- کامنت‌های فارسی مجاز است

#### JSON
- Indent با 2 space
- UTF-8 encoding
- فیلدها به ترتیب الفبایی
- از `null` برای مقادیر خالی استفاده کنید

#### JavaScript
- از ES6+ استفاده کنید
- camelCase برای متغیرها
- JSDoc برای توابع

### Workflow توسعه

1. **Fork** کنید
2. **Branch** جدید بسازید: `git checkout -b feature/my-feature`
3. تغییرات را اعمال کنید
4. **Test** کنید: `make test`
5. **Commit** کنید: `git commit -m "Add: my feature"`
6. **Push** کنید: `git push origin feature/my-feature`
7. **Pull Request** باز کنید

### Commit Messages

از این فرمت استفاده کنید:

```
Type: Short description

Longer description if needed

Types:
- Add: اضافه کردن ویژگی جدید
- Fix: اصلاح باگ
- Update: بروزرسانی داده‌ها
- Refactor: بازنویسی کد
- Docs: تغییرات مستندات
- Test: اضافه کردن تست
- Style: تغییرات فرمت کد
```

مثال:
```
Add: English names for all cities

- Added english_name field to all cities
- Updated tests to check for english names
- Generated new output files
```

### دیباگ

#### API Server

```bash
# اجرا در حالت debug
python api_server.py

# تست endpoint
curl http://localhost:8000/api/provinces
```

#### تست‌ها

```bash
# اجرا با verbose
python -m pytest tests/ -v -s

# اجرا با coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### بهینه‌سازی

#### فایل JSON

```bash
# فشرده‌سازی
python scripts/generate_minified.py

# بررسی حجم
ls -lh iran_cities*.json
```

#### API Performance

- از caching استفاده کنید
- Response را gzip کنید
- از CDN استفاده کنید

### مشکلات رایج

#### خطای encoding

```python
# همیشه UTF-8 استفاده کنید
with open('file.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

#### خطای import

```bash
# مطمئن شوید virtual environment فعال است
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```

---

## English

### Prerequisites

- Python 3.7+
- pip
- Git

### Development Setup

See Persian section above for detailed instructions.

### Project Structure

See Persian section above.

### Useful Commands

```bash
make install    # Install dependencies
make test       # Run tests
make generate   # Generate all formats
make run        # Run API server
make clean      # Clean generated files
```

### Development Workflow

1. Fork the repository
2. Create a new branch
3. Make changes
4. Run tests
5. Commit changes
6. Push to branch
7. Open Pull Request

### Coding Standards

- Follow PEP 8 for Python
- Use 2-space indentation for JSON
- Write clear commit messages
- Add tests for new features

---

## 📞 Support

- GitHub Issues: [Open an issue](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/issues)
- Discussions: [GitHub Discussions](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/discussions)

## 📝 License

MIT License - see [LICENSE](../LICENSE) file for details.
