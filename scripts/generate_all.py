#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate all derived distribution formats from the canonical JSON file."""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running this file directly from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.generate_csv import generate_csv
from scripts.generate_geojson import generate_geojson
from scripts.generate_minified import generate_minified
from scripts.generate_sql import generate_sql


def main() -> int:
    print("🚀 Generating derived formats...\n")
    try:
        Path("iran_cities.mysql.sql").write_text(generate_sql("mysql"), encoding="utf-8")
        print("✅ iran_cities.mysql.sql")

        Path("iran_cities.postgresql.sql").write_text(generate_sql("postgresql"), encoding="utf-8")
        print("✅ iran_cities.postgresql.sql")

        generate_csv()
        generate_geojson()
        generate_minified()

        print("\n✅ All derived formats generated successfully.")
        return 0
    except Exception as exc:
        print(f"\n❌ Generation failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
