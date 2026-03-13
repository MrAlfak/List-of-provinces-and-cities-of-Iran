#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت اعتبارسنجی داده‌ها
Data Validation Script

این اسکریپت تمام داده‌ها را بررسی و اعتبارسنجی می‌کند.
"""

import json
import sys
from pathlib import Path

def validate_data():
    """اعتبارسنجی کامل داده‌ها"""
    
    print("🔍 شروع اعتبارسنجی داده‌ها...")
    print("🔍 Starting data validation...\n")
    
    errors = []
    warnings = []
    
    # خواندن فایل اصلی
    with open('iran_cities.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ فایل JSON خوانده شد: {len(data)} استان")
    print(f"✅ JSON file loaded: {len(data)} provinces\n")
    
    # بررسی استان‌ها
    province_ids = set()
    province_names = set()
    city_ids = set()
    total_cities = 0
    
    for province in data:
        # بررسی فیلدهای ضروری استان
        required_fields = ['id', 'province', 'english_name', 'phone_code', 'cities_count', 'cities']
        for field in required_fields:
            if field not in province:
                errors.append(f"❌ استان {province.get('province', 'نامشخص')} فاقد فیلد {field} است")
        
        # بررسی ID یکتا
        if province['id'] in province_ids:
            errors.append(f"❌ ID تکراری برای استان: {province['id']}")
        province_ids.add(province['id'])
        
        # بررسی نام یکتا
        if province['province'] in province_names:
            errors.append(f"❌ نام تکراری برای استان: {province['province']}")
        province_names.add(province['province'])
        
        # بررسی تعداد شهرها
        actual_cities = len(province['cities'])
        if province['cities_count'] != actual_cities:
            errors.append(f"❌ تعداد شهرهای {province['province']} نادرست است: {province['cities_count']} != {actual_cities}")
        
        total_cities += actual_cities
        
        # بررسی مرکز استان
        has_capital = False
        for city in province['cities']:
            # بررسی فیلدهای ضروری شهر
            required_city_fields = ['id', 'name', 'english_name', 'latitude', 'longitude', 'is_capital']
            for field in required_city_fields:
                if field not in city:
                    errors.append(f"❌ شهر {city.get('name', 'نامشخص')} فاقد فیلد {field} است")
            
            # بررسی ID یکتا
            if city['id'] in city_ids:
                errors.append(f"❌ ID تکراری برای شهر: {city['id']} ({city['name']})")
            city_ids.add(city['id'])
            
            # بررسی مختصات
            try:
                lat = float(city['latitude'])
                lon = float(city['longitude'])
                
                # بررسی محدوده ایران
                if not (25 <= lat <= 40):
                    warnings.append(f"⚠️ عرض جغرافیایی {city['name']} خارج از محدوده ایران: {lat}")
                if not (44 <= lon <= 64):
                    warnings.append(f"⚠️ طول جغرافیایی {city['name']} خارج از محدوده ایران: {lon}")
            except (ValueError, TypeError):
                errors.append(f"❌ مختصات نامعتبر برای {city['name']}")
            
            # بررسی مرکز استان
            if city.get('is_capital'):
                if has_capital:
                    errors.append(f"❌ استان {province['province']} بیش از یک مرکز دارد")
                has_capital = True
        
        if not has_capital:
            errors.append(f"❌ استان {province['province']} فاقد مرکز است")
    
    # نمایش نتایج
    print(f"📊 آمار کلی:")
    print(f"   - تعداد استان‌ها: {len(data)}")
    print(f"   - تعداد شهرها: {total_cities}")
    print(f"   - ID های یکتا استان: {len(province_ids)}")
    print(f"   - ID های یکتا شهر: {len(city_ids)}\n")
    
    print(f"📊 Statistics:")
    print(f"   - Provinces: {len(data)}")
    print(f"   - Cities: {total_cities}")
    print(f"   - Unique province IDs: {len(province_ids)}")
    print(f"   - Unique city IDs: {len(city_ids)}\n")
    
    # نمایش خطاها
    if errors:
        print(f"❌ تعداد خطاها: {len(errors)}")
        print(f"❌ Errors found: {len(errors)}\n")
        for error in errors[:10]:  # نمایش 10 خطای اول
            print(f"   {error}")
        if len(errors) > 10:
            print(f"   ... و {len(errors) - 10} خطای دیگر")
        print()
    else:
        print("✅ هیچ خطایی یافت نشد!")
        print("✅ No errors found!\n")
    
    # نمایش هشدارها
    if warnings:
        print(f"⚠️ تعداد هشدارها: {len(warnings)}")
        print(f"⚠️ Warnings found: {len(warnings)}\n")
        for warning in warnings[:10]:  # نمایش 10 هشدار اول
            print(f"   {warning}")
        if len(warnings) > 10:
            print(f"   ... و {len(warnings) - 10} هشدار دیگر")
        print()
    else:
        print("✅ هیچ هشداری یافت نشد!")
        print("✅ No warnings found!\n")
    
    # نتیجه نهایی
    if errors:
        print("❌ اعتبارسنجی ناموفق بود!")
        print("❌ Validation failed!")
        return False
    else:
        print("✅ اعتبارسنجی با موفقیت انجام شد!")
        print("✅ Validation successful!")
        return True

if __name__ == '__main__':
    success = validate_data()
    sys.exit(0 if success else 1)
