# 🇮🇷 Complete List of Iranian Provinces and Cities

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Persian](https://img.shields.io/badge/language-Persian-red.svg)](README.fa.md)

The most **complete and professional** dataset of Iranian provinces and cities for developers.

[فارسی](README.fa.md) | English

## ✨ Features

✅ **883 Cities**: All official cities of Iran  
📍 **Geographic Coordinates**: Precise latitude and longitude for each city  
🏛️ **Province Capitals**: Marked with `is_capital` field  
🌍 **Multiple Formats**: JSON, SQL, CSV, and GeoJSON  
⚡ **Minified Version**: Optimized for frontend projects  
🚀 **API Server**: Ready-to-use local API script  
🆔 **Unique IDs**: Every province and city has a unique identifier  
🌐 **English Names**: All provinces and cities have English names  
👥 **Population**: City population data (work in progress)  
📮 **Postal Codes**: City center postal codes (work in progress)

## 📦 Repository Contents

```
├── iran_cities.json          # Main data source (readable & complete)
├── iran_cities.min.json      # Minified version for web
├── iran_cities.sql           # MySQL/PostgreSQL script
├── iran_cities.csv           # Excel-compatible format
├── iran_cities.geojson       # GeoJSON standard format
├── api_server.py             # Simple API server
├── tests/                    # Automated tests
└── docs/                     # Complete documentation
```

## 🚀 Installation & Usage

### 1️⃣ Direct Download

```bash
# Download JSON file
curl -O https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json

# Or with wget
wget https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json
```

### 2️⃣ JavaScript/TypeScript Usage


```javascript
// Fetch from CDN
fetch('https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.min.json')
  .then(response => response.json())
  .then(data => console.log(data));

// Or direct import
import iranCities from './iran_cities.json';
```

### 3️⃣ Python Usage

```python
import json
import requests

# Download from internet
url = 'https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json'
response = requests.get(url)
data = response.json()

# Or read from local file
with open('iran_cities.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

### 4️⃣ SQL Database Usage

```bash
# MySQL
mysql -u username -p database_name < iran_cities.sql

# PostgreSQL
psql -U username -d database_name -f iran_cities.sql
```

### 5️⃣ Run Local API Server

```bash
# Install dependencies
pip install flask flask-cors

# Run server
python api_server.py

# Server runs on port 8000
```

## 📡 API Endpoints

After running `api_server.py`:

```
GET /api/provinces              # List all provinces
GET /api/provinces/:id          # Get specific province
GET /api/cities                 # List all cities
GET /api/cities/:id             # Get specific city
GET /api/search?q=Tehran        # Search cities and provinces
```

## 📊 JSON Data Structure

```json
{
  "id": 1,
  "province": "آذربایجان شرقی",
  "english_name": "East Azerbaijan",
  "phone_code": "041",
  "cities_count": 55,
  "cities": [
    {
      "id": 1,
      "name": "تبریز",
      "english_name": "Tabriz",
      "latitude": "38.0739964",
      "longitude": "46.2961952",
      "is_capital": true,
      "population": 1558693,
      "postal_code": "5138683751"
    }
  ]
}
```

## 🗺️ Using GeoJSON with Maps

```javascript
// With Leaflet
fetch('iran_cities.geojson')
  .then(response => response.json())
  .then(data => {
    L.geoJSON(data, {
      onEachFeature: function(feature, layer) {
        layer.bindPopup(feature.properties.name);
      }
    }).addTo(map);
  });

// With Mapbox
map.addSource('iran-cities', {
  type: 'geojson',
  data: 'iran_cities.geojson'
});
```

## 🧪 Tests

```bash
# Run tests
python -m pytest tests/

# Test uniqueness
python tests/test_uniqueness.py

# Test coordinates validity
python tests/test_coordinates.py
```

## 📈 Statistics

- **31 Provinces**
- **883 Cities**
- **Precise Geographic Coordinates**
- **Provincial Phone Codes**
- **Persian and English Names**

## 🤝 Contributing

We're looking to make this dataset even better! If you have:

- Accurate population data
- City postal codes
- Found errors in the data
- Improvement suggestions

Please submit a **Pull Request** or open an **Issue**.

### Contribution Guide

1. Fork the repository
2. Create a new branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Made with ❤️ for the Iranian developer community

---

**Last Updated**: 2024  
**Version**: 2.0.0  
**Maintainer**: [@MrAlfak](https://github.com/MrAlfak)
