from api_server import normalize_query
from scripts.generate_sql import quote
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
