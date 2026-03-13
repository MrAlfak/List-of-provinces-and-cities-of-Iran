#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix and enhance Iran cities data
- Add unique IDs
- Add English names
- Fix duplicate names
- Add metadata fields
- Clean up data
"""

import json
import requests
import re

# English transliterations for provinces
PROVINCE_ENGLISH_NAMES = {
    "آذربایجان شرقی": "East Azerbaijan",
    "آذربایجان غربی": "West Azerbaijan",
    "اردبیل": "Ardabil",
    "اصفهان": "Isfahan",
    "البرز": "Alborz",
    "ایلام": "Ilam",
    "بوشهر": "Bushehr",
    "تهران": "Tehran",
    "خراسان جنوبی": "South Khorasan",
    "خراسان رضوی": "Razavi Khorasan",
    "خراسان شمالی": "North Khorasan",
    "خوزستان": "Khuzestan",
    "زنجان": "Zanjan",
    "سمنان": "Semnan",
    "سیستان و بلوچستان": "Sistan and Baluchestan",
    "فارس": "Fars",
    "قزوین": "Qazvin",
    "قم": "Qom",
    "کردستان": "Kurdistan",
    "کرمان": "Kerman",
    "کرمانشاه": "Kermanshah",
    "کهگیلویه و بویراحمد": "Kohgiluyeh and Boyer-Ahmad",
    "گلستان": "Golestan",
    "گیلان": "Gilan",
    "لرستان": "Lorestan",
    "مازندران": "Mazandaran",
    "مرکزی": "Markazi",
    "هرمزگان": "Hormozgan",
    "همدان": "Hamadan",
    "چهارمحال و بختیاری": "Chaharmahal and Bakhtiari",
    "یزد": "Yazd"
}

# Common city name transliterations
CITY_ENGLISH_NAMES = {
    "تهران": "Tehran",
    "مشهد": "Mashhad",
    "اصفهان": "Isfahan",
    "کرج": "Karaj",
    "تبریز": "Tabriz",
    "شیراز": "Shiraz",
    "قم": "Qom",
    "اهواز": "Ahvaz",
    "کرمانشاه": "Kermanshah",
    "ارومیه": "Urmia",
    "رشت": "Rasht",
    "زاهدان": "Zahedan",
    "همدان": "Hamadan",
    "کرمان": "Kerman",
    "یزد": "Yazd",
    "اردبیل": "Ardabil",
    "بندر عباس": "Bandar Abbas",
    "اراک": "Arak",
    "قزوین": "Qazvin",
    "زنجان": "Zanjan",
    "سنندج": "Sanandaj",
    "خرم‌آباد": "Khorramabad",
    "گرگان": "Gorgan",
    "ساری": "Sari",
    "بیرجند": "Birjand",
    "بجنورد": "Bojnord",
    "سبزوار": "Sabzevar",
    "نیشابور": "Neyshabur",
    "بوشهر": "Bushehr",
    "یاسوج": "Yasuj",
    "شهرکرد": "Shahrekord"
}

def download_original_data():
    """Download original data from GitHub"""
    url = 'https://raw.githubusercontent.com/MrAlfak/List-of-provinces-and-cities-of-Iran/main/iran_cities.json'
    print("📥 Downloading original data...")
    response = requests.get(url)
    return response.json()

def clean_city_name(name):
    """Clean city name (remove extra spaces, etc.)"""
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def generate_english_name(persian_name):
    """Generate English transliteration for city name"""
    # Check if we have a predefined translation
    if persian_name in CITY_ENGLISH_NAMES:
        return CITY_ENGLISH_NAMES[persian_name]
    
    # Otherwise, return None (to be filled manually later)
    return None

def fix_and_enhance_data(data):
    """Fix and enhance the data"""
    print("🔧 Fixing and enhancing data...")
    
    province_id = 1
    city_global_id = 1
    
    enhanced_data = []
    
    for province in data:
        # Clean province data
        province_data = {
            "id": province_id,
            "province": province['province'],
            "english_name": PROVINCE_ENGLISH_NAMES.get(province['province'], province.get('english_name', '')),
            "phone_code": province['phone_code'],
            "cities_count": len(province['cities']),
            "last_updated": "2024-01-15",
            "cities": []
        }
        
        # Track city names to avoid duplicates
        seen_cities = set()
        
        for city in province['cities']:
            # Clean city name
            city_name = clean_city_name(city['name'])
            
            # Skip duplicates
            if city_name in seen_cities:
                print(f"  ⚠️  Skipping duplicate: {city_name} in {province['province']}")
                continue
            
            seen_cities.add(city_name)
            
            # Generate English name
            english_name = generate_english_name(city_name)
            
            # Create city data
            city_data = {
                "id": city_global_id,
                "name": city_name,
                "english_name": english_name,
                "latitude": city['latitude'],
                "longitude": city['longitude'],
                "is_capital": city.get('is_capital', False),
                "population": city.get('population'),
                "postal_code": city.get('postal_code')
            }
            
            province_data['cities'].append(city_data)
            city_global_id += 1
        
        # Update cities count
        province_data['cities_count'] = len(province_data['cities'])
        
        enhanced_data.append(province_data)
        province_id += 1
        
        print(f"  ✅ {province['province']}: {province_data['cities_count']} cities")
    
    return enhanced_data

def save_data(data, filename='iran_cities.json'):
    """Save enhanced data to file"""
    print(f"\n💾 Saving to {filename}...")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved successfully!")

def main():
    print("🇮🇷 Iran Cities Data - Fix and Enhance\n")
    
    try:
        # Download original data
        data = download_original_data()
        print(f"✅ Downloaded {len(data)} provinces\n")
        
        # Fix and enhance
        enhanced_data = fix_and_enhance_data(data)
        
        # Save
        save_data(enhanced_data)
        
        # Statistics
        total_cities = sum(p['cities_count'] for p in enhanced_data)
        print(f"\n📊 Statistics:")
        print(f"  Provinces: {len(enhanced_data)}")
        print(f"  Cities: {total_cities}")
        
        print("\n✅ All done!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
