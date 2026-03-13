# iran-cities-data

Complete list of Iranian provinces and cities with geographic coordinates.

## Installation

```bash
npm install iran-cities-data
```

## Usage

### JavaScript/Node.js

```javascript
const iranCities = require('iran-cities-data');

// Get all provinces
console.log(iranCities);

// Find a specific province
const tehran = iranCities.find(p => p.english_name === 'Tehran');
console.log(tehran);

// Get all cities from a province
const cities = tehran.cities;
console.log(cities);

// Search for a city
const tabriz = iranCities
  .flatMap(p => p.cities)
  .find(c => c.english_name === 'Tabriz');
console.log(tabriz);
```

### TypeScript

```typescript
import iranCities, { Province, City } from 'iran-cities-data';

const provinces: Province[] = iranCities;

// Type-safe access
const province: Province = provinces[0];
const city: City = province.cities[0];
```

### Browser (ES6)

```javascript
import iranCities from 'iran-cities-data';

// Use in your app
const provinces = iranCities;
```

## Data Structure

```typescript
interface City {
  id: number;
  name: string;              // Persian name
  english_name: string;
  latitude: string;
  longitude: string;
  is_capital: boolean;
  population: number | null;
  postal_code: string | null;
}

interface Province {
  id: number;
  province: string;          // Persian name
  english_name: string;
  phone_code: string;
  cities_count: number;
  cities: City[];
}
```

## Features

- ✅ 31 Provinces
- ✅ 883 Cities
- ✅ Geographic coordinates for all cities
- ✅ Persian and English names
- ✅ Province capitals marked
- ✅ TypeScript definitions included
- ✅ Zero dependencies

## Available Formats

This package includes multiple data formats:

- `iran_cities.json` - Full readable JSON (241 KB)
- `iran_cities.min.json` - Minified JSON (148 KB)
- `iran_cities.sql` - SQL script for MySQL/PostgreSQL
- `iran_cities.csv` - CSV format for Excel
- `iran_cities.geojson` - GeoJSON for mapping

## Examples

### Get all province names

```javascript
const provinceNames = iranCities.map(p => p.english_name);
console.log(provinceNames);
```

### Get all capital cities

```javascript
const capitals = iranCities.map(p => 
  p.cities.find(c => c.is_capital)
);
console.log(capitals);
```

### Search cities by name

```javascript
function searchCity(query) {
  return iranCities
    .flatMap(p => p.cities)
    .filter(c => 
      c.name.includes(query) || 
      c.english_name.toLowerCase().includes(query.toLowerCase())
    );
}

const results = searchCity('Tehran');
console.log(results);
```

### Get cities in a specific area

```javascript
function getCitiesInArea(minLat, maxLat, minLon, maxLon) {
  return iranCities
    .flatMap(p => p.cities)
    .filter(c => {
      const lat = parseFloat(c.latitude);
      const lon = parseFloat(c.longitude);
      return lat >= minLat && lat <= maxLat && 
             lon >= minLon && lon <= maxLon;
    });
}

// Get cities in northern Iran
const northernCities = getCitiesInArea(35, 40, 44, 64);
console.log(northernCities);
```

## License

MIT

## Links

- [GitHub Repository](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran)
- [Documentation](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/blob/main/docs/API.md)
- [Report Issues](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/issues)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](https://github.com/MrAlfak/List-of-provinces-and-cities-of-Iran/blob/main/CONTRIBUTING.md) for details.
