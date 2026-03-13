#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate SQL file from Iran cities JSON data
"""

import json
import sys
import os

def load_data():
    """Load Iran cities data"""
    with open('iran_cities.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_sql():
    """Generate SQL script"""
    data = load_data()
    
    sql = []
    
    # Header
    sql.append("-- Iran Provinces and Cities Database")
    sql.append("-- Generated automatically from iran_cities.json")
    sql.append("-- Encoding: UTF-8")
    sql.append("")
    sql.append("SET NAMES utf8mb4;")
    sql.append("SET CHARACTER SET utf8mb4;")
    sql.append("")
    
    # Drop tables if exist
    sql.append("-- Drop tables if they exist")
    sql.append("DROP TABLE IF EXISTS `cities`;")
    sql.append("DROP TABLE IF EXISTS `provinces`;")
    sql.append("")
    
    # Create provinces table
    sql.append("-- Create provinces table")
    sql.append("CREATE TABLE `provinces` (")
    sql.append("  `id` INT PRIMARY KEY,")
    sql.append("  `name` VARCHAR(100) NOT NULL,")
    sql.append("  `english_name` VARCHAR(100) NOT NULL,")
    sql.append("  `phone_code` VARCHAR(10) NOT NULL,")
    sql.append("  `cities_count` INT NOT NULL,")
    sql.append("  UNIQUE KEY `name` (`name`),")
    sql.append("  UNIQUE KEY `english_name` (`english_name`)")
    sql.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
    sql.append("")
    
    # Create cities table
    sql.append("-- Create cities table")
    sql.append("CREATE TABLE `cities` (")
    sql.append("  `id` INT PRIMARY KEY,")
    sql.append("  `province_id` INT NOT NULL,")
    sql.append("  `name` VARCHAR(100) NOT NULL,")
    sql.append("  `english_name` VARCHAR(100),")
    sql.append("  `latitude` DECIMAL(10, 7) NOT NULL,")
    sql.append("  `longitude` DECIMAL(10, 7) NOT NULL,")
    sql.append("  `is_capital` BOOLEAN DEFAULT FALSE,")
    sql.append("  `population` INT,")
    sql.append("  `postal_code` VARCHAR(20),")
    sql.append("  FOREIGN KEY (`province_id`) REFERENCES `provinces`(`id`) ON DELETE CASCADE,")
    sql.append("  INDEX `idx_province` (`province_id`),")
    sql.append("  INDEX `idx_name` (`name`)")
    sql.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
    sql.append("")
    
    # Insert provinces
    sql.append("-- Insert provinces data")
    for province in data:
        sql.append(
            f"INSERT INTO `provinces` (`id`, `name`, `english_name`, `phone_code`, `cities_count`) "
            f"VALUES ({province['id']}, '{province['province']}', '{province['english_name']}', "
            f"'{province['phone_code']}', {province['cities_count']});"
        )
    sql.append("")
    
    # Insert cities
    sql.append("-- Insert cities data")
    city_global_id = 1
    for province in data:
        for city in province['cities']:
            english_name = city.get('english_name', 'NULL')
            if english_name != 'NULL':
                english_name = f"'{english_name}'"
            
            population = city.get('population', 'NULL')
            postal_code = city.get('postal_code', 'NULL')
            if postal_code != 'NULL':
                postal_code = f"'{postal_code}'"
            
            is_capital = 1 if city.get('is_capital', False) else 0
            
            sql.append(
                f"INSERT INTO `cities` (`id`, `province_id`, `name`, `english_name`, "
                f"`latitude`, `longitude`, `is_capital`, `population`, `postal_code`) "
                f"VALUES ({city_global_id}, {province['id']}, '{city['name']}', {english_name}, "
                f"{city['latitude']}, {city['longitude']}, {is_capital}, {population}, {postal_code});"
            )
            city_global_id += 1
    
    return '\n'.join(sql)

if __name__ == '__main__':
    print("🔄 Generating SQL file...")
    
    try:
        sql_content = generate_sql()
        
        with open('iran_cities.sql', 'w', encoding='utf-8') as f:
            f.write(sql_content)
        
        print("✅ SQL file generated successfully: iran_cities.sql")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
