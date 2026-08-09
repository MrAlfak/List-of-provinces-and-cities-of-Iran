#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalize an explicitly supplied Iran locations dataset safely.

The old implementation downloaded ``iran_cities.json`` from this repository and
then treated that copy as its own upstream source. That made provenance
circular and could also renumber every city. This replacement is deliberately
boring: callers must provide an input file, existing IDs are preserved, and new
IDs are allocated only above the current maximum.

This script performs structural cleanup only. It does not decide whether a
record is legally a city, does not silently delete similar names, and does not
invent English transliterations.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


ARABIC_TO_PERSIAN = str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک"})

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
    "یزد": "Yazd",
}


def clean_name(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).translate(ARABIC_TO_PERSIAN)
    text = text.replace("ـ", "")
    return re.sub(r"\s+", " ", text).strip()


def max_existing_id(data: list[dict[str, Any]], collection: str) -> int:
    values: list[int] = []
    if collection == "province":
        values = [p["id"] for p in data if isinstance(p.get("id"), int)]
    else:
        values = [
            c["id"]
            for p in data
            for c in p.get("cities", [])
            if isinstance(c.get("id"), int)
        ]
    return max(values, default=0)


def enhance_data(data: list[dict[str, Any]], source_date: str | None = None) -> list[dict[str, Any]]:
    next_province_id = max_existing_id(data, "province") + 1
    next_city_id = max_existing_id(data, "city") + 1
    used_province_ids: set[int] = set()
    used_city_ids: set[int] = set()
    result: list[dict[str, Any]] = []

    for raw_province in data:
        province_name = clean_name(raw_province.get("province"))
        if not province_name:
            raise ValueError("Province without a name")

        province_id = raw_province.get("id")
        if not isinstance(province_id, int) or province_id in used_province_ids:
            province_id = next_province_id
            next_province_id += 1
        used_province_ids.add(province_id)

        province: dict[str, Any] = {
            **raw_province,
            "id": province_id,
            "province": province_name,
            "english_name": raw_province.get("english_name") or PROVINCE_ENGLISH_NAMES.get(province_name),
            "phone_code": str(raw_province.get("phone_code", "")).strip(),
            "cities": [],
        }
        if source_date:
            province["last_updated"] = source_date

        for raw_city in raw_province.get("cities", []):
            if isinstance(raw_city, str):
                raw_city = {"name": raw_city}
            if not isinstance(raw_city, dict):
                raise ValueError(f"Invalid city record in {province_name}: {raw_city!r}")

            city_name = clean_name(raw_city.get("name"))
            if not city_name:
                raise ValueError(f"City without a name in {province_name}")

            city_id = raw_city.get("id")
            if not isinstance(city_id, int) or city_id in used_city_ids:
                city_id = next_city_id
                next_city_id += 1
            used_city_ids.add(city_id)

            province["cities"].append({
                **raw_city,
                "id": city_id,
                "name": city_name,
                "english_name": raw_city.get("english_name"),
                "is_capital": bool(raw_city.get("is_capital", False)),
                "population": raw_city.get("population"),
                "postal_code": raw_city.get("postal_code"),
            })

        province["cities_count"] = len(province["cities"])
        result.append(province)

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Explicit upstream/local JSON file")
    parser.add_argument("--output", default="iran_cities.json", help="Normalized output file")
    parser.add_argument(
        "--source-date",
        help="Date belonging to the source snapshot (do not use the processing date by accident)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    if source_path == output_path:
        raise SystemExit("Refusing to use the output file as its own upstream source. Use a separate --input snapshot.")

    data = json.loads(source_path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise SystemExit("Expected a top-level JSON array of provinces.")

    enhanced = enhance_data(data, args.source_date)
    output_path.write_text(json.dumps(enhanced, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ Wrote {len(enhanced)} provinces to {output_path}")
    print(f"   Cities/locations: {sum(len(p['cities']) for p in enhanced)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
