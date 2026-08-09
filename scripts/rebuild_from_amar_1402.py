#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild Iran's city dataset from the SCI 1402 administrative snapshot.

The source snapshot is the raw country-division export mirrored by
``sajaddp/list-of-cities-in-Iran`` from the Statistical Center of Iran (SCI).
The mirror contains municipal subarea rows with ``CODEREC == 5`` (for example
``اراک 1`` and ``تبریز1-``) in addition to independent cities.  We therefore
exclude a numbered/municipal subarea *only* when its derived base name exists
as another CODEREC=5 record in the same province and county.  This keeps the
rule source-relative and avoids a hand-maintained deletion list.

The canonical 1402 snapshot pinned by this repository contains:
- 1,659 raw CODEREC=5 rows
- 209 source-relative urban subareas
- 1,450 independent city records

Legacy numeric IDs, English names and coordinates are retained when an
unambiguous province+city match exists.  Coordinates/English names are only
enrichment and never determine membership.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any


SOURCE_REPOSITORY = "sajaddp/list-of-cities-in-Iran"
SOURCE_COMMIT = "474942269f75ec247e1af5684f5e3eca9f304431"
SOURCE_PATH = "offical/list.json"
SOURCE_YEAR_JALALI = 1402
EXPECTED_RAW_CITY_ROWS = 1659
EXPECTED_EXCLUDED_SUBAREAS = 209
EXPECTED_CANONICAL_CITIES = 1450

TRANSLATE = str.maketrans(
    {
        "ي": "ی",
        "ى": "ی",
        "ك": "ک",
        "۰": "0",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
    }
)
NUMERIC_SUBAREA_RE = re.compile(r"^(.*?)[\s_\-–—]*(\d+)[\s_\-–—]*$")
NAMED_SUBAREA_RE = re.compile(r"^(.*?)[\s_\-–—]+(?:منطقه|ناحیه|شهرداری|حوزه)\b.*$")


def normalize_fa(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).translate(TRANSLATE)
    text = text.replace("\u200c", " ").replace("ـ", "")
    return re.sub(r"\s+", " ", text).strip()


def compact_fa(value: Any) -> str:
    return re.sub(r"[^0-9A-Za-z\u0600-\u06ff]+", "", normalize_fa(value)).casefold()


def as_int(value: Any) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def source_city_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (
        compact_fa(row.get("نام استان")),
        compact_fa(row.get("نام شهرستان")),
        compact_fa(row.get("نام")),
    )


def source_county_key(row: dict[str, Any]) -> tuple[str, str]:
    return compact_fa(row.get("نام استان")), compact_fa(row.get("نام شهرستان"))


def derived_subarea_base(name: Any) -> str | None:
    normalized = normalize_fa(name)
    match = NUMERIC_SUBAREA_RE.match(normalized)
    if match:
        return match.group(1).strip(" _-–—")
    match = NAMED_SUBAREA_RE.match(normalized)
    if match:
        return match.group(1).strip(" _-–—")
    return None


def split_city_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    raw_cities = [row for row in rows if as_int(row.get("CODEREC")) == 5]
    existing = {source_city_key(row) for row in raw_cities}
    canonical: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    for row in raw_cities:
        base = derived_subarea_base(row.get("نام"))
        if base:
            base_key = (*source_county_key(row), compact_fa(base))
            if base_key in existing:
                excluded.append(row)
                continue
        canonical.append(row)

    return canonical, excluded


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_legacy(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    data = load_json(path)
    if not isinstance(data, list):
        raise ValueError("Legacy JSON must be a top-level province array")
    return data


def legacy_indexes(legacy: list[dict[str, Any]]):
    provinces: dict[str, dict[str, Any]] = {}
    exact_cities: dict[tuple[str, str], dict[str, Any]] = {}
    compact_candidates: defaultdict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    max_province_id = 0
    max_city_id = 0

    for province in legacy:
        pkey = compact_fa(province.get("province"))
        provinces[pkey] = province
        if isinstance(province.get("id"), int):
            max_province_id = max(max_province_id, province["id"])
        for city in province.get("cities", []):
            exact_cities[(pkey, normalize_fa(city.get("name")).casefold())] = city
            compact_candidates[(pkey, compact_fa(city.get("name")))].append(city)
            if isinstance(city.get("id"), int):
                max_city_id = max(max_city_id, city["id"])

    return provinces, exact_cities, compact_candidates, max_province_id, max_city_id


def match_legacy_city(
    province_key: str,
    name: str,
    exact: dict[tuple[str, str], dict[str, Any]],
    compact: dict[tuple[str, str], list[dict[str, Any]]],
) -> dict[str, Any]:
    hit = exact.get((province_key, normalize_fa(name).casefold()))
    if hit:
        return hit
    candidates = compact.get((province_key, compact_fa(name)), [])
    return candidates[0] if len(candidates) == 1 else {}


def code_piece(value: Any, width: int) -> str:
    number = as_int(value)
    if number is None:
        raise ValueError(f"Missing/invalid source code component: {value!r}")
    return str(number).zfill(width)


def official_city_code(row: dict[str, Any]) -> str:
    return ":".join(
        [
            str(SOURCE_YEAR_JALALI),
            code_piece(row.get("کد استان"), 2),
            code_piece(row.get("کد شهرستان"), 3),
            code_piece(row.get("کد بخش"), 3),
            code_piece(row.get("کد دهستان/ شهر"), 4),
        ]
    )


def rebuild(rows: list[dict[str, Any]], legacy: list[dict[str, Any]]):
    canonical_rows, excluded_rows = split_city_rows(rows)
    if len([r for r in rows if as_int(r.get("CODEREC")) == 5]) != EXPECTED_RAW_CITY_ROWS:
        raise ValueError("Pinned source raw city-row count changed; inspect source before rebuilding")
    if len(excluded_rows) != EXPECTED_EXCLUDED_SUBAREAS:
        raise ValueError("Pinned source urban-subarea count changed; inspect exclusion rule")
    if len(canonical_rows) != EXPECTED_CANONICAL_CITIES:
        raise ValueError("Pinned source canonical city count changed")

    old_provinces, old_exact, old_compact, max_province_id, max_city_id = legacy_indexes(legacy)
    next_province_id = max_province_id + 1
    next_city_id = max_city_id + 1

    grouped: defaultdict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in canonical_rows:
        province_code = as_int(row.get("کد استان"))
        province_name = normalize_fa(row.get("نام استان"))
        if province_code is None or not province_name:
            raise ValueError(f"Invalid province fields in source row: {row!r}")
        grouped[(province_code, province_name)].append(row)

    output: list[dict[str, Any]] = []
    matched_legacy_cities = 0

    for (province_code, province_name), city_rows in sorted(grouped.items(), key=lambda x: x[0][0]):
        pkey = compact_fa(province_name)
        old_province = old_provinces.get(pkey, {})
        old_pid = old_province.get("id")
        if isinstance(old_pid, int):
            province_id = old_pid
        else:
            province_id = next_province_id
            next_province_id += 1

        province_uid = old_province.get("uid") or f"ir:province:{SOURCE_YEAR_JALALI}:{province_code:02d}"
        province = {
            "id": province_id,
            "uid": province_uid,
            "official_code": f"{SOURCE_YEAR_JALALI}:{province_code:02d}",
            "province": province_name,
            "english_name": old_province.get("english_name"),
            "phone_code": old_province.get("phone_code"),
            "cities_count": 0,
            "last_updated": str(SOURCE_YEAR_JALALI),
            "cities": [],
        }

        for row in sorted(
            city_rows,
            key=lambda r: (
                as_int(r.get("کد شهرستان")) or -1,
                as_int(r.get("کد بخش")) or -1,
                as_int(r.get("کد دهستان/ شهر")) or -1,
                normalize_fa(r.get("نام")),
            ),
        ):
            name = normalize_fa(row.get("نام"))
            old = match_legacy_city(pkey, name, old_exact, old_compact)
            old_cid = old.get("id")
            if isinstance(old_cid, int):
                city_id = old_cid
                matched_legacy_cities += 1
            else:
                city_id = next_city_id
                next_city_id += 1

            source_code = official_city_code(row)
            province["cities"].append(
                {
                    "id": city_id,
                    "uid": old.get("uid") or f"ir:city:{source_code}",
                    "official_code": source_code,
                    "name": name,
                    "english_name": old.get("english_name"),
                    "latitude": old.get("latitude"),
                    "longitude": old.get("longitude"),
                    "is_capital": bool(old.get("is_capital", False)),
                    "population": old.get("population"),
                    "postal_code": old.get("postal_code"),
                    "county": normalize_fa(row.get("نام شهرستان")) or None,
                    "county_code": code_piece(row.get("کد شهرستان"), 3),
                    "district": normalize_fa(row.get("نام بخش")) or None,
                    "district_code": code_piece(row.get("کد بخش"), 3),
                }
            )

        province["cities_count"] = len(province["cities"])
        output.append(province)

    stats = {
        "provinces": len(output),
        "raw_coderec5_rows": EXPECTED_RAW_CITY_ROWS,
        "excluded_urban_subareas": len(excluded_rows),
        "cities": sum(p["cities_count"] for p in output),
        "legacy_enriched_cities": matched_legacy_cities,
    }
    return output, excluded_rows, stats


def write_provenance(path: Path, source_path: Path, stats: dict[str, int]) -> None:
    digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
    provenance = {
        "schema_version": 2,
        "canonical_membership_rule": (
            "Use CODEREC=5 records from the pinned SCI 1402 administrative snapshot, "
            "excluding a municipal subarea only when its numbered/named base resolves "
            "to another CODEREC=5 city in the same province and county."
        ),
        "canonical_dataset": {
            "path": "iran_cities.json",
            "status": "source-backed",
            "snapshot_year_jalali": SOURCE_YEAR_JALALI,
            "publisher": "Statistical Center of Iran",
            "official_source_page": "https://amar.org.ir/geo",
            "mirror_repository": SOURCE_REPOSITORY,
            "mirror_commit": SOURCE_COMMIT,
            "mirror_path": SOURCE_PATH,
            "source_sha256": digest,
            "source_license": "GPL-3.0-only (redistributed mirror/data derivatives)",
            "raw_coderec5_rows": stats["raw_coderec5_rows"],
            "excluded_urban_subareas": stats["excluded_urban_subareas"],
            "canonical_city_count": stats["cities"],
            "note": (
                "Membership is source-backed as of 1402. Coordinates and English names are legacy "
                "enrichment and may be null or require separate review. Later country-division "
                "decisions are not represented until a newer source snapshot is imported."
            ),
        },
        "refresh_policy": {
            "required_evidence": [
                "publisher/source URL or archival identifier",
                "snapshot date/year",
                "source checksum",
                "pinned mirror/source revision when a mirror is used",
                "import command and importer version",
                "validation and audit reports",
            ],
            "forbidden_shortcuts": [
                "using this repository's generated JSON as its own upstream source",
                "classifying a record as a city from coordinates alone",
                "deleting records only because coordinates or aliases are similar",
                "removing a numbered record unless its base city exists in the same source county",
            ],
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-json", required=True, help="Pinned SCI 1402 raw list.json")
    parser.add_argument("--legacy-json", default="iran_cities.json", help="Legacy enrichment source")
    parser.add_argument("--output", default="iran_cities.json")
    parser.add_argument("--provenance", default="data/provenance.json")
    parser.add_argument("--excluded-report", default="data/excluded-urban-subareas-1402.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_path = Path(args.source_json)
    rows = load_json(source_path)
    if not isinstance(rows, list):
        raise ValueError("SCI source JSON must be a top-level row array")

    legacy_path = Path(args.legacy_json) if args.legacy_json else None
    legacy = load_legacy(legacy_path)
    rebuilt, excluded, stats = rebuild(rows, legacy)

    Path(args.output).write_text(json.dumps(rebuilt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    Path(args.excluded_report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.excluded_report).write_text(
        json.dumps(
            [
                {
                    "name": normalize_fa(row.get("نام")),
                    "province": normalize_fa(row.get("نام استان")),
                    "county": normalize_fa(row.get("نام شهرستان")),
                    "source_city_code": row.get("کد دهستان/ شهر"),
                    "derived_base": derived_subarea_base(row.get("نام")),
                }
                for row in excluded
            ],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_provenance(Path(args.provenance), source_path, stats)
    print(json.dumps(stats, ensure_ascii=False, indent=2))

    if stats["provinces"] != 31 or stats["cities"] != EXPECTED_CANONICAL_CITIES:
        print("❌ Rebuild invariants failed")
        return 1
    print("✅ Rebuilt source-backed SCI 1402 city snapshot")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
