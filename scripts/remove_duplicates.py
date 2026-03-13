#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove duplicate cities from Iran cities data
"""

import json

def remove_duplicates():
    """Remove duplicate cities"""
    print("🔄 Removing duplicate cities...")
    
    with open('iran_cities.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    duplicates_to_remove = [
        ("تهران", "اسلام شهر"),  # Keep اسلام‌شهر
        ("بوشهر", "بندر بوشهر"),  # Keep بوشهر
        ("بوشهر", "دیر"),  # Keep بندر دیر
        ("خراسان جنوبی", "قائنات"),  # Keep قائن
        ("خوزستان", "چمران"),  # Keep هفتگل
        ("فارس", "نورآباد ممسنی"),  # Keep نورآباد
        ("قزوین", "الوند"),  # Keep قزوین
        ("مازندران", "امیرکلا"),  # Keep امیرشهر
        ("مرکزی", "مأمونیه"),  # Keep زرندیه
        ("کهگیلویه و بویراحمد", "گچساران"),  # Keep دوگنبدان
        ("گلستان", "گلستان"),  # This is tricky - different province
        ("گیلان", "هشتپر"),  # Keep تالش
    ]
    
    removed_count = 0
    
    for province in data:
        cities_to_keep = []
        removed_in_province = []
        
        for city in province['cities']:
            # Check if this city should be removed
            should_remove = False
            
            for dup_province, dup_city in duplicates_to_remove:
                if province['province'] == dup_province and city['name'] == dup_city:
                    should_remove = True
                    removed_in_province.append(city['name'])
                    break
            
            if not should_remove:
                cities_to_keep.append(city)
            else:
                removed_count += 1
        
        province['cities'] = cities_to_keep
        province['cities_count'] = len(cities_to_keep)
        
        if removed_in_province:
            print(f"  ✅ {province['province']}: Removed {removed_in_province}")
    
    # Save
    with open('iran_cities.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Removed {removed_count} duplicate cities")
    
    # Update total count
    total_cities = sum(p['cities_count'] for p in data)
    print(f"📊 Total cities now: {total_cities}")

if __name__ == '__main__':
    remove_duplicates()
