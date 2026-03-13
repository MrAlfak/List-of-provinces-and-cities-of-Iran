#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test validity of geographic coordinates in Iran cities data
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Iran's approximate geographic boundaries
IRAN_BOUNDS = {
    'lat_min': 25.0,  # Southern border
    'lat_max': 40.0,  # Northern border
    'lon_min': 44.0,  # Western border
    'lon_max': 64.0   # Eastern border
}

def load_data():
    """Load Iran cities data"""
    with open('iran_cities.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def test_coordinates_format():
    """Test that all coordinates are valid numbers"""
    data = load_data()
    errors = []
    
    for province in data:
        for city in province['cities']:
            try:
                lat = float(city['latitude'])
                lon = float(city['longitude'])
            except (ValueError, KeyError) as e:
                errors.append(f"{city['name']} in {province['province']}: {e}")
    
    assert len(errors) == 0, f"Invalid coordinate formats:\n" + "\n".join(errors)
    print("✅ All coordinates have valid format")

def test_coordinates_in_iran():
    """Test that all coordinates are within Iran's boundaries"""
    data = load_data()
    errors = []
    
    for province in data:
        for city in province['cities']:
            lat = float(city['latitude'])
            lon = float(city['longitude'])
            
            if not (IRAN_BOUNDS['lat_min'] <= lat <= IRAN_BOUNDS['lat_max']):
                errors.append(f"{city['name']}: latitude {lat} out of bounds")
            
            if not (IRAN_BOUNDS['lon_min'] <= lon <= IRAN_BOUNDS['lon_max']):
                errors.append(f"{city['name']}: longitude {lon} out of bounds")
    
    assert len(errors) == 0, f"Coordinates out of Iran's boundaries:\n" + "\n".join(errors)
    print("✅ All coordinates are within Iran's boundaries")

def test_duplicate_coordinates():
    """Test for cities with identical coordinates"""
    data = load_data()
    coord_map = {}
    duplicates = []
    
    for province in data:
        for city in province['cities']:
            coord = (city['latitude'], city['longitude'])
            
            if coord in coord_map:
                duplicates.append(
                    f"{city['name']} ({province['province']}) has same coordinates as "
                    f"{coord_map[coord]['name']} ({coord_map[coord]['province']})"
                )
            else:
                coord_map[coord] = {
                    'name': city['name'],
                    'province': province['province']
                }
    
    if duplicates:
        print("⚠️  Warning: Cities with duplicate coordinates:")
        for dup in duplicates:
            print(f"   {dup}")
    else:
        print("✅ No duplicate coordinates found")

def test_capital_coordinates():
    """Test that each province has exactly one capital"""
    data = load_data()
    errors = []
    
    for province in data:
        capitals = [c for c in province['cities'] if c.get('is_capital', False)]
        
        if len(capitals) == 0:
            errors.append(f"{province['province']} has no capital city")
        elif len(capitals) > 1:
            capital_names = [c['name'] for c in capitals]
            errors.append(f"{province['province']} has multiple capitals: {capital_names}")
    
    assert len(errors) == 0, "Capital city errors:\n" + "\n".join(errors)
    print("✅ Each province has exactly one capital")

if __name__ == '__main__':
    print("🧪 Running coordinate tests...\n")
    
    try:
        test_coordinates_format()
        test_coordinates_in_iran()
        test_duplicate_coordinates()
        test_capital_coordinates()
        
        print("\n✅ All coordinate tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
