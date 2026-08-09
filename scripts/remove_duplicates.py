#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Safely detect and remove exact duplicate city records.

This script intentionally does *not* contain a hand-maintained list of cities to
remove. A city must never be deleted merely because it shares a coordinate,
alias, county name, or similar spelling with another record.

By default this command is read-only. Use ``--apply`` to remove only records
that are exact duplicates after Persian name normalization and coordinate
normalization within the same province.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


ARABIC_TO_PERSIAN = str.maketrans({
    "ي": "ی",
    "ى": "ی",
    "ك": "ک",
})


def normalize_name(value: str) -> str:
    """Return a comparison-safe Persian name without changing display text."""
    value = unicodedata.normalize("NFKC", value or "").translate(ARABIC_TO_PERSIAN)
    value = value.replace("\u200c", " ").replace("ـ", "")
    return re.sub(r"\s+", " ", value).strip().casefold()


def normalize_coordinate(value: Any) -> str:
    """Normalize a coordinate for exact-record comparison."""
    try:
        return f"{float(value):.7f}"
    except (TypeError, ValueError):
        return str(value).strip()


def exact_key(city: dict[str, Any]) -> tuple[str, str, str]:
    return (
        normalize_name(str(city.get("name", ""))),
        normalize_coordinate(city.get("latitude")),
        normalize_coordinate(city.get("longitude")),
    )


def find_exact_duplicates(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    duplicates: list[dict[str, Any]] = []
    for province in data:
        seen: dict[tuple[str, str, str], dict[str, Any]] = {}
        for city in province.get("cities", []):
            key = exact_key(city)
            if key in seen:
                duplicates.append({
                    "province": province.get("province"),
                    "keep_id": seen[key].get("id"),
                    "remove_id": city.get("id"),
                    "name": city.get("name"),
                    "latitude": city.get("latitude"),
                    "longitude": city.get("longitude"),
                })
            else:
                seen[key] = city
    return duplicates


def remove_exact_duplicates(data: list[dict[str, Any]]) -> int:
    removed = 0
    for province in data:
        seen: set[tuple[str, str, str]] = set()
        kept: list[dict[str, Any]] = []
        for city in province.get("cities", []):
            key = exact_key(city)
            if key in seen:
                removed += 1
                continue
            seen.add(key)
            kept.append(city)
        province["cities"] = kept
        province["cities_count"] = len(kept)
    return removed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="iran_cities.json", help="Input JSON file")
    parser.add_argument("--output", help="Output path; defaults to --input when --apply is used")
    parser.add_argument("--apply", action="store_true", help="Actually remove exact duplicates")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    data = json.loads(input_path.read_text(encoding="utf-8"))

    duplicates = find_exact_duplicates(data)
    if not duplicates:
        print("✅ No exact duplicate city records found.")
        return 0

    print(f"Found {len(duplicates)} exact duplicate record(s):")
    for item in duplicates:
        print(
            f"  - {item['province']} / {item['name']} "
            f"(keep id={item['keep_id']}, duplicate id={item['remove_id']})"
        )

    if not args.apply:
        print("\nRead-only mode: nothing was changed. Re-run with --apply to remove only these exact duplicates.")
        return 0

    removed = remove_exact_duplicates(data)
    output_path = Path(args.output or args.input)
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"✅ Removed {removed} exact duplicate record(s). Wrote {output_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
