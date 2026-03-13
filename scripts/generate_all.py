#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate all output formats from Iran cities JSON data
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generate_sql import generate_sql
from scripts.generate_csv import generate_csv
from scripts.generate_geojson import generate_geojson
from scripts.generate_minified import generate_minified

def main():
    """Generate all formats"""
    print("🚀 Generating all output formats...\n")
    
    try:
        # Generate SQL
        print("1️⃣ Generating SQL...")
        sql_content = generate_sql()
        with open('iran_cities.sql', 'w', encoding='utf-8') as f:
            f.write(sql_content)
        print("   ✅ SQL generated\n")
        
        # Generate CSV
        print("2️⃣ Generating CSV...")
        generate_csv()
        print()
        
        # Generate GeoJSON
        print("3️⃣ Generating GeoJSON...")
        generate_geojson()
        print()
        
        # Generate Minified
        print("4️⃣ Generating Minified JSON...")
        generate_minified()
        print()
        
        print("✅ All formats generated successfully!")
        print("\nGenerated files:")
        print("  📄 iran_cities.sql")
        print("  📄 iran_cities.csv")
        print("  📄 iran_cities.geojson")
        print("  📄 iran_cities.min.json")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
