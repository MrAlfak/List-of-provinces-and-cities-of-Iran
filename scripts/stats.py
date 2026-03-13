#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت نمایش آمار
Statistics Display Script

این اسکریپت آمار کامل داده‌ها را نمایش می‌دهد.
"""

import json
from collections import Counter

def show_statistics():
    """نمایش آمار کامل"""
    
    print("📊 آمار کامل داده‌های ایران")
    print("📊 Complete Iran Data Statistics")
    print("=" * 60)
    print()
    
    # خواندن داده‌ها
    with open('iran_cities.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # آمار کلی
    total_provinces = len(data)
    total_cities = sum(p['cities_count'] for p in data)
    
    print(f"🏛️ تعداد کل استان‌ها: {total_provinces}")
    print(f"🏛️ Total Provinces: {total_provinces}")
    print()
    
    print(f"🏙️ تعداد کل شهرها: {total_cities}")
    print(f"🏙️ Total Cities: {total_cities}")
    print()
    
    # استان‌های پرجمعیت‌ترین (از نظر تعداد شهر)
    print("📈 استان‌های دارای بیشترین شهر:")
    print("📈 Provinces with Most Cities:")
    print("-" * 60)
    
    sorted_provinces = sorted(data, key=lambda x: x['cities_count'], reverse=True)
    for i, province in enumerate(sorted_provinces[:10], 1):
        print(f"{i:2d}. {province['province']:20s} ({province['english_name']:20s}): {province['cities_count']:3d} شهر")
    print()
    
    # استان‌های کم‌جمعیت‌ترین (از نظر تعداد شهر)
    print("📉 استان‌های دارای کمترین شهر:")
    print("📉 Provinces with Least Cities:")
    print("-" * 60)
    
    for i, province in enumerate(sorted_provinces[-10:], 1):
        print(f"{i:2d}. {province['province']:20s} ({province['english_name']:20s}): {province['cities_count']:3d} شهر")
    print()
    
    # آمار کدهای تلفن
    phone_codes = Counter(p['phone_code'] for p in data)
    print(f"📞 تعداد کدهای تلفن یکتا: {len(phone_codes)}")
    print(f"📞 Unique Phone Codes: {len(phone_codes)}")
    print()
    
    # آمار نام‌های انگلیسی
    cities_with_english = 0
    for province in data:
        for city in province['cities']:
            if city.get('english_name'):
                cities_with_english += 1
    
    print(f"🌐 شهرهای دارای نام انگلیسی: {cities_with_english} از {total_cities} ({cities_with_english/total_cities*100:.1f}%)")
    print(f"🌐 Cities with English Names: {cities_with_english} of {total_cities} ({cities_with_english/total_cities*100:.1f}%)")
    print()
    
    # آمار مراکز استان
    capitals = sum(1 for p in data for c in p['cities'] if c.get('is_capital'))
    print(f"🏛️ تعداد مراکز استان: {capitals}")
    print(f"🏛️ Province Capitals: {capitals}")
    print()
    
    # آمار مختصات
    cities_with_coords = 0
    for province in data:
        for city in province['cities']:
            if city.get('latitude') and city.get('longitude'):
                cities_with_coords += 1
    
    print(f"📍 شهرهای دارای مختصات: {cities_with_coords} از {total_cities} ({cities_with_coords/total_cities*100:.1f}%)")
    print(f"📍 Cities with Coordinates: {cities_with_coords} of {total_cities} ({cities_with_coords/total_cities*100:.1f}%)")
    print()
    
    # میانگین تعداد شهر در هر استان
    avg_cities = total_cities / total_provinces
    print(f"📊 میانگین تعداد شهر در هر استان: {avg_cities:.1f}")
    print(f"📊 Average Cities per Province: {avg_cities:.1f}")
    print()
    
    print("=" * 60)
    print("✅ آمار با موفقیت نمایش داده شد!")
    print("✅ Statistics displayed successfully!")

if __name__ == '__main__':
    show_statistics()
