# 🚀 شروع سریع | Quick Start

## نصب و استفاده در 3 دقیقه!

### 1️⃣ دانلود فایل JSON

```bash
curl -O https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json
```

### 2️⃣ استفاده در JavaScript

```javascript
fetch('iran_cities.json')
  .then(response => response.json())
  .then(data => {
    console.log(`تعداد استان‌ها: ${data.length}`);
    console.log(`اولین استان: ${data[0].province}`);
  });
```

### 3️⃣ استفاده در Python

```python
import json

with open('iran_cities.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"تعداد استان‌ها: {len(data)}")
print(f"اولین استان: {data[0]['province']}")
```

### 4️⃣ اجرای API Server

```bash
pip install flask flask-cors
python api_server.py
```

سپس مرورگر را باز کنید: http://localhost:8000

### 5️⃣ نمایش روی نقشه

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>
<body>
    <div id="map" style="height: 600px;"></div>
    <script>
        const map = L.map('map').setView([32.4279, 53.6880], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        
        fetch('iran_cities.geojson')
            .then(response => response.json())
            .then(data => {
                L.geoJSON(data, {
                    onEachFeature: (feature, layer) => {
                        layer.bindPopup(feature.properties.name);
                    }
                }).addTo(map);
            });
    </script>
</body>
</html>
```

## 📚 مستندات کامل

- [README فارسی](README.fa.md)
- [README English](README.md)
- [مستندات API](docs/API.md)
- [راهنمای توسعه](docs/DEVELOPMENT.md)
- [نمونه‌های بیشتر](examples/README.md)

## 🎯 موارد استفاده رایج

### دریافت لیست استان‌ها

```javascript
const provinces = data.map(p => ({
    id: p.id,
    name: p.province,
    englishName: p.english_name
}));
```

### جستجوی شهر

```javascript
function findCity(cityName) {
    for (const province of data) {
        const city = province.cities.find(c => 
            c.name.includes(cityName)
        );
        if (city) {
            return {
                city: city.name,
                province: province.province,
                coordinates: {
                    lat: city.latitude,
                    lon: city.longitude
                }
            };
        }
    }
    return null;
}

const tehran = findCity('تهران');
console.log(tehran);
```

### دریافت مراکز استان‌ها

```javascript
const capitals = data.map(province => {
    const capital = province.cities.find(c => c.is_capital);
    return {
        province: province.province,
        capital: capital.name,
        phoneCode: province.phone_code
    };
});
```

## 💡 نکات مهم

1. **برای production از نسخه minified استفاده کنید:**
   ```
   iran_cities.min.json (148 KB)
   ```

2. **برای نقشه از GeoJSON استفاده کنید:**
   ```
   iran_cities.geojson
   ```

3. **برای دیتابیس از SQL استفاده کنید:**
   ```
   iran_cities.sql
   ```

4. **برای Excel از CSV استفاده کنید:**
   ```
   iran_cities.csv
   ```

## 🤝 کمک و پشتیبانی

- [گزارش مشکل](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/issues)
- [راهنمای مشارکت](CONTRIBUTING.md)
- [تاریخچه تغییرات](CHANGELOG.md)

---

**موفق باشید! 🎉**
