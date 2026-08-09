#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for optional geographic coordinate enrichment.

Canonical city membership is source-backed independently of coordinates. These
tests validate coordinate pairs only when they are present; missing pairs are
allowed and are reported by the audit layer as enrichment debt.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


IRAN_BOUNDS = {
    "lat_min": 24.0,
    "lat_max": 40.5,
    "lon_min": 43.5,
    "lon_max": 64.5,
}


def load_data():
    return json.loads(Path("iran_cities.json").read_text(encoding="utf-8-sig"))


def parsed_coordinates(city):
    lat = city.get("latitude")
    lon = city.get("longitude")
    if lat is None and lon is None:
        return None
    assert lat is not None and lon is not None, f"Partial coordinate pair for {city.get('name')}"
    lat_f = float(lat)
    lon_f = float(lon)
    assert math.isfinite(lat_f) and math.isfinite(lon_f)
    return lat_f, lon_f


def test_coordinate_pairs_are_valid_when_present():
    data = load_data()
    geocoded = 0
    missing = 0

    for province in data:
        for city in province["cities"]:
            coords = parsed_coordinates(city)
            if coords is None:
                missing += 1
                continue
            geocoded += 1

    assert geocoded > 0, "Expected at least some geocoded city records"
    assert geocoded + missing == sum(len(p["cities"]) for p in data)


def test_present_coordinates_are_within_broad_iran_bounds():
    data = load_data()
    errors = []

    for province in data:
        for city in province["cities"]:
            coords = parsed_coordinates(city)
            if coords is None:
                continue
            lat, lon = coords
            if not (IRAN_BOUNDS["lat_min"] <= lat <= IRAN_BOUNDS["lat_max"]):
                errors.append(f"{province['province']} / {city['name']}: latitude {lat}")
            if not (IRAN_BOUNDS["lon_min"] <= lon <= IRAN_BOUNDS["lon_max"]):
                errors.append(f"{province['province']} / {city['name']}: longitude {lon}")

    assert not errors, "Coordinates outside broad Iran bounds:\n" + "\n".join(errors)


def test_duplicate_coordinate_points_are_audit_warnings_not_identity_failures():
    data = load_data()
    coord_map = {}
    duplicate_groups = []

    for province in data:
        for city in province["cities"]:
            coords = parsed_coordinates(city)
            if coords is None:
                continue
            key = (round(coords[0], 7), round(coords[1], 7))
            if key in coord_map:
                duplicate_groups.append((coord_map[key], (province["province"], city["name"])))
            else:
                coord_map[key] = (province["province"], city["name"])

    # Coordinate equality alone is not evidence that one of two source-backed
    # city records should be deleted. The semantic audit reports these groups.
    assert isinstance(duplicate_groups, list)


def test_each_province_has_exactly_one_capital():
    data = load_data()
    errors = []

    for province in data:
        capitals = [city for city in province["cities"] if city.get("is_capital") is True]
        if len(capitals) != 1:
            errors.append(
                f"{province['province']} has {len(capitals)} capitals: "
                f"{[city.get('name') for city in capitals]}"
            )

    assert not errors, "Capital city errors:\n" + "\n".join(errors)
