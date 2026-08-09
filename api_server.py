#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only API for Iran provinces/cities data.

The built-in Flask server is for local development only. Production containers
run this application through Gunicorn (see Dockerfile).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable

from flask import Flask, jsonify, request
from flask_cors import CORS


APP_VERSION = "2.1.0"
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_FILE = BASE_DIR / "iran_cities.json"
DATA_FILE = Path(os.environ.get("IRAN_CITIES_DATA_FILE", str(DEFAULT_DATA_FILE))).expanduser().resolve()
MAX_PER_PAGE = 500
ARABIC_TO_PERSIAN = str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک"})

app = Flask(__name__)

# CORS is opt-in. Example:
#   CORS_ORIGINS=https://example.com,https://admin.example.com
cors_origins = [item.strip() for item in os.environ.get("CORS_ORIGINS", "").split(",") if item.strip()]
if cors_origins:
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})


def normalize_query(value: Any) -> str:
    """Normalize Persian/Arabic variants and whitespace for search matching."""
    text = unicodedata.normalize("NFKC", str(value or "")).translate(ARABIC_TO_PERSIAN)
    text = text.replace("\u200c", " ").replace("ـ", "")
    return re.sub(r"\s+", " ", text).strip().casefold()


def load_data(path: Path = DATA_FILE) -> tuple[list[dict[str, Any]], str]:
    """Load the configured dataset and return data plus SHA-256 fingerprint."""
    if not path.is_file():
        raise RuntimeError(f"Dataset not found: {path}")
    raw = path.read_bytes()
    try:
        data = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid dataset {path}: {exc}") from exc
    if not isinstance(data, list):
        raise RuntimeError(f"Dataset root must be an array: {path}")
    return data, hashlib.sha256(raw).hexdigest()


iran_data, DATASET_SHA256 = load_data()


def flatten_cities(data: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for province in data:
        for city in province.get("cities", []):
            item = dict(city)
            item["province_id"] = province.get("id")
            item["province_name"] = province.get("province")
            item["province_english_name"] = province.get("english_name")
            output.append(item)
    return output


ALL_CITIES = flatten_cities(iran_data)
PROVINCES_BY_ID = {p.get("id"): p for p in iran_data if isinstance(p.get("id"), int)}
CITIES_BY_ID = {c.get("id"): c for c in ALL_CITIES if isinstance(c.get("id"), int)}


def parse_positive_int(name: str, default: int, maximum: int | None = None) -> int:
    raw = request.args.get(name)
    if raw in (None, ""):
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    if maximum is not None:
        value = min(value, maximum)
    return value


def paginate(items: list[dict[str, Any]]) -> dict[str, Any]:
    page = parse_positive_int("page", 1)
    per_page = parse_positive_int("per_page", 100, MAX_PER_PAGE)
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (total + per_page - 1) // per_page if total else 0
    return {
        "data": items[start:end],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
            "has_next": end < total,
            "has_previous": page > 1 and total > 0,
        },
    }


def success(data: Any = None, **extra: Any):
    payload = {"success": True, "data": data}
    payload.update(extra)
    return jsonify(payload)


def failure(message: str, status: int, code: str):
    return jsonify({"success": False, "error": {"code": code, "message": message}}), status


@app.get("/")
def home():
    return jsonify({
        "name": "Iran Cities API",
        "version": APP_VERSION,
        "api": "/api/v1",
        "health": "/health",
        "documentation": "docs/API.md",
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "version": APP_VERSION,
        "dataset_sha256": DATASET_SHA256,
        "provinces": len(iran_data),
        "records": len(ALL_CITIES),
    })


@app.get("/api/v1/meta")
@app.get("/api/meta")
def meta():
    return success({
        "api_version": "v1",
        "application_version": APP_VERSION,
        "dataset_sha256": DATASET_SHA256,
        "provinces": len(iran_data),
        "records": len(ALL_CITIES),
        "data_status": "legacy-unverified" if not any(c.get("official_code") for c in ALL_CITIES) else "source-backed",
    })


@app.get("/api/v1/provinces")
@app.get("/api/provinces")
def get_provinces():
    provinces = [
        {
            "id": p.get("id"),
            "uid": p.get("uid"),
            "official_code": p.get("official_code"),
            "province": p.get("province"),
            "english_name": p.get("english_name"),
            "phone_code": p.get("phone_code"),
            "cities_count": len(p.get("cities", [])),
        }
        for p in iran_data
    ]
    return success(provinces, count=len(provinces))


@app.get("/api/v1/provinces/<int:province_id>")
@app.get("/api/provinces/<int:province_id>")
def get_province(province_id: int):
    province = PROVINCES_BY_ID.get(province_id)
    if province is None:
        return failure("Province not found", 404, "province_not_found")
    return success(province)


@app.get("/api/v1/cities")
@app.get("/api/cities")
def get_cities():
    items = ALL_CITIES
    province_id = request.args.get("province_id")
    query = normalize_query(request.args.get("q", ""))

    if province_id:
        try:
            province_id_int = int(province_id)
        except ValueError:
            return failure("province_id must be an integer", 400, "invalid_parameter")
        items = [c for c in items if c.get("province_id") == province_id_int]

    if query:
        items = [
            c
            for c in items
            if query in normalize_query(c.get("name"))
            or query in normalize_query(c.get("english_name"))
            or query in normalize_query(c.get("province_name"))
        ]

    try:
        result = paginate(items)
    except ValueError as exc:
        return failure(str(exc), 400, "invalid_parameter")
    return success(result["data"], pagination=result["pagination"])


@app.get("/api/v1/cities/<int:city_id>")
@app.get("/api/cities/<int:city_id>")
def get_city(city_id: int):
    city = CITIES_BY_ID.get(city_id)
    if city is None:
        return failure("City not found", 404, "city_not_found")
    return success(city)


@app.get("/api/v1/search")
@app.get("/api/search")
def search():
    query = normalize_query(request.args.get("q", ""))
    if not query:
        return failure('Query parameter "q" is required', 400, "missing_query")

    provinces = [
        {
            "id": p.get("id"),
            "province": p.get("province"),
            "english_name": p.get("english_name"),
        }
        for p in iran_data
        if query in normalize_query(p.get("province")) or query in normalize_query(p.get("english_name"))
    ]
    cities = [
        c
        for c in ALL_CITIES
        if query in normalize_query(c.get("name")) or query in normalize_query(c.get("english_name"))
    ]

    try:
        page = parse_positive_int("page", 1)
        per_page = parse_positive_int("per_page", 100, MAX_PER_PAGE)
    except ValueError as exc:
        return failure(str(exc), 400, "invalid_parameter")

    combined: list[dict[str, Any]] = [
        {"type": "province", **item} for item in provinces
    ] + [
        {"type": "city", **item} for item in cities
    ]
    total = len(combined)
    start = (page - 1) * per_page
    end = start + per_page
    return success(
        combined[start:end],
        query=request.args.get("q", ""),
        pagination={
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page if total else 0,
            "has_next": end < total,
            "has_previous": page > 1 and total > 0,
        },
    )


@app.errorhandler(404)
def not_found(_error):
    return failure("Endpoint not found", 404, "endpoint_not_found")


@app.errorhandler(405)
def method_not_allowed(_error):
    return failure("Method not allowed", 405, "method_not_allowed")


@app.errorhandler(500)
def internal_error(_error):
    return failure("Internal server error", 500, "internal_error")


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    app.run(host=host, port=port, debug=debug)
