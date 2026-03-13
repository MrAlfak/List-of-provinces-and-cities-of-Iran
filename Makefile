.PHONY: help install test generate clean run validate stats docker-build docker-run all

help:
	@echo "🇮🇷 Iran Cities Data - دستورات موجود | Available Commands"
	@echo ""
	@echo "  make install       - نصب وابستگی‌ها | Install dependencies"
	@echo "  make test          - اجرای تست‌ها | Run all tests"
	@echo "  make generate      - تولید فایل‌ها | Generate all formats"
	@echo "  make validate      - اعتبارسنجی | Validate data"
	@echo "  make stats         - نمایش آمار | Show statistics"
	@echo "  make run           - اجرای API | Run API server"
	@echo "  make clean         - پاک‌سازی | Clean generated files"
	@echo "  make docker-build  - ساخت Docker | Build Docker image"
	@echo "  make docker-run    - اجرای Docker | Run Docker container"
	@echo "  make all           - انجام همه | Do everything"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v
	@echo "✅ All tests passed"

generate:
	@echo "🔄 Generating all formats..."
	python scripts/generate_all.py
	@echo "✅ All formats generated"

validate:
	@echo "🔍 Validating data..."
	python scripts/validate_data.py
	@echo "✅ Data validated"

stats:
	@echo "📊 Showing statistics..."
	python scripts/stats.py

run:
	@echo "🚀 Starting API server..."
	python api_server.py

clean:
	@echo "🧹 Cleaning generated files..."
	rm -f iran_cities.min.json
	rm -f iran_cities.sql
	rm -f iran_cities.csv
	rm -f iran_cities.geojson
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned"

docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t iran-cities-api .
	@echo "✅ Docker image built"

docker-run:
	@echo "🐳 Running Docker container..."
	docker run -p 8000:8000 iran-cities-api

all: install generate validate test
	@echo "✅ همه کارها با موفقیت انجام شد!"
	@echo "✅ All tasks completed successfully!"

