#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate GeoJSON file from Iran cities JSON data
"""

import json
import sys

def load_data():
    """Load Iran cities data"""
    with open('iran_cities.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_geojson():
    """Generate GeoJSON file"""
    data = load_data()
    
    features = []
    
    for province in data:
        for city in province['cities']:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        float(city['longitude']),
                        float(city['latitude'])
                    ]
                },
                "properties": {
                    "id": city['id'],
                    "name": city['name'],
                    "english_name": city.get('english_name', ''),
                    "is_capital": city.get('is_capital', False),
                    "population": city.get('population'),
                    "postal_code": city.get('postal_code'),
                    "province_id": province['id'],
                    "province": province['province'],
                    "province_english": province['english_name'],
                    "phone_code": province['phone_code']
                }
            }
            features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "title": "Iran Cities",
            "description": "Geographic data of Iranian provinces and cities",
            "version": "2.0.0",
            "total_cities": len(features)
        }
    }
    
    with open('iran_cities.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    
    print(f"✅ GeoJSON file generated successfully: iran_cities.geojson ({len(features)} features)")

if __name__ == '__main__':
    print("🔄 Generating GeoJSON file...")
    
    try:
        generate_geojson()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
