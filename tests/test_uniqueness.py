#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uniqueness tests for the source-backed Iran city dataset."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path


TRANSLATE = str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک"})


def normalize(value):
    text = unicodedata.normalize("NFKC", str(value or "")).translate(TRANSLATE)
    text = text.replace("\u200c", " ").replace("ـ", "")
    return re.sub(r"\s+", " ", text).strip().casefold()


def load_data():
    return json.loads(Path("iran_cities.json").read_text(encoding="utf-8-sig"))


def test_province_identifiers_are_globally_unique():
    data = load_data()
    ids = [province["id"] for province in data]
    names = [normalize(province["province"]) for province in data]
    codes = [province.get("official_code") for province in data]
    uids = [province.get("uid") for province in data]

    assert len(ids) == len(set(ids))
    assert len(names) == len(set(names))
    assert all(codes) and len(codes) == len(set(codes))
    assert all(uids) and len(uids) == len(set(uids))


def test_city_ids_uids_and_official_codes_are_globally_unique():
    data = load_data()
    cities = [city for province in data for city in province["cities"]]
    ids = [city["id"] for city in cities]
    uids = [city.get("uid") for city in cities]
    codes = [city.get("official_code") for city in cities]

    assert len(ids) == len(set(ids)), "City numeric IDs must be globally unique"
    assert all(uids) and len(uids) == len(set(uids)), "City UIDs must be complete and unique"
    assert all(codes) and len(codes) == len(set(codes)), "Official source codes must be complete and unique"


def test_city_names_are_unique_within_source_county():
    data = load_data()

    for province in data:
        seen = set()
        for city in province["cities"]:
            key = (normalize(city.get("county")), normalize(city["name"]))
            assert key not in seen, (
                f"Duplicate normalized city name within county in {province['province']}: "
                f"{city.get('county')} / {city['name']}"
            )
            seen.add(key)


def test_declared_city_counts_match_and_canonical_total_is_1450():
    data = load_data()
    total = 0

    for province in data:
        actual = len(province["cities"])
        assert actual == province["cities_count"], (
            f"Cities count mismatch in {province['province']}: "
            f"declared {province['cities_count']}, actual {actual}"
        )
        total += actual

    assert len(data) == 31
    assert total == 1450
