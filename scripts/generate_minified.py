#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate minified JSON file from Iran cities JSON data
"""

import json
import sys

def load_data():
    """Load Iran cities data"""
    with open('iran_cities.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_minified():
    """Generate minified JSON file"""
    data = load_data()
    
    # Write minified version (no indentation, no extra spaces)
    with open('iran_cities.min.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    
    # Get file sizes
    import os
    original_size = os.path.getsize('iran_cities.json')
    minified_size = os.path.getsize('iran_cities.min.json')
    reduction = ((original_size - minified_size) / original_size) * 100
    
    print(f"✅ Minified JSON generated successfully: iran_cities.min.json")
    print(f"   Original size: {original_size:,} bytes")
    print(f"   Minified size: {minified_size:,} bytes")
    print(f"   Size reduction: {reduction:.1f}%")

if __name__ == '__main__':
    print("🔄 Generating minified JSON file...")
    
    try:
        generate_minified()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
