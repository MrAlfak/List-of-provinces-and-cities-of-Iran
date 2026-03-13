/**
 * Example usage of Iran Cities data in JavaScript/Node.js
 */

const fs = require('fs');

// Method 1: Load from local file (Node.js)
function loadFromFile() {
    const data = fs.readFileSync('../iran_cities.json', 'utf8');
    return JSON.parse(data);
}

// Method 2: Load from URL (Browser/Node.js with fetch)
async function loadFromURL() {
    const url = 'https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json';
    const response = await fetch(url);
    return await response.json();
}

// Example 1: Get all provinces
function getProvinces(data) {
    return data.map(p => ({
        id: p.id,
        name: p.province,
        englishName: p.english_name,
        citiesCount: p.cities_count
    }));
}

// Example 2: Find a province by name
function findProvince(data, name) {
    return data.find(p => 
        p.province.toLowerCase().includes(name.toLowerCase()) ||
        p.english_name.toLowerCase().includes(name.toLowerCase())
    );
}

// Example 3: Get all cities in a province
function getCitiesInProvince(data, provinceName) {
    const province = findProvince(data, provinceName);
    return province ? province.cities : [];
}

// Example 4: Find a city by name
function findCity(data, cityName) {
    const results = [];
    
    data.forEach(province => {
        province.cities.forEach(city => {
            if (city.name.toLowerCase().includes(cityName.toLowerCase()) ||
                (city.english_name && city.english_name.toLowerCase().includes(cityName.toLowerCase()))) {
                results.push({
                    city: city.name,
                    englishName: city.english_name,
                    province: province.province,
                    coordinates: {
                        lat: parseFloat(city.latitude),
                        lon: parseFloat(city.longitude)
                    },
                    isCapital: city.is_capital || false
                });
            }
        });
    });
    
    return results;
}

// Example 5: Get all capital cities
function getCapitals(data) {
    const capitals = [];
    
    data.forEach(province => {
        const capital = province.cities.find(c => c.is_capital);
        if (capital) {
            capitals.push({
                city: capital.name,
                englishName: capital.english_name,
                province: province.province,
                phoneCode: province.phone_code
            });
        }
    });
    
    return capitals;
}

// Example 6: Calculate distance between two cities
function calculateDistance(city1, city2) {
    const R = 6371; // Earth's radius in km
    
    const lat1 = parseFloat(city1.latitude) * Math.PI / 180;
    const lat2 = parseFloat(city2.latitude) * Math.PI / 180;
    const dLat = lat2 - lat1;
    const dLon = (parseFloat(city2.longitude) - parseFloat(city1.longitude)) * Math.PI / 180;
    
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1) * Math.cos(lat2) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    
    return R * c;
}

// Example 7: Group cities by province
function groupCitiesByProvince(data) {
    const grouped = {};
    
    data.forEach(province => {
        grouped[province.province] = province.cities.map(c => c.name);
    });
    
    return grouped;
}

// Example 8: Get statistics
function getStatistics(data) {
    const totalCities = data.reduce((sum, p) => sum + p.cities_count, 0);
    const avgCitiesPerProvince = totalCities / data.length;
    
    const provinceWithMostCities = data.reduce((max, p) => 
        p.cities_count > max.cities_count ? p : max
    );
    
    return {
        totalProvinces: data.length,
        totalCities: totalCities,
        avgCitiesPerProvince: avgCitiesPerProvince.toFixed(2),
        provinceWithMostCities: {
            name: provinceWithMostCities.province,
            count: provinceWithMostCities.cities_count
        }
    };
}

// Main example
function main() {
    console.log('🇮🇷 Iran Cities Data - JavaScript Examples\n');
    
    // Load data
    console.log('📥 Loading data...');
    const data = loadFromFile();
    console.log(`✅ Loaded ${data.length} provinces\n`);
    
    // Example 1: List provinces
    console.log('📋 All Provinces:');
    const provinces = getProvinces(data);
    provinces.slice(0, 5).forEach(p => {
        console.log(`  ${p.id}. ${p.name} (${p.englishName}) - ${p.citiesCount} cities`);
    });
    console.log(`  ... and ${provinces.length - 5} more\n`);
    
    // Example 2: Find Tehran province
    console.log('🔍 Finding Tehran province:');
    const tehran = findProvince(data, 'تهران');
    if (tehran) {
        console.log(`  Found: ${tehran.province} with ${tehran.cities_count} cities\n`);
    }
    
    // Example 3: Get cities in Tehran
    console.log('🏙️ Cities in Tehran province:');
    const cities = getCitiesInProvince(data, 'تهران');
    cities.slice(0, 5).forEach(city => {
        const capital = city.is_capital ? '⭐' : '  ';
        console.log(`  ${capital} ${city.name}`);
    });
    console.log(`  ... and ${cities.length - 5} more\n`);
    
    // Example 4: Find cities
    console.log('🔍 Searching for "اصفهان":');
    const results = findCity(data, 'اصفهان');
    results.forEach(r => {
        console.log(`  ${r.city} in ${r.province}`);
        console.log(`    Coordinates: ${r.coordinates.lat}, ${r.coordinates.lon}\n`);
    });
    
    // Example 5: List capitals
    console.log('⭐ Provincial Capitals:');
    const capitals = getCapitals(data);
    capitals.slice(0, 5).forEach(cap => {
        console.log(`  ${cap.city} (${cap.province}) - Phone: ${cap.phoneCode}`);
    });
    console.log(`  ... and ${capitals.length - 5} more\n`);
    
    // Example 6: Statistics
    console.log('📊 Statistics:');
    const stats = getStatistics(data);
    console.log(`  Total Provinces: ${stats.totalProvinces}`);
    console.log(`  Total Cities: ${stats.totalCities}`);
    console.log(`  Average Cities per Province: ${stats.avgCitiesPerProvince}`);
    console.log(`  Province with Most Cities: ${stats.provinceWithMostCities.name} (${stats.provinceWithMostCities.count})\n`);
    
    console.log('✅ Examples completed!');
}

// Run if executed directly
if (require.main === module) {
    main();
}

// Export functions for use in other modules
module.exports = {
    loadFromFile,
    loadFromURL,
    getProvinces,
    findProvince,
    getCitiesInProvince,
    findCity,
    getCapitals,
    calculateDistance,
    groupCitiesByProvince,
    getStatistics
};
