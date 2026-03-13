#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage of Iran Cities data in Python
"""

import json
import requests

# Method 1: Load from local file
def load_from_file():
    """Load data from local JSON file"""
    with open('../iran_cities.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Method 2: Load from GitHub
def load_from_github():
    """Load data from GitHub repository"""
    url = 'https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json'
    response = requests.get(url)
    return response.json()

# Example 1: Get all provinces
def get_provinces(data):
    """Get list of all provinces"""
    provinces = [
        {
            'id': p['id'],
            'name': p['province'],
            'english_name': p['english_name'],
            'cities_count': p['cities_count']
        }
        for p in data
    ]
    return provinces

# Example 2: Find a province by name
def find_province(data, name):
    """Find a province by name"""
    for province in data:
        if name.lower() in province['province'].lower():
            return province
    return None

# Example 3: Get all cities in a province
def get_cities_in_province(data, province_name):
    """Get all cities in a specific province"""
    province = find_province(data, province_name)
    if province:
        return province['cities']
    return []

# Example 4: Find a city by name
def find_city(data, city_name):
    """Find a city by name across all provinces"""
    results = []
    for province in data:
        for city in province['cities']:
            if city_name.lower() in city['name'].lower():
                results.append({
                    'city': city['name'],
                    'province': province['province'],
                    'coordinates': {
                        'lat': city['latitude'],
                        'lon': city['longitude']
                    },
                    'is_capital': city.get('is_capital', False)
                })
    return results

# Example 5: Get all capital cities
def get_capitals(data):
    """Get all provincial capital cities"""
    capitals = []
    for province in data:
        for city in province['cities']:
            if city.get('is_capital', False):
                capitals.append({
                    'city': city['name'],
                    'province': province['province'],
                    'phone_code': province['phone_code']
                })
    return capitals

# Example 6: Calculate distance between two cities
def calculate_distance(city1, city2):
    """Calculate approximate distance between two cities (in km)"""
    from math import radians, sin, cos, sqrt, atan2
    
    lat1, lon1 = float(city1['latitude']), float(city1['longitude'])
    lat2, lon2 = float(city2['latitude']), float(city2['longitude'])
    
    R = 6371  # Earth's radius in km
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

# Main example
if __name__ == '__main__':
    print("🇮🇷 Iran Cities Data - Python Examples\n")
    
    # Load data
    print("📥 Loading data...")
    data = load_from_file()
    print(f"✅ Loaded {len(data)} provinces\n")
    
    # Example 1: List provinces
    print("📋 All Provinces:")
    provinces = get_provinces(data)
    for p in provinces[:5]:  # Show first 5
        print(f"  {p['id']}. {p['name']} ({p['english_name']}) - {p['cities_count']} cities")
    print(f"  ... and {len(provinces) - 5} more\n")
    
    # Example 2: Find Tehran province
    print("🔍 Finding Tehran province:")
    tehran = find_province(data, 'تهران')
    if tehran:
        print(f"  Found: {tehran['province']} with {tehran['cities_count']} cities\n")
    
    # Example 3: Get cities in Tehran
    print("🏙️ Cities in Tehran province:")
    cities = get_cities_in_province(data, 'تهران')
    for city in cities[:5]:  # Show first 5
        capital = "⭐" if city.get('is_capital') else "  "
        print(f"  {capital} {city['name']}")
    print(f"  ... and {len(cities) - 5} more\n")
    
    # Example 4: Find cities named "شیراز"
    print("🔍 Searching for 'شیراز':")
    results = find_city(data, 'شیراز')
    for r in results:
        print(f"  {r['city']} in {r['province']}")
        print(f"    Coordinates: {r['coordinates']['lat']}, {r['coordinates']['lon']}\n")
    
    # Example 5: List all capitals
    print("⭐ Provincial Capitals:")
    capitals = get_capitals(data)
    for cap in capitals[:5]:  # Show first 5
        print(f"  {cap['city']} ({cap['province']}) - Phone: {cap['phone_code']}")
    print(f"  ... and {len(capitals) - 5} more\n")
    
    # Example 6: Calculate distance
    print("📏 Distance calculation:")
    tehran_city = find_city(data, 'تهران')[0]
    shiraz_city = find_city(data, 'شیراز')[0]
    
    # Get full city data
    for province in data:
        for city in province['cities']:
            if city['name'] == 'تهران':
                tehran_full = city
            if city['name'] == 'شیراز':
                shiraz_full = city
    
    distance = calculate_distance(tehran_full, shiraz_full)
    print(f"  Distance between Tehran and Shiraz: {distance:.2f} km\n")
    
    print("✅ Examples completed!")
