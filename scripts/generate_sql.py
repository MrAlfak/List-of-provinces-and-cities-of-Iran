#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate SQL for MySQL or PostgreSQL from ``iran_cities.json``."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_data(path: str = "iran_cities.json") -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError("Expected a top-level province array")
    return data


def quote(value: Any) -> str:
    """Return a portable single-quoted SQL literal."""
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def number(value: Any) -> str:
    if value is None or value == "":
        return "NULL"
    return str(float(value))


def generate_mysql_sql(data: list[dict[str, Any]]) -> str:
    lines = [
        "-- Iran Provinces and Cities Database (MySQL 8+)",
        "-- Generated from iran_cities.json; do not edit by hand.",
        "SET NAMES utf8mb4;",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "DROP TABLE IF EXISTS `cities`;",
        "DROP TABLE IF EXISTS `provinces`;",
        "SET FOREIGN_KEY_CHECKS = 1;",
        "",
        "CREATE TABLE `provinces` (",
        "  `id` INT NOT NULL PRIMARY KEY,",
        "  `uid` VARCHAR(128) NULL UNIQUE,",
        "  `official_code` VARCHAR(64) NULL,",
        "  `name` VARCHAR(150) NOT NULL,",
        "  `english_name` VARCHAR(150) NULL,",
        "  `phone_code` VARCHAR(16) NULL,",
        "  `cities_count` INT NOT NULL,",
        "  UNIQUE KEY `uq_province_name` (`name`)",
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;",
        "",
        "CREATE TABLE `cities` (",
        "  `id` INT NOT NULL PRIMARY KEY,",
        "  `province_id` INT NOT NULL,",
        "  `uid` VARCHAR(128) NULL UNIQUE,",
        "  `official_code` VARCHAR(64) NULL,",
        "  `name` VARCHAR(150) NOT NULL,",
        "  `english_name` VARCHAR(150) NULL,",
        "  `latitude` DECIMAL(12,8) NULL,",
        "  `longitude` DECIMAL(12,8) NULL,",
        "  `is_capital` BOOLEAN NOT NULL DEFAULT FALSE,",
        "  `population` BIGINT NULL,",
        "  `postal_code` VARCHAR(32) NULL,",
        "  `county` VARCHAR(150) NULL,",
        "  `county_code` VARCHAR(64) NULL,",
        "  `district` VARCHAR(150) NULL,",
        "  `district_code` VARCHAR(64) NULL,",
        "  CONSTRAINT `fk_cities_province` FOREIGN KEY (`province_id`) REFERENCES `provinces` (`id`) ON DELETE CASCADE,",
        "  UNIQUE KEY `uq_city_name_province` (`province_id`, `name`),",
        "  KEY `idx_city_name` (`name`),",
        "  KEY `idx_city_official_code` (`official_code`)",
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;",
        "",
    ]

    for province in data:
        lines.append(
            "INSERT INTO `provinces` (`id`,`uid`,`official_code`,`name`,`english_name`,`phone_code`,`cities_count`) VALUES "
            f"({province['id']},{quote(province.get('uid'))},{quote(province.get('official_code'))},"
            f"{quote(province.get('province'))},{quote(province.get('english_name'))},{quote(province.get('phone_code'))},"
            f"{len(province.get('cities', []))});"
        )

    lines.append("")
    for province in data:
        for city in province.get("cities", []):
            population = "NULL" if city.get("population") in (None, "") else str(int(city["population"]))
            lines.append(
                "INSERT INTO `cities` (`id`,`province_id`,`uid`,`official_code`,`name`,`english_name`,`latitude`,`longitude`,"
                "`is_capital`,`population`,`postal_code`,`county`,`county_code`,`district`,`district_code`) VALUES "
                f"({city['id']},{province['id']},{quote(city.get('uid'))},{quote(city.get('official_code'))},"
                f"{quote(city.get('name'))},{quote(city.get('english_name'))},{number(city.get('latitude'))},"
                f"{number(city.get('longitude'))},{1 if city.get('is_capital') else 0},{population},"
                f"{quote(city.get('postal_code'))},{quote(city.get('county'))},{quote(city.get('county_code'))},"
                f"{quote(city.get('district'))},{quote(city.get('district_code'))});"
            )
    return "\n".join(lines) + "\n"


def generate_postgresql_sql(data: list[dict[str, Any]]) -> str:
    lines = [
        "-- Iran Provinces and Cities Database (PostgreSQL 14+)",
        "-- Generated from iran_cities.json; do not edit by hand.",
        "BEGIN;",
        "DROP TABLE IF EXISTS cities;",
        "DROP TABLE IF EXISTS provinces;",
        "",
        "CREATE TABLE provinces (",
        "  id INTEGER PRIMARY KEY,",
        "  uid VARCHAR(128) UNIQUE,",
        "  official_code VARCHAR(64),",
        "  name VARCHAR(150) NOT NULL UNIQUE,",
        "  english_name VARCHAR(150),",
        "  phone_code VARCHAR(16),",
        "  cities_count INTEGER NOT NULL",
        ");",
        "",
        "CREATE TABLE cities (",
        "  id INTEGER PRIMARY KEY,",
        "  province_id INTEGER NOT NULL REFERENCES provinces(id) ON DELETE CASCADE,",
        "  uid VARCHAR(128) UNIQUE,",
        "  official_code VARCHAR(64),",
        "  name VARCHAR(150) NOT NULL,",
        "  english_name VARCHAR(150),",
        "  latitude NUMERIC(12,8),",
        "  longitude NUMERIC(12,8),",
        "  is_capital BOOLEAN NOT NULL DEFAULT FALSE,",
        "  population BIGINT,",
        "  postal_code VARCHAR(32),",
        "  county VARCHAR(150),",
        "  county_code VARCHAR(64),",
        "  district VARCHAR(150),",
        "  district_code VARCHAR(64),",
        "  UNIQUE (province_id, name)",
        ");",
        "CREATE INDEX idx_city_name ON cities(name);",
        "CREATE INDEX idx_city_official_code ON cities(official_code);",
        "",
    ]

    for province in data:
        lines.append(
            "INSERT INTO provinces (id,uid,official_code,name,english_name,phone_code,cities_count) VALUES "
            f"({province['id']},{quote(province.get('uid'))},{quote(province.get('official_code'))},"
            f"{quote(province.get('province'))},{quote(province.get('english_name'))},{quote(province.get('phone_code'))},"
            f"{len(province.get('cities', []))});"
        )

    lines.append("")
    for province in data:
        for city in province.get("cities", []):
            population = "NULL" if city.get("population") in (None, "") else str(int(city["population"]))
            lines.append(
                "INSERT INTO cities (id,province_id,uid,official_code,name,english_name,latitude,longitude,is_capital,"
                "population,postal_code,county,county_code,district,district_code) VALUES "
                f"({city['id']},{province['id']},{quote(city.get('uid'))},{quote(city.get('official_code'))},"
                f"{quote(city.get('name'))},{quote(city.get('english_name'))},{number(city.get('latitude'))},"
                f"{number(city.get('longitude'))},{'TRUE' if city.get('is_capital') else 'FALSE'},{population},"
                f"{quote(city.get('postal_code'))},{quote(city.get('county'))},{quote(city.get('county_code'))},"
                f"{quote(city.get('district'))},{quote(city.get('district_code'))});"
            )
    lines.extend(["", "COMMIT;"])
    return "\n".join(lines) + "\n"


def generate_sql(dialect: str = "mysql", input_path: str = "iran_cities.json") -> str:
    data = load_data(input_path)
    if dialect == "mysql":
        return generate_mysql_sql(data)
    if dialect == "postgresql":
        return generate_postgresql_sql(data)
    raise ValueError(f"Unsupported SQL dialect: {dialect}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="iran_cities.json")
    parser.add_argument("--dialect", choices=("mysql", "postgresql", "both"), default="both")
    parser.add_argument("--output", help="Output path for a single dialect")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.dialect == "both":
        outputs = {
            "iran_cities.mysql.sql": generate_sql("mysql", args.input),
            "iran_cities.postgresql.sql": generate_sql("postgresql", args.input),
        }
        for path, content in outputs.items():
            Path(path).write_text(content, encoding="utf-8")
            print(f"✅ Generated {path}")
        return 0

    output = args.output or f"iran_cities.{args.dialect}.sql"
    Path(output).write_text(generate_sql(args.dialect, args.input), encoding="utf-8")
    print(f"✅ Generated {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
