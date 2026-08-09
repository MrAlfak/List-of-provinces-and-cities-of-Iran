#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild the canonical city list from normalized country-division data.

The canonical question "is this record an official city?" must come from an
administrative-division source, not from coordinates, search results, or a
hand-maintained deletion list.

Input format
------------
A UTF-8/UTF-8-BOM CSV with these columns (the normalized format commonly used
for Iran country-division exports):

    id,parentCountryDivisionId,name,code,divisionType

``divisionType`` values:
    0 country, 1 province, 2 county, 3 district, 4 rural district,
    5 city, 6 settlement/village.

The script keeps the existing JSON schema for compatibility, preserves legacy
numeric IDs when a province/city match is found, adds a stable ``uid`` based on
the official code, and enriches matched cities with legacy coordinates and
English names. New official cities receive new numeric IDs above the previous
maximum, so existing consumers are not renumbered.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


ARABIC_TO_PERSIAN = str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک"})


def normalize_fa(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).translate(ARABIC_TO_PERSIAN)
    text = text.replace("\u200c", " ").replace("ـ", "")
    return re.sub(r"\s+", " ", text).strip().casefold()


def as_int(value: Any) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def read_divisions(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"id", "parentCountryDivisionId", "name", "code", "divisionType"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            missing = sorted(required.difference(set(reader.fieldnames or [])))
            raise ValueError(f"Missing required division columns: {', '.join(missing)}")
        return [dict(row) for row in reader]


def load_legacy(path: Path | None) -> list[dict[str, Any]]:
    if not path:
        return []
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError("Legacy JSON must be a top-level province array")
    return data


def ancestors(row: dict[str, str], by_id: dict[str, dict[str, str]]) -> Iterable[dict[str, str]]:
    seen: set[str] = set()
    current = row
    while True:
        parent_id = str(current.get("parentCountryDivisionId", "")).strip()
        if not parent_id or parent_id in seen:
            return
        seen.add(parent_id)
        parent = by_id.get(parent_id)
        if not parent:
            return
        yield parent
        current = parent


def nearest_ancestor(
    row: dict[str, str], by_id: dict[str, dict[str, str]], division_type: int
) -> dict[str, str] | None:
    for item in ancestors(row, by_id):
        if as_int(item.get("divisionType")) == division_type:
            return item
    return None


def build_legacy_indexes(legacy: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, str], dict[str, Any]], int, int]:
    province_index: dict[str, dict[str, Any]] = {}
    city_index: dict[tuple[str, str], dict[str, Any]] = {}
    max_province_id = 0
    max_city_id = 0

    for province in legacy:
        pkey = normalize_fa(province.get("province"))
        province_index[pkey] = province
        if isinstance(province.get("id"), int):
            max_province_id = max(max_province_id, province["id"])
        for city in province.get("cities", []):
            city_index[(pkey, normalize_fa(city.get("name")))] = city
            if isinstance(city.get("id"), int):
                max_city_id = max(max_city_id, city["id"])

    return province_index, city_index, max_province_id, max_city_id


def rebuild(divisions: list[dict[str, str]], legacy: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    by_id = {str(row.get("id", "")).strip(): row for row in divisions}
    province_rows = [r for r in divisions if as_int(r.get("divisionType")) == 1]
    city_rows = [r for r in divisions if as_int(r.get("divisionType")) == 5]

    legacy_provinces, legacy_cities, max_province_id, max_city_id = build_legacy_indexes(legacy)
    next_province_id = max_province_id + 1
    next_city_id = max_city_id + 1

    provinces_by_source_id: dict[str, dict[str, Any]] = {}
    output: list[dict[str, Any]] = []

    for source in sorted(province_rows, key=lambda r: (str(r.get("code", "")), str(r.get("name", "")))):
        name = str(source.get("name", "")).strip()
        pkey = normalize_fa(name)
        old = legacy_provinces.get(pkey, {})
        province_id = old.get("id") if isinstance(old.get("id"), int) else next_province_id
        if not isinstance(old.get("id"), int):
            next_province_id += 1

        code = str(source.get("code", "")).strip()
        item = {
            "id": province_id,
            "uid": f"ir:province:{code or source['id']}",
            "official_code": code or None,
            "province": name,
            "english_name": old.get("english_name"),
            "phone_code": old.get("phone_code"),
            "cities_count": 0,
            "cities": [],
        }
        provinces_by_source_id[str(source["id"]).strip()] = item
        output.append(item)

    unmatched_cities = 0
    enriched_cities = 0

    for source in sorted(city_rows, key=lambda r: (str(r.get("code", "")), str(r.get("name", "")))):
        province_source = nearest_ancestor(source, by_id, 1)
        if not province_source:
            unmatched_cities += 1
            continue

        province = provinces_by_source_id.get(str(province_source.get("id", "")).strip())
        if not province:
            unmatched_cities += 1
            continue

        name = str(source.get("name", "")).strip()
        pkey = normalize_fa(province["province"])
        old = legacy_cities.get((pkey, normalize_fa(name)), {})
        city_id = old.get("id") if isinstance(old.get("id"), int) else next_city_id
        if not isinstance(old.get("id"), int):
            next_city_id += 1
        else:
            enriched_cities += 1

        county = nearest_ancestor(source, by_id, 2)
        district = nearest_ancestor(source, by_id, 3)
        code = str(source.get("code", "")).strip()

        province["cities"].append({
            "id": city_id,
            "uid": f"ir:city:{code or source['id']}",
            "official_code": code or None,
            "name": name,
            "english_name": old.get("english_name"),
            "latitude": old.get("latitude"),
            "longitude": old.get("longitude"),
            "is_capital": bool(old.get("is_capital", False)),
            "population": old.get("population"),
            "postal_code": old.get("postal_code"),
            "county": county.get("name") if county else None,
            "county_code": county.get("code") if county else None,
            "district": district.get("name") if district else None,
            "district_code": district.get("code") if district else None,
        })

    for province in output:
        province["cities_count"] = len(province["cities"])

    stats = {
        "provinces": len(output),
        "cities": sum(p["cities_count"] for p in output),
        "legacy_enriched_cities": enriched_cities,
        "unresolved_city_rows": unmatched_cities,
    }
    return output, stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--divisions-csv", required=True, help="Normalized administrative divisions CSV")
    parser.add_argument("--legacy-json", default="iran_cities.json", help="Optional legacy coordinate enrichment JSON")
    parser.add_argument("--output", default="iran_cities.rebuilt.json", help="Output JSON path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    divisions = read_divisions(Path(args.divisions_csv))
    legacy_path = Path(args.legacy_json) if args.legacy_json else None
    legacy = load_legacy(legacy_path)
    rebuilt, stats = rebuild(divisions, legacy)

    Path(args.output).write_text(
        json.dumps(rebuilt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if stats["unresolved_city_rows"]:
        print("⚠️ Some city rows could not be attached to a province; inspect the source hierarchy.")
        return 2
    print(f"✅ Rebuilt canonical city membership into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
