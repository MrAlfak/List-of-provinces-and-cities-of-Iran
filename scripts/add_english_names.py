#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add comprehensive English names to all cities
"""

import json
import re

# Comprehensive city name transliterations
CITY_ENGLISH_NAMES = {
    # استان‌های بزرگ
    "تهران": "Tehran", "مشهد": "Mashhad", "اصفهان": "Isfahan", "کرج": "Karaj",
    "تبریز": "Tabriz", "شیراز": "Shiraz", "قم": "Qom", "اهواز": "Ahvaz",
    "کرمانشاه": "Kermanshah", "ارومیه": "Urmia", "رشت": "Rasht", "زاهدان": "Zahedan",
    "همدان": "Hamadan", "کرمان": "Kerman", "یزد": "Yazd", "اردبیل": "Ardabil",
    "بندر عباس": "Bandar Abbas", "اراک": "Arak", "قزوین": "Qazvin", "زنجان": "Zanjan",
    "سنندج": "Sanandaj", "خرم‌آباد": "Khorramabad", "گرگان": "Gorgan", "ساری": "Sari",
    "بیرجند": "Birjand", "بجنورد": "Bojnord", "یاسوج": "Yasuj", "شهرکرد": "Shahrekord",
    
    # شهرهای مهم
    "سبزوار": "Sabzevar", "نیشابور": "Neyshabur", "بوشهر": "Bushehr",
    "آمل": "Amol", "بابل": "Babol", "قائم‌شهر": "Qaemshahr",
    "گنبد کاووس": "Gonbad-e Kavus", "گنبدکاووس": "Gonbad-e Kavus",
    "بندر انزلی": "Bandar Anzali", "لاهیجان": "Lahijan",
    "ساوه": "Saveh", "خمینی‌شهر": "Khomeyni Shahr",
    "نجف‌آباد": "Najafabad", "کاشان": "Kashan",
    "بروجرد": "Borujerd", "دزفول": "Dezful", "آبادان": "Abadan",
    "خرمشهر": "Khorramshahr", "اندیمشک": "Andimeshk",
    "مراغه": "Maragheh", "میانه": "Mianeh", "مرند": "Marand",
    "بناب": "Bonab", "سراب": "Sarab", "اهر": "Ahar",
    "خوی": "Khoy", "ماکو": "Maku", "مهاباد": "Mahabad",
    "بوکان": "Bukan", "میاندوآب": "Miandoab", "سردشت": "Sardasht",
    "پیرانشهر": "Piranshahr", "نقده": "Naqadeh",
    
    # شهرهای دیگر - الفبایی
    "آباده": "Abadeh", "آبدان": "Abdan", "آبیک": "Abyek",
    "آذرشهر": "Azarshahr", "آستارا": "Astara", "آستانه اشرفیه": "Astaneh Ashrafiyeh",
    "آشتیان": "Ashtian", "آق قلا": "Aq Qala", "آمل": "Amol",
    "ابرکوه": "Abarkuh", "ابهر": "Abhar", "اردستان": "Ardestan",
    "اردکان": "Ardakan", "ارسنجان": "Arsanjan", "ازنا": "Azna",
    "اسدآباد": "Asadabad", "اسفراین": "Esfarayen", "اسلام‌آباد غرب": "Eslamabad-e Gharb",
    "اسلام شهر": "Eslam Shahr", "اسلام‌شهر": "Eslam Shahr",
    "اشتهارد": "Eshtehard", "اشنویه": "Oshnaviyeh", "اصلاندوز": "Aslanduz",
    "اقلید": "Eqlid", "الشتر": "Aleshtar", "الیگودرز": "Aligudarz",
    "امیدیه": "Omidiyeh", "انار": "Anar", "اندیشه": "Andisheh",
    "اهرم": "Ahram", "اوز": "Owz", "ایذه": "Izeh",
    "ایرانشهر": "Iranshahr", "ایلام": "Ilam", "ایوان": "Ivan",

    # ادامه شهرها
    "بابل": "Babol", "بابلسر": "Babolsar", "باغ‌ملک": "Bagh-e Malek",
    "بافت": "Baft", "بافق": "Bafq", "بانه": "Baneh",
    "باوی": "Bavi", "بجستان": "Bajestan", "بردسیر": "Bardsir",
    "بردستان": "Bardestan", "برزول": "Barzul", "برزویه": "Barzaviyeh",
    "بروجرد": "Borujerd", "بروجن": "Borujen", "بستان": "Bostan",
    "بستان‌آباد": "Bostanabad", "بستک": "Bastak", "بشرویه": "Boshruyeh",
    "بم": "Bam", "بمپور": "Bampur", "بناب": "Bonab",
    "بندر امام خمینی": "Bandar Imam Khomeini", "بندر ترکمن": "Bandar Torkaman",
    "بندر خمیر": "Bandar Khamir", "بندر دیر": "Bandar Deyr", "بندر دیلم": "Bandar Deylam",
    "بندر ریگ": "Bandar Rig", "بندر کنگان": "Bandar Kangan", "بندر گز": "Bandar Gaz",
    "بندر گناوه": "Bandar Ganaveh", "بندر لنگه": "Bandar Lengeh",
    "بنجار": "Banjar", "بهار": "Bahar", "بهارستان": "Baharestan",
    "بهبهان": "Behbahan", "بهشهر": "Behshahr", "بوانات": "Bavanat",
    "بوئین‌زهرا": "Buin Zahra", "بوکان": "Bukan", "بویین میاندشت": "Buyin Miandasht",
    "بیجار": "Bijar", "بیرجند": "Birjand", "بیله‌سوار": "Bileh Savar",
    
    "پارس‌آباد": "Parsabad", "پاکدشت": "Pakdasht", "پاوه": "Paveh",
    "پردیس": "Pardis", "پیرانشهر": "Piranshahr", "پیشوا": "Pishva",
    
    "تاکستان": "Takestan", "تایباد": "Taybad", "تبریز": "Tabriz",
    "تربت جام": "Torbat-e Jam", "تربت حیدریه": "Torbat-e Heydarieh",
    "تفت": "Taft", "تفرش": "Tafresh", "تکاب": "Takab",
    "تنکابن": "Tonekabon", "تویسرکان": "Tuyserkan",
    
    "جاجرم": "Jajarm", "جاسک": "Jask", "جلفا": "Jolfa",
    "جم": "Jam", "جهرم": "Jahrom", "جوانرود": "Javanrud",
    "جویبار": "Juybar", "جیرفت": "Jiroft",
    
    "چابهار": "Chabahar", "چادگان": "Chadegan", "چالوس": "Chalus",
    "چرام": "Charam", "چناران": "Chenaran",
    
    "حاجی‌آباد": "Hajjiabad", "خاش": "Khash", "خاوران": "Khavaran",
    "خرم‌آباد": "Khorramabad", "خرمدره": "Khorramdarreh", "خرمشهر": "Khorramshahr",
    "خلخال": "Khalkhal", "خمین": "Khomein", "خوانسار": "Khansar",
    "خواف": "Khvaf", "خور": "Khur", "خوی": "Khoy",
    "خورموج": "Khorramuj", "خوسف": "Khusf",
    
    "دامغان": "Damghan", "داراب": "Darab", "دره شهر": "Dareh Shahr",
    "درگز": "Dargaz", "دزفول": "Dezful", "دشت آزادگان": "Dasht-e Azadegan",
    "دلیجان": "Delijan", "دماوند": "Damavand", "دهاقان": "Dehaqan",
    "دهدشت": "Dehdasht", "دهلران": "Dehloran", "دورود": "Dorud",
    "دوگنبدان": "Dogonbadan",
    
    "رابر": "Raver", "راسک": "Rask", "رامسر": "Ramsar",
    "رامشیر": "Ramshir", "رامهرمز": "Ramhormoz", "راور": "Ravar",
    "رباط کریم": "Robat Karim", "رشت": "Rasht", "رضوان‌شهر": "Rezvanshahr",
    "رفسنجان": "Rafsanjan", "رودبار": "Rudbar", "رودسر": "Rudsar",
    "رودهن": "Rudehen", "روانسر": "Ravansar", "ری": "Rey",
    
    "زابل": "Zabol", "زاهدان": "Zahedan", "زرند": "Zarand",
    "زرقان": "Zarqan", "زرین‌شهر": "Zarrin Shahr", "زنجان": "Zanjan",
    
    "ساری": "Sari", "ساوجبلاغ": "Saveh Bolagh", "ساوه": "Saveh",
    "سبزوار": "Sabzevar", "سراب": "Sarab", "سرابله": "Sarableh",
    "سرخس": "Sarakhs", "سردشت": "Sardasht", "سرعین": "Sarein",
    "سرپل ذهاب": "Sarpol-e Zahab", "سروستان": "Sarvestan",
    "سلماس": "Salmas", "سمنان": "Semnan", "سمیرم": "Semirom",
    "سنندج": "Sanandaj", "سنقر": "Sonqor", "سوادکوه": "Savadkuh",
    "سوسنگرد": "Susangerd", "سومار": "Sumar", "سی سخت": "Si Sakht",
    "سیرجان": "Sirjan", "سیمرغ": "Simorgh",
    
    "شادگان": "Shadegan", "شاهرود": "Shahroud", "شاهین‌شهر": "Shahin Shahr",
    "شاهین دژ": "Shahin Dezh", "شبستر": "Shabestar", "شفت": "Shaft",
    "شهر بابک": "Shahr-e Babak", "شهرضا": "Shahreza", "شهرکرد": "Shahrekord",
    "شهریار": "Shahriar", "شوش": "Shush", "شوشتر": "Shushtar",
    "شیراز": "Shiraz", "شیروان": "Shirvan",
    
    "صحنه": "Sahneh", "صومعه سرا": "Sowme'eh Sara",
    
    "طالقان": "Taleqan", "طبس": "Tabas", "طرقبه": "Torqabeh",
    
    "عجب‌شیر": "Ajab Shir", "عسلویه": "Asaluyeh",
    
    "فارسان": "Farsan", "فاروج": "Faruj", "فردوس": "Ferdows",
    "فردیس": "Fardis", "فریدن": "Faridan", "فریدون‌کنار": "Fereydunkenar",
    "فریدون‌شهر": "Fereydunshahr", "فریمان": "Fariman", "فسا": "Fasa",
    "فلاورجان": "Falavarjan", "فومن": "Fuman", "فیروزآباد": "Firuzabad",
    "فیروزکوه": "Firuzkuh",
    
    "قائم‌شهر": "Qaemshahr", "قائن": "Qayen", "قدس": "Qods",
    "قروه": "Qorveh", "قزوین": "Qazvin", "قشم": "Qeshm",
    "قصر شیرین": "Qasr-e Shirin", "قلعه گنج": "Qaleh Ganj",
    "قم": "Qom", "قوچان": "Quchan",
    
    "کازرون": "Kazerun", "کاشان": "Kashan", "کاشمر": "Kashmar",
    "کامیاران": "Kamyaran", "کبودرآهنگ": "Kabudarahang", "کرج": "Karaj",
    "کردکوی": "Kordkuy", "کرمان": "Kerman", "کرمانشاه": "Kermanshah",
    "کلاله": "Kalaleh", "کلات": "Kalat", "کلیبر": "Kalibar",
    "کنارک": "Konarak", "کنگاور": "Kangavar", "کوار": "Kavar",
    "کوهبنان": "Kuhbanan", "کوهدشت": "Kuhdasht", "کیش": "Kish",
    
    "گتوند": "Gotvand", "گراش": "Gerash", "گرگان": "Gorgan",
    "گرمسار": "Garmsar", "گلپایگان": "Golpayegan", "گناباد": "Gonabad",
    "گنبد کاووس": "Gonbad-e Kavus", "گچساران": "Gachsaran",
    
    "لاهیجان": "Lahijan", "لامرد": "Lamerd", "لار": "Lar",
    "لردگان": "Lordegan", "لنگرود": "Langarud", "لوشان": "Lushan",
    
    "ماسال": "Masal", "ماکو": "Maku", "ماهان": "Mahan",
    "ماهشهر": "Mahshahr", "مبارکه": "Mobarakeh", "مراغه": "Maragheh",
    "مرند": "Marand", "مریوان": "Marivan", "مرودشت": "Marvdasht",
    "مسجد سلیمان": "Masjed Soleyman", "مشگین‌شهر": "Meshgin Shahr",
    "مشهد": "Mashhad", "ملارد": "Malard", "ملایر": "Malayer",
    "منجیل": "Manjil", "مهاباد": "Mahabad", "مهدی‌شهر": "Mahdi Shahr",
    "مهران": "Mehran", "مهریز": "Mehriz", "میاندوآب": "Miandoab",
    "میانه": "Mianeh", "میبد": "Meybod", "میناب": "Minab",
    "مینودشت": "Minudasht",
    
    "نائین": "Naein", "نجف‌آباد": "Najafabad", "نراق": "Naraq",
    "نظرآباد": "Nazarabad", "نطنز": "Natanz", "نقده": "Naqadeh",
    "نکا": "Neka", "نور": "Nur", "نورآباد": "Nurabad",
    "نوشهر": "Nowshahr", "نهاوند": "Nahavand", "نی‌ریز": "Neyriz",
    "نیشابور": "Neyshabur", "نیک‌شهر": "Nikshahr",
    
    "ورامین": "Varamin",
    
    "هرسین": "Harsin", "هشتگرد": "Hashtgerd", "هشتپر": "Hashtpar",
    "همدان": "Hamadan",
    
    "یاسوج": "Yasuj", "یزد": "Yazd"
}

def transliterate_persian_to_english(persian_text):
    """Simple transliteration for cities without predefined names"""
    # این تابع برای شهرهایی که نام انگلیسی ندارند
    transliteration_map = {
        'آ': 'A', 'ا': 'A', 'ب': 'B', 'پ': 'P', 'ت': 'T', 'ث': 'S',
        'ج': 'J', 'چ': 'Ch', 'ح': 'H', 'خ': 'Kh', 'د': 'D', 'ذ': 'Z',
        'ر': 'R', 'ز': 'Z', 'ژ': 'Zh', 'س': 'S', 'ش': 'Sh', 'ص': 'S',
        'ض': 'Z', 'ط': 'T', 'ظ': 'Z', 'ع': 'A', 'غ': 'Gh', 'ف': 'F',
        'ق': 'Q', 'ک': 'K', 'گ': 'G', 'ل': 'L', 'م': 'M', 'ن': 'N',
        'و': 'V', 'ه': 'H', 'ی': 'Y', 'ئ': '', 'ء': '', '‌': ' '
    }
    
    result = []
    for char in persian_text:
        result.append(transliteration_map.get(char, char))
    
    return ''.join(result).strip()

def add_english_names():
    """Add English names to all cities"""
    print("🔄 Adding English names to cities...")
    
    with open('iran_cities.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_cities = 0
    cities_with_names = 0
    cities_without_names = 0
    
    for province in data:
        for city in province['cities']:
            total_cities += 1
            
            # Check if already has English name
            if city.get('english_name'):
                cities_with_names += 1
                continue
            
            # Try to find in dictionary
            city_name = city['name']
            if city_name in CITY_ENGLISH_NAMES:
                city['english_name'] = CITY_ENGLISH_NAMES[city_name]
                cities_with_names += 1
            else:
                # Use transliteration
                city['english_name'] = transliterate_persian_to_english(city_name)
                cities_without_names += 1
                print(f"  ⚠️  Auto-transliterated: {city_name} -> {city['english_name']}")
    
    # Save
    with open('iran_cities.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ English names added!")
    print(f"  Total cities: {total_cities}")
    print(f"  With predefined names: {cities_with_names}")
    print(f"  Auto-transliterated: {cities_without_names}")

if __name__ == '__main__':
    add_english_names()
