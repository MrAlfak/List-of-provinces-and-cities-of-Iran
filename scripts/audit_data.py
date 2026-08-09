#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit source-backed membership and optional enrichment quality.

``--strict`` protects canonical membership: provenance must be source-backed and
every city must have a unique official source code. Coordinates, English names,
and duplicate coordinate points are enrichment warnings and do not invalidate
an otherwise source-backed city registry. Use ``--strict-enrichment`` when a
consumer specifically requires those optional fields to be clean as well.
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

FACILITY_PATTERNS = (
    re.compile(r"^مرز\s+"),
    re.compile(r"^پایانه\s+مرزی"),
)

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
        if city.get("latitude") is None or city.get("longitude") is None:
            return None
        return round(float(city["latitude"]), 7), round(float(city["longitude"]), 7)
    except (KeyError, TypeError, ValueError):
        return None


def looks_auto_transliterated(value: Any) -> bool:
    text = str(value or "").strip()
    if not text:
        return False
    if re.search(r"[\u0600-\u06ff]", text):
        return True
    letters = [ch for ch in text if ch.isalpha()]
    if len(letters) < 4:
        return False
    uppercase_ratio = sum(ch.isupper() for ch in letters) / len(letters)
    vowel_ratio = sum(ch.lower() in "aeiou" for ch in letters) / len(letters)
    return uppercase_ratio > 0.55 and vowel_ratio < 0.22


def read_provenance_status(path: Path) -> tuple[str, dict[str, Any]]:
    if not path.exists():
        return "missing", {}
    try:
        provenance = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return "invalid", {}
    canonical = provenance.get("canonical_dataset")
    if isinstance(canonical, dict):
        return str(canonical.get("status", "present")), canonical
    legacy = provenance.get("current_legacy_dataset")
    if isinstance(legacy, dict):
        return str(legacy.get("status", "legacy-unverified")), legacy
    return "present", {}


def audit(data: list[dict[str, Any]], provenance_path: Path) -> dict[str, Any]:
    facility_records: list[dict[str, Any]] = []
    admin_review: list[dict[str, Any]] = []
    weak_english: list[dict[str, Any]] = []
    missing_english = 0
    missing_coordinates = 0
    missing_official_code = 0
    official_codes: list[str] = []
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
            if not city.get("english_name"):
                missing_english += 1
            if city.get("latitude") is None or city.get("longitude") is None:
                missing_coordinates += 1

            code = city.get("official_code")
            if not code:
                missing_official_code += 1
            else:
                official_codes.append(str(code))

            key = coord_key(city)
            if key is not None:
                coordinate_groups[key].append(record)

    duplicate_coordinates = [
        {"coordinates": list(key), "records": records}
        for key, records in coordinate_groups.items()
        if len(records) > 1
    ]
    duplicate_official_codes = sorted(code for code, count in Counter(official_codes).items() if count > 1)
    provenance_status, canonical_meta = read_provenance_status(provenance_path)

    membership_blockers = (
        missing_official_code
        + len(duplicate_official_codes)
        + (0 if provenance_status == "source-backed" else 1)
    )
    enrichment_warnings = (
        len(duplicate_coordinates)
        + len(weak_english)
        + missing_english
        + missing_coordinates
    )

    return {
        "summary": {
            "provinces": len(data),
            "records": sum(len(p.get("cities", [])) for p in data),
            "membership_blockers": membership_blockers,
            "records_without_official_code": missing_official_code,
            "duplicate_official_codes": len(duplicate_official_codes),
            "provenance_status": provenance_status,
            "facility_review": len(facility_records),
            "administrative_name_review": len(admin_review),
            "duplicate_coordinate_groups": len(duplicate_coordinates),
            "weak_english_names": len(weak_english),
            "missing_english_names": missing_english,
            "missing_coordinates": missing_coordinates,
            "enrichment_warnings": enrichment_warnings,
            "snapshot_year_jalali": canonical_meta.get("snapshot_year_jalali"),
        },
        "duplicate_official_codes": duplicate_official_codes,
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
    parser.add_argument("--strict", action="store_true", help="Fail on source-membership/provenance blockers")
    parser.add_argument(
        "--strict-enrichment",
        action="store_true",
        help="Also fail on coordinate/English enrichment warnings",
    )
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

    if args.strict and summary["membership_blockers"]:
        print(f"❌ Strict membership audit failed: {summary['membership_blockers']} blocker(s).")
        return 1
    if args.strict_enrichment and summary["enrichment_warnings"]:
        print(f"❌ Strict enrichment audit failed: {summary['enrichment_warnings']} warning(s).")
        return 1

    if summary["membership_blockers"]:
        print("⚠️ Membership/provenance blockers remain; do not market this dataset as source-backed.")
    elif summary["enrichment_warnings"]:
        print("✅ Membership is source-backed; optional enrichment still has review items.")
    else:
        print("✅ Membership and enrichment audit are clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
