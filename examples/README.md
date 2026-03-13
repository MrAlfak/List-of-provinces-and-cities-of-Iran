# 📚 Examples | نمونه‌ها

این پوشه شامل نمونه‌های استفاده از داده‌های استان‌ها و شهرهای ایران در زبان‌های مختلف است.

## 📁 فایل‌ها

### 1. `index.html`
یک صفحه وب تعاملی برای نمایش استان‌ها و شهرها

**نحوه استفاده:**
```bash
# فقط فایل را در مرورگر باز کنید
open index.html
```

**ویژگی‌ها:**
- نمایش تمام استان‌ها
- جستجوی زنده
- نمایش شهرهای هر استان
- طراحی زیبا و ریسپانسیو

### 2. `example.py`
نمونه‌های استفاده در Python

**نحوه استفاده:**
```bash
cd examples
python example.py
```

**توابع موجود:**
- `load_from_file()` - بارگذاری از فایل محلی
- `load_from_github()` - بارگذاری از GitHub
- `get_provinces()` - دریافت لیست استان‌ها
- `find_province()` - جستجوی استان
- `get_cities_in_province()` - دریافت شهرهای یک استان
- `find_city()` - جستجوی شهر
- `get_capitals()` - دریافت مراکز استان‌ها
- `calculate_distance()` - محاسبه فاصله بین دو شهر

### 3. `example.js`
نمونه‌های استفاده در JavaScript/Node.js

**نحوه استفاده:**
```bash
cd examples
node example.js
```

**توابع موجود:**
- `loadFromFile()` - بارگذاری از فایل محلی
- `loadFromURL()` - بارگذاری از URL
- `getProvinces()` - دریافت لیست استان‌ها
- `findProvince()` - جستجوی استان
- `getCitiesInProvince()` - دریافت شهرهای یک استان
- `findCity()` - جستجوی شهر
- `getCapitals()` - دریافت مراکز استان‌ها
- `calculateDistance()` - محاسبه فاصله
- `groupCitiesByProvince()` - گروه‌بندی شهرها
- `getStatistics()` - آمار کلی

## 🎯 موارد استفاده

### استفاده در React

```jsx
import React, { useState, useEffect } from 'react';

function IranCities() {
  const [provinces, setProvinces] = useState([]);
  
  useEffect(() => {
    fetch('https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json')
      .then(res => res.json())
      .then(data => setProvinces(data));
  }, []);
  
  return (
    <div>
      {provinces.map(province => (
        <div key={province.id}>
          <h2>{province.province}</h2>
          <p>{province.cities_count} شهر</p>
        </div>
      ))}
    </div>
  );
}
```

### استفاده در Vue.js

```vue
<template>
  <div>
    <div v-for="province in provinces" :key="province.id">
      <h2>{{ province.province }}</h2>
      <p>{{ province.cities_count }} شهر</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      provinces: []
    };
  },
  mounted() {
    fetch('https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json')
      .then(res => res.json())
      .then(data => this.provinces = data);
  }
};
</script>
```

### استفاده در PHP

```php
<?php
$json = file_get_contents('iran_cities.json');
$data = json_decode($json, true);

foreach ($data as $province) {
    echo $province['province'] . " - " . $province['cities_count'] . " شهر\n";
    
    foreach ($province['cities'] as $city) {
        echo "  - " . $city['name'] . "\n";
    }
}
?>
```

### استفاده در C#

```csharp
using System;
using System.IO;
using Newtonsoft.Json;

class Program
{
    static void Main()
    {
        string json = File.ReadAllText("iran_cities.json");
        var data = JsonConvert.DeserializeObject<List<Province>>(json);
        
        foreach (var province in data)
        {
            Console.WriteLine($"{province.Province} - {province.CitiesCount} شهر");
        }
    }
}
```

## 🗺️ استفاده با نقشه

### Leaflet

```javascript
// بارگذاری GeoJSON
fetch('iran_cities.geojson')
  .then(response => response.json())
  .then(data => {
    L.geoJSON(data, {
      pointToLayer: function(feature, latlng) {
        return L.circleMarker(latlng, {
          radius: feature.properties.is_capital ? 8 : 5,
          fillColor: feature.properties.is_capital ? '#ff0000' : '#0000ff',
          color: '#fff',
          weight: 1,
          opacity: 1,
          fillOpacity: 0.8
        });
      },
      onEachFeature: function(feature, layer) {
        layer.bindPopup(`
          <b>${feature.properties.name}</b><br>
          ${feature.properties.province}<br>
          ${feature.properties.is_capital ? '⭐ مرکز استان' : ''}
        `);
      }
    }).addTo(map);
  });
```

### Google Maps

```javascript
fetch('iran_cities.json')
  .then(response => response.json())
  .then(data => {
    data.forEach(province => {
      province.cities.forEach(city => {
        const marker = new google.maps.Marker({
          position: {
            lat: parseFloat(city.latitude),
            lng: parseFloat(city.longitude)
          },
          map: map,
          title: city.name,
          icon: city.is_capital ? 'star.png' : 'circle.png'
        });
      });
    });
  });
```

## 💡 نکات

1. برای استفاده در production، فایل minified را استفاده کنید
2. داده‌ها را cache کنید تا بارگذاری سریع‌تر شود
3. برای جستجوی سریع، از index استفاده کنید
4. برای نمایش روی نقشه، از فایل GeoJSON استفاده کنید

## 🤝 مشارکت

اگر نمونه کد جالبی دارید، لطفاً Pull Request بفرستید!
