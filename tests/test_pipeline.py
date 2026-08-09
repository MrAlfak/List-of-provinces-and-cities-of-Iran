import json

from api_server import normalize_query
from scripts.audit_data import audit
from scripts.generate_sql import quote
from scripts.rebuild_from_amar_1402 import derived_subarea_base, split_city_rows
from scripts.remove_duplicates import find_exact_duplicates, remove_exact_duplicates
from scripts.validate_data import validate_data


def test_same_coordinates_do_not_make_different_names_duplicates():
    data = [
        {
            "province": "نمونه",
            "cities": [
                {"id": 1, "name": "شهر الف", "latitude": "35.0", "longitude": "51.0"},
                {"id": 2, "name": "شهر ب", "latitude": "35.0", "longitude": "51.0"},
            ],
        }
    ]
    assert find_exact_duplicates(data) == []
    assert remove_exact_duplicates(data) == 0
    assert len(data[0]["cities"]) == 2


def test_only_exact_normalized_duplicate_is_removed():
    data = [
        {
            "province": "نمونه",
            "cities": [
                {"id": 1, "name": "اسلام‌شهر", "latitude": "35.5", "longitude": "51.2"},
                {"id": 2, "name": "اسلام شهر", "latitude": 35.5, "longitude": 51.2},
                {"id": 3, "name": "اسلام شهر", "latitude": 35.6, "longitude": 51.2},
            ],
        }
    ]
    assert len(find_exact_duplicates(data)) == 1
    assert remove_exact_duplicates(data) == 1
    assert [city["id"] for city in data[0]["cities"]] == [1, 3]


def test_sql_literal_escapes_apostrophes():
    assert quote("Sowme'eh Sara") == "'Sowme''eh Sara'"
    assert quote(None) == "NULL"


def test_persian_search_normalization():
    assert normalize_query("ك ي  شهر") == normalize_query("ک ی شهر")
    assert normalize_query("اسلام‌شهر") == normalize_query("اسلام شهر")


def test_validator_rejects_global_duplicate_city_id():
    data = [
        {
            "id": 1,
            "province": "الف",
            "cities_count": 1,
            "cities": [
                {
                    "id": 10,
                    "name": "الف‌شهر",
                    "is_capital": True,
                    "latitude": 35,
                    "longitude": 51,
                    "english_name": "A",
                }
            ],
        },
        {
            "id": 2,
            "province": "ب",
            "cities_count": 1,
            "cities": [
                {
                    "id": 10,
                    "name": "ب‌شهر",
                    "is_capital": True,
                    "latitude": 36,
                    "longitude": 52,
                    "english_name": "B",
                }
            ],
        },
    ]
    errors, _warnings, _stats = validate_data(data, expected_provinces=None)
    assert any("Duplicate global city id 10" in error for error in errors)


def source_row(name, county="نمونه", code=1000):
    return {
        "کد استان": 1,
        "نام استان": "استان نمونه",
        "کد شهرستان": 1,
        "نام شهرستان": county,
        "کد بخش": 1,
        "نام بخش": "مرکزی",
        "کد دهستان/ شهر": code,
        "CODEREC": 5,
        "نام": name,
    }


def test_1402_numeric_subareas_are_excluded_only_when_base_city_exists_same_county():
    rows = [
        source_row("تبریز", code=1),
        source_row("تبریز 1", code=2),
        source_row("تبریز2-", code=3),
        source_row("اسلامشهر", code=4),
        source_row("اسلام شهر6", code=5),
        source_row("فاز 2", county="شهرستان دیگر", code=6),
    ]
    canonical, excluded = split_city_rows(rows)
    assert {r["نام"] for r in excluded} == {"تبریز 1", "تبریز2-", "اسلام شهر6"}
    assert {r["نام"] for r in canonical} == {"تبریز", "اسلامشهر", "فاز 2"}


def test_1402_named_municipal_subarea_requires_base_city_in_same_county():
    rows = [
        source_row("یزد", code=1),
        source_row("یزد_منطقه تاریخی", code=2),
        source_row("آزاد_منطقه تاریخی", county="شهرستان دیگر", code=3),
    ]
    canonical, excluded = split_city_rows(rows)
    assert [r["نام"] for r in excluded] == ["یزد_منطقه تاریخی"]
    assert {r["نام"] for r in canonical} == {"یزد", "آزاد_منطقه تاریخی"}
    assert derived_subarea_base("یزد_منطقه تاریخی") == "یزد"


def test_strict_membership_audit_ignores_optional_enrichment(tmp_path):
    provenance = tmp_path / "provenance.json"
    provenance.write_text(
        json.dumps({"canonical_dataset": {"status": "source-backed", "snapshot_year_jalali": 1402}}),
        encoding="utf-8",
    )
    data = [
        {
            "province": "نمونه",
            "cities": [
                {
                    "id": 1,
                    "name": "شهر",
                    "official_code": "1402:01:001:001:0001",
                    "english_name": None,
                    "latitude": None,
                    "longitude": None,
                }
            ],
        }
    ]
    report = audit(data, provenance)
    assert report["summary"]["membership_blockers"] == 0
    assert report["summary"]["enrichment_warnings"] == 2
