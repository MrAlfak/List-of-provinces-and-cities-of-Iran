# 📡 API Documentation | مستندات API

[فارسی](#فارسی) | [English](#english)

---

## فارسی

### راه‌اندازی سرور

```bash
# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای سرور
python api_server.py
```

سرور روی `http://localhost:8000` اجرا می‌شود.

### Endpoints

#### 1. صفحه اصلی
```
GET /
```

**پاسخ:**
```json
{
  "message": "Iran Cities API",
  "version": "2.0.0",
  "endpoints": {
    "provinces": "/api/provinces",
    "province_by_id": "/api/provinces/<id>",
    "cities": "/api/cities",
    "city_by_id": "/api/cities/<id>",
    "search": "/api/search?q=<query>"
  }
}
```

#### 2. لیست استان‌ها
```
GET /api/provinces
```

**پاسخ:**
```json
{
  "success": true,
  "count": 31,
  "data": [
    {
      "id": 1,
      "province": "آذربایجان شرقی",
      "english_name": "East Azerbaijan",
      "phone_code": "041",
      "cities_count": 55
    }
  ]
}
```

#### 3. اطلاعات یک استان
```
GET /api/provinces/:id
```

**مثال:**
```bash
curl http://localhost:8000/api/provinces/1
```

**پاسخ:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "province": "آذربایجان شرقی",
    "english_name": "East Azerbaijan",
    "phone_code": "041",
    "cities_count": 55,
    "cities": [...]
  }
}
```

#### 4. لیست تمام شهرها
```
GET /api/cities
```

**پاسخ:**
```json
{
  "success": true,
  "count": 895,
  "data": [
    {
      "id": 1,
      "name": "تبریز",
      "english_name": "Tabriz",
      "latitude": "38.0739964",
      "longitude": "46.2961952",
      "is_capital": true,
      "province_id": 1,
      "province_name": "آذربایجان شرقی"
    }
  ]
}
```

#### 5. اطلاعات یک شهر
```
GET /api/cities/:id
```

**مثال:**
```bash
curl http://localhost:8000/api/cities/1
```

#### 6. جستجو
```
GET /api/search?q=<query>
```

**مثال:**
```bash
curl http://localhost:8000/api/search?q=تهران
```

**پاسخ:**
```json
{
  "success": true,
  "query": "تهران",
  "results": {
    "provinces": [
      {
        "id": 8,
        "province": "تهران",
        "english_name": "Tehran"
      }
    ],
    "cities": [
      {
        "id": 1,
        "name": "تهران",
        "english_name": "Tehran",
        "province": "تهران"
      }
    ]
  },
  "total": 2
}
```

### کدهای خطا

| کد | توضیح |
|----|-------|
| 200 | موفق |
| 400 | درخواست نامعتبر |
| 404 | یافت نشد |
| 500 | خطای سرور |

### مثال‌های استفاده

#### JavaScript/Fetch
```javascript
// دریافت لیست استان‌ها
fetch('http://localhost:8000/api/provinces')
  .then(response => response.json())
  .then(data => console.log(data));

// جستجو
fetch('http://localhost:8000/api/search?q=اصفهان')
  .then(response => response.json())
  .then(data => console.log(data));
```

#### Python/Requests
```python
import requests

# دریافت لیست شهرها
response = requests.get('http://localhost:8000/api/cities')
data = response.json()
print(data)

# جستجو
response = requests.get('http://localhost:8000/api/search', params={'q': 'شیراز'})
data = response.json()
print(data)
```

#### cURL
```bash
# لیست استان‌ها
curl http://localhost:8000/api/provinces

# اطلاعات استان خاص
curl http://localhost:8000/api/provinces/1

# جستجو
curl "http://localhost:8000/api/search?q=مشهد"
```

---

## English

### Server Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python api_server.py
```

Server runs on `http://localhost:8000`.

### Endpoints

#### 1. Home Page
```
GET /
```

**Response:**
```json
{
  "message": "Iran Cities API",
  "version": "2.0.0",
  "endpoints": {
    "provinces": "/api/provinces",
    "province_by_id": "/api/provinces/<id>",
    "cities": "/api/cities",
    "city_by_id": "/api/cities/<id>",
    "search": "/api/search?q=<query>"
  }
}
```

#### 2. List Provinces
```
GET /api/provinces
```

#### 3. Get Province
```
GET /api/provinces/:id
```

#### 4. List Cities
```
GET /api/cities
```

#### 5. Get City
```
GET /api/cities/:id
```

#### 6. Search
```
GET /api/search?q=<query>
```

### Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Server Error |

### Usage Examples

See Persian section above for detailed examples.

---

## CORS

The API has CORS enabled, so you can call it from any domain.

## Rate Limiting

Currently, there is no rate limiting. For production use, consider adding rate limiting.

## Authentication

Currently, the API is open and doesn't require authentication. For production use, consider adding authentication.
