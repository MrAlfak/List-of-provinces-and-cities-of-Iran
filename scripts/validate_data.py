#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate the structural integrity of an Iran city dataset.

This validator deliberately separates *structural correctness* from the
semantic question of whether a record is officially a city. Use
``scripts/audit_data.py --strict`` on a newly rebuilt, source-backed snapshot
for semantic/enrichment quality.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Any


IRAN_BOUNDS = {"lat_min": 24.0, "lat_max": 40.5, "lon_min": 43.5, "lon_max": 64.5}
ARABIC_TO_PERSIAN = str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک"})


def normalize_name(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).translate(ARABIC_TO_PERSIAN)
    text = text.replace("\u200c", " ").replace("ـ", "")
    return re.sub(r"\s+", " ", text).strip().casefold()


def validate_data(data: Any, expected_provinces: int | None = 31) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, list):
        return ["Top-level JSON value must be an array of provinces"], warnings, {"provinces": 0, "cities": 0}

    if expected_provinces is not None and len(data) != expected_provinces:
        errors.append(f"Expected {expected_provinces} provinces, found {len(data)}")

    province_ids: set[int] = set()
    province_names: set[str] = set()
    province_uids: set[str] = set()
    city_ids: set[int] = set()
    city_uids: set[str] = set()
    total_cities = 0

    for p_index, province in enumerate(data):
        if not isinstance(province, dict):
            errors.append(f"Province at index {p_index} is not an object")
            continue

        label = str(province.get("province") or f"index {p_index}")
        for field in ("id", "province", "cities_count", "cities"):
            if field not in province:
                errors.append(f"Province {label!r} is missing required field {field!r}")

        province_id = province.get("id")
        if not isinstance(province_id, int) or province_id <= 0:
            errors.append(f"Province {label!r} has invalid numeric id: {province_id!r}")
        elif province_id in province_ids:
            errors.append(f"Duplicate province id: {province_id}")
        else:
            province_ids.add(province_id)

        normalized_province = normalize_name(province.get("province"))
        if not normalized_province:
            errors.append(f"Province {label!r} has an empty name")
        elif normalized_province in province_names:
            errors.append(f"Duplicate normalized province name: {label}")
        else:
            province_names.add(normalized_province)

        province_uid = province.get("uid")
        if province_uid:
            if not isinstance(province_uid, str) or province_uid in province_uids:
                errors.append(f"Province {label!r} has invalid/duplicate uid: {province_uid!r}")
            else:
                province_uids.add(province_uid)

        cities = province.get("cities", [])
        if not isinstance(cities, list):
            errors.append(f"Province {label!r} cities must be an array")
            continue

        total_cities += len(cities)
        if province.get("cities_count") != len(cities):
            errors.append(
                f"cities_count mismatch in {label}: declared={province.get('cities_count')!r}, actual={len(cities)}"
            )

        local_names: set[str] = set()
        capital_count = 0

        for c_index, city in enumerate(cities):
            if not isinstance(city, dict):
                errors.append(f"City at {label}[{c_index}] is not an object")
                continue

            city_label = str(city.get("name") or f"{label}[{c_index}]")
            for field in ("id", "name", "is_capital"):
                if field not in city:
                    errors.append(f"City {city_label!r} in {label} is missing required field {field!r}")

            city_id = city.get("id")
            if not isinstance(city_id, int) or city_id <= 0:
                errors.append(f"City {city_label!r} has invalid numeric id: {city_id!r}")
            elif city_id in city_ids:
                errors.append(f"Duplicate global city id {city_id}: {label} / {city_label}")
            else:
                city_ids.add(city_id)

            normalized_city = normalize_name(city.get("name"))
            if not normalized_city:
                errors.append(f"City with empty name in {label}")
            elif normalized_city in local_names:
                errors.append(f"Duplicate normalized city name in {label}: {city_label}")
            else:
                local_names.add(normalized_city)

            city_uid = city.get("uid")
            if city_uid:
                if not isinstance(city_uid, str) or city_uid in city_uids:
                    errors.append(f"City {city_label!r} has invalid/duplicate uid: {city_uid!r}")
                else:
                    city_uids.add(city_uid)

            if city.get("is_capital") is True:
                capital_count += 1
            elif not isinstance(city.get("is_capital"), bool):
                errors.append(f"City {label} / {city_label} has non-boolean is_capital")

            lat = city.get("latitude")
            lon = city.get("longitude")
            if (lat is None) != (lon is None):
                errors.append(f"City {label} / {city_label} must provide both latitude and longitude or neither")
            elif lat is not None and lon is not None:
                try:
                    lat_f = float(lat)
                    lon_f = float(lon)
                    if not (math.isfinite(lat_f) and math.isfinite(lon_f)):
                        raise ValueError("non-finite")
                    if not (IRAN_BOUNDS["lat_min"] <= lat_f <= IRAN_BOUNDS["lat_max"]):
                        warnings.append(f"Latitude outside broad Iran bounds: {label} / {city_label}: {lat_f}")
                    if not (IRAN_BOUNDS["lon_min"] <= lon_f <= IRAN_BOUNDS["lon_max"]):
                        warnings.append(f"Longitude outside broad Iran bounds: {label} / {city_label}: {lon_f}")
                except (TypeError, ValueError):
                    errors.append(f"Invalid coordinates for {label} / {city_label}: {lat!r}, {lon!r}")
            else:
                warnings.append(f"Missing coordinate enrichment: {label} / {city_label}")

            if not city.get("english_name"):
                warnings.append(f"Missing English-name enrichment: {label} / {city_label}")

        if capital_count != 1:
            errors.append(f"Province {label} must have exactly one capital; found {capital_count}")

    stats = {"provinces": len(data), "cities": total_cities}
    return errors, warnings, stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="iran_cities.json")
    parser.add_argument("--expected-provinces", type=int, default=31)
    parser.add_argument("--warnings-as-errors", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.input)
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"❌ Could not load {path}: {exc}")
        return 1

    errors, warnings, stats = validate_data(data, args.expected_provinces)
    print(f"📊 Provinces: {stats['provinces']} | Cities/locations: {stats['cities']}")

    if warnings:
        print(f"⚠️ Warnings: {len(warnings)}")
        for warning in warnings[:20]:
            print(f"  - {warning}")
        if len(warnings) > 20:
            print(f"  ... {len(warnings) - 20} more warning(s)")

    if errors:
        print(f"❌ Errors: {len(errors)}")
        for error in errors[:30]:
            print(f"  - {error}")
        if len(errors) > 30:
            print(f"  ... {len(errors) - 30} more error(s)")
        return 1

    if args.warnings_as_errors and warnings:
        print("❌ Validation failed because --warnings-as-errors was requested.")
        return 1

    print("✅ Structural validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
