#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit semantic and enrichment quality without silently changing data.

Structural validity belongs in ``validate_data.py``. This command reports
records that need source-level review: obvious border/facility labels,
administrative-area names that historically leaked into the legacy city list,
duplicate coordinates, weak English transliterations, and missing provenance.

Legacy data can be inspected in report-only mode. ``--strict`` is intended for
new source-backed snapshots and returns a non-zero exit status when review
items remain.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ARABIC_TO_PERSIAN = str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک"})

# High-confidence facility/border naming patterns. These are review signals,
# not an automatic deletion list.
FACILITY_PATTERNS = (
    re.compile(r"^مرز\s+"),
    re.compile(r"^پایانه\s+مرزی"),
)

# Names found in the legacy dataset that are also commonly used for a higher
# administrative area. They require checking against the selected source
# snapshot before they may be published as a city. Do not auto-delete them.
ADMINISTRATIVE_REVIEW_NAMES = {
    "چایپاره",
    "خوروبیابانک",
    "دشت آزادگان",
    "شمیرانات",
    "ساوجبلاغ",
    "زرندیه",
    "سوادکوه",
    "ثلاث باباجانی",
}


def normalize_fa(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).translate(ARABIC_TO_PERSIAN)
    text = text.replace("\u200c", " ").replace("ـ", "")
    return re.sub(r"\s+", " ", text).strip()


def coord_key(city: dict[str, Any]) -> tuple[float, float] | None:
    try:
        return round(float(city["latitude"]), 7), round(float(city["longitude"]), 7)
    except (KeyError, TypeError, ValueError):
        return None


def looks_auto_transliterated(value: Any) -> bool:
    text = str(value or "").strip()
    if not text:
        return False
    # Persian/Arabic marks leaking into an English field are always suspicious.
    if re.search(r"[\u0600-\u06ff]", text):
        return True
    letters = [ch for ch in text if ch.isalpha()]
    if len(letters) < 4:
        return False
    uppercase_ratio = sum(ch.isupper() for ch in letters) / len(letters)
    vowel_ratio = sum(ch.lower() in "aeiou" for ch in letters) / len(letters)
    return uppercase_ratio > 0.55 and vowel_ratio < 0.22


def audit(data: list[dict[str, Any]], provenance_path: Path) -> dict[str, Any]:
    facility_records: list[dict[str, Any]] = []
    admin_review: list[dict[str, Any]] = []
    weak_english: list[dict[str, Any]] = []
    missing_official_code = 0
    coordinate_groups: defaultdict[tuple[float, float], list[dict[str, Any]]] = defaultdict(list)

    for province in data:
        province_name = province.get("province")
        for city in province.get("cities", []):
            name = normalize_fa(city.get("name"))
            record = {"id": city.get("id"), "province": province_name, "name": city.get("name")}

            if any(pattern.search(name) for pattern in FACILITY_PATTERNS):
                facility_records.append(record)
            if name in ADMINISTRATIVE_REVIEW_NAMES:
                admin_review.append(record)
            if looks_auto_transliterated(city.get("english_name")):
                weak_english.append({**record, "english_name": city.get("english_name")})
            if not city.get("official_code"):
                missing_official_code += 1

            key = coord_key(city)
            if key is not None:
                coordinate_groups[key].append(record)

    duplicate_coordinates = [
        {"coordinates": list(key), "records": records}
        for key, records in coordinate_groups.items()
        if len(records) > 1
    ]

    provenance_status = "missing"
    if provenance_path.exists():
        try:
            provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
            provenance_status = provenance.get("current_legacy_dataset", {}).get("status", "present")
        except (json.JSONDecodeError, OSError):
            provenance_status = "invalid"

    return {
        "summary": {
            "provinces": len(data),
            "records": sum(len(p.get("cities", [])) for p in data),
            "facility_review": len(facility_records),
            "administrative_name_review": len(admin_review),
            "duplicate_coordinate_groups": len(duplicate_coordinates),
            "weak_english_names": len(weak_english),
            "records_without_official_code": missing_official_code,
            "provenance_status": provenance_status,
        },
        "facility_review": facility_records,
        "administrative_name_review": admin_review,
        "duplicate_coordinates": duplicate_coordinates,
        "weak_english_names": weak_english,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="iran_cities.json")
    parser.add_argument("--provenance", default="data/provenance.json")
    parser.add_argument("--json-output", help="Optional path for the full audit report")
    parser.add_argument("--strict", action="store_true", help="Fail if any semantic review item remains")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    report = audit(data, Path(args.provenance))
    summary = report["summary"]

    print("📊 Data audit")
    for key, value in summary.items():
        print(f"  {key}: {value}")

    if args.json_output:
        Path(args.json_output).write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    unresolved = (
        summary["facility_review"]
        + summary["administrative_name_review"]
        + summary["duplicate_coordinate_groups"]
        + summary["weak_english_names"]
        + summary["records_without_official_code"]
    )
    if args.strict and unresolved:
        print(f"❌ Strict audit failed: {unresolved} review item(s) remain.")
        return 1

    if unresolved:
        print("⚠️ Review items remain. This is expected for the legacy dataset; do not market it as authoritative.")
    else:
        print("✅ No audit review items found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
