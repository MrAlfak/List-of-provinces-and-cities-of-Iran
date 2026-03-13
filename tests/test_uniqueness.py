#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test uniqueness of IDs and names in Iran cities data
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_data():
    """Load Iran cities data"""
    with open('iran_cities.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def test_province_id_uniqueness():
    """Test that all province IDs are unique"""
    data = load_data()
    province_ids = [p['id'] for p in data]
    
    assert len(province_ids) == len(set(province_ids)), \
        "Province IDs are not unique!"
    
    print("✅ Province IDs are unique")

def test_province_name_uniqueness():
    """Test that all province names are unique"""
    data = load_data()
    province_names = [p['province'] for p in data]
    
    duplicates = [name for name in province_names if province_names.count(name) > 1]
    
    assert len(province_names) == len(set(province_names)), \
        f"Province names are not unique! Duplicates: {set(duplicates)}"
    
    print("✅ Province names are unique")

def test_city_id_uniqueness():
    """Test that all city IDs are unique within each province"""
    data = load_data()
    
    for province in data:
        city_ids = [c['id'] for c in province['cities']]
        duplicates = [cid for cid in city_ids if city_ids.count(cid) > 1]
        
        assert len(city_ids) == len(set(city_ids)), \
            f"City IDs in {province['province']} are not unique! Duplicates: {set(duplicates)}"
    
    print("✅ City IDs are unique within provinces")

def test_city_name_uniqueness_in_province():
    """Test that city names are unique within each province"""
    data = load_data()
    
    for province in data:
        city_names = [c['name'] for c in province['cities']]
        duplicates = [name for name in city_names if city_names.count(name) > 1]
        
        if duplicates:
            print(f"⚠️  Warning: Duplicate city names in {province['province']}: {set(duplicates)}")
        else:
            print(f"✅ City names in {province['province']} are unique")

def test_cities_count():
    """Test that cities_count matches actual number of cities"""
    data = load_data()
    
    for province in data:
        actual_count = len(province['cities'])
        declared_count = province['cities_count']
        
        assert actual_count == declared_count, \
            f"Cities count mismatch in {province['province']}: declared {declared_count}, actual {actual_count}"
    
    print("✅ All cities counts are correct")

if __name__ == '__main__':
    print("🧪 Running uniqueness tests...\n")
    
    try:
        test_province_id_uniqueness()
        test_province_name_uniqueness()
        test_city_id_uniqueness()
        test_city_name_uniqueness_in_province()
        test_cities_count()
        
        print("\n✅ All uniqueness tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
