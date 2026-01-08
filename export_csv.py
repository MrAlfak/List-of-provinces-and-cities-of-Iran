import json
import csv

def json_to_csv():
    try:
        with open('iran_cities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        output_file = 'iran_cities.csv'
        
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            # نوشتن هدر
            writer.writerow(['Province', 'English Name', 'Phone Code', 'City'])
            
            # نوشتن داده‌ها
            for item in data:
                for city in item['cities']:
                    writer.writerow([
                        item['province'],
                        item['english_name'],
                        item['phone_code'],
                        city
                    ])
        
        print(f"✅ Successfully exported to {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    json_to_csv()
