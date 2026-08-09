.PHONY: help install test generate clean run validate audit stats docker-build docker-run docker-test all

help:
	@echo "🇮🇷 Iran Cities Data - Available commands"
	@echo "  make install       Install dependencies"
	@echo "  make validate      Validate structural integrity"
	@echo "  make audit         Report semantic/enrichment data debt"
	@echo "  make test          Run regression tests"
	@echo "  make generate      Generate CSV/GeoJSON/minified/SQL outputs"
	@echo "  make stats         Show dataset statistics"
	@echo "  make run           Run local Flask development server"
	@echo "  make docker-build  Build production-style API image"
	@echo "  make docker-run    Run API image on port 8000"
	@echo "  make docker-test   Smoke-test container health endpoint"
	@echo "  make clean         Remove generated artifacts/caches"
	@echo "  make all           Validate, audit, test and generate"

install:
	python -m pip install -r requirements.txt

validate:
	python scripts/validate_data.py

audit:
	python scripts/audit_data.py

test:
	python -m pytest tests/ -v

generate:
	python scripts/generate_all.py

stats:
	python scripts/stats.py

run:
	python api_server.py

clean:
	rm -f iran_cities.min.json iran_cities.mysql.sql iran_cities.postgresql.sql iran_cities.csv iran_cities.geojson
	rm -f data/audit-report.json
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t iran-cities-api .

docker-run:
	docker run --rm -p 8000:8000 iran-cities-api

docker-test: docker-build
	docker run -d --rm --name iran-cities-api-test -p 18000:8000 iran-cities-api
	@python -c "import time,urllib.request; time.sleep(1); print(urllib.request.urlopen('http://127.0.0.1:18000/health', timeout=5).read().decode())"
	docker stop iran-cities-api-test

all: validate audit test generate
	@echo "✅ Validation, audit, tests and generation completed."
