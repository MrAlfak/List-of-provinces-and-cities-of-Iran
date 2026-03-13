#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate CSV file from Iran cities JSON data
"""

import json
import csv
import sys

def load_data():
    """Load Iran cities data"""
    with open('iran_cities.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_csv():
    """Generate CSV file"""
    data = load_data()
    
    # Prepare rows
    rows = []
    
    for province in data:
        for city in province['cities']:
            rows.append({
                'city_id': city['id'],
                'city_name': city['name'],
                'city_english_name': city.get('english_name', ''),
                'latitude': city['latitude'],
                'longitude': city['longitude'],
                'is_capital': 'Yes' if city.get('is_capital', False) else 'No',
                'population': city.get('population', ''),
                'postal_code': city.get('postal_code', ''),
                'province_id': province['id'],
                'province_name': province['province'],
                'province_english_name': province['english_name'],
                'phone_code': province['phone_code']
            })
    
    # Write CSV
    with open('iran_cities.csv', 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = [
            'city_id', 'city_name', 'city_english_name', 
            'latitude', 'longitude', 'is_capital',
            'population', 'postal_code',
            'province_id', 'province_name', 'province_english_name', 'phone_code'
        ]
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ CSV file generated successfully: iran_cities.csv ({len(rows)} cities)")

if __name__ == '__main__':
    print("🔄 Generating CSV file...")
    
    try:
        generate_csv()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
