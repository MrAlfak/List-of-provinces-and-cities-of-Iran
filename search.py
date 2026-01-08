import json
import sys

def load_data():
    with open('iran_cities.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def search(query):
    data = load_data()
    results = []
    
    query = query.lower()
    
    for item in data:
        # جستجو در نام استان (فارسی و انگلیسی)
        if query in item['province'] or query in item['english_name'].lower():
            results.append({
                'type': 'Province',
                'name': item['province'],
                'english': item['english_name'],
                'phone_code': item['phone_code'],
                'cities_count': len(item['cities'])
            })
        
        # جستجو در شهرها
        for city in item['cities']:
            if query in city:
                results.append({
                    'type': 'City',
                    'name': city,
                    'province': item['province'],
                    'phone_code': item['phone_code']
                })
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py <search_term>")
        print("Example: python search.py تهران")
        sys.exit(1)
    
    search_term = sys.argv[1]
    results = search(search_term)
    
    if not results:
        print(f"No results found for '{search_term}'")
    else:
        print(f"Found {len(results)} results:\n")
        for res in results:
            if res['type'] == 'Province':
                print(f"📌 [استان] {res['name']} ({res['english']}) | پیش‌شماره: {res['phone_code']} | تعداد شهرها: {res['cities_count']}")
            else:
                print(f"🏙️ [شهر] {res['name']} (استان {res['province']}) | پیش‌شماره: {res['phone_code']}")
