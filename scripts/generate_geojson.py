#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate GeoJSON from canonical Iran city data.

GeoJSON can only represent point features for records with usable coordinates.
Canonical city membership does not depend on coordinate enrichment, so cities
with missing/invalid coordinates are skipped and counted in metadata instead of
crashing generation or fabricating a location.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any


INPUT = Path("iran_cities.json")
OUTPUT = Path("iran_cities.geojson")


def load_data() -> list[dict[str, Any]]:
    return json.loads(INPUT.read_text(encoding="utf-8-sig"))


def point_coordinates(city: dict[str, Any]) -> list[float] | None:
    lat = city.get("latitude")
    lon = city.get("longitude")
    if lat is None or lon is None:
        return None
    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except (TypeError, ValueError):
        return None
    if not (math.isfinite(lat_f) and math.isfinite(lon_f)):
        return None
    return [lon_f, lat_f]


def generate_geojson() -> dict[str, int]:
    data = load_data()
    features: list[dict[str, Any]] = []
    canonical_total = 0
    skipped = 0

    for province in data:
        for city in province.get("cities", []):
            canonical_total += 1
            coordinates = point_coordinates(city)
            if coordinates is None:
                skipped += 1
                continue

            features.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": coordinates},
                    "properties": {
                        "id": city.get("id"),
                        "uid": city.get("uid"),
                        "official_code": city.get("official_code"),
                        "name": city.get("name"),
                        "english_name": city.get("english_name"),
                        "is_capital": city.get("is_capital", False),
                        "population": city.get("population"),
                        "postal_code": city.get("postal_code"),
                        "county": city.get("county"),
                        "district": city.get("district"),
                        "province_id": province.get("id"),
                        "province_uid": province.get("uid"),
                        "province": province.get("province"),
                        "province_english": province.get("english_name"),
                        "phone_code": province.get("phone_code"),
                    },
                }
            )

    geojson = {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "title": "Iran Cities (geocoded subset)",
            "description": (
                "Point features for canonical city records that currently have coordinate enrichment. "
                "See iran_cities.json for the complete source-backed city membership."
            ),
            "canonical_total_cities": canonical_total,
            "geocoded_features": len(features),
            "skipped_without_coordinates": skipped,
        },
    }
    OUTPUT.write_text(json.dumps(geojson, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "canonical_total_cities": canonical_total,
        "geocoded_features": len(features),
        "skipped_without_coordinates": skipped,
    }


if __name__ == "__main__":
    print("🔄 Generating GeoJSON file...")
    try:
        stats = generate_geojson()
        print(
            "✅ GeoJSON generated: "
            f"{stats['geocoded_features']} geocoded / {stats['canonical_total_cities']} canonical; "
            f"{stats['skipped_without_coordinates']} skipped without coordinates"
        )
    except Exception as exc:
        print(f"❌ Error: {exc}")
        sys.exit(1)
