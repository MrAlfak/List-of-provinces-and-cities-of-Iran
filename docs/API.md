# Iran Cities API

The API is **read-only**. `/api/v1` is the stable namespace; legacy `/api/...` aliases remain for compatibility.

> The API exposes the checked-in dataset as-is. `/api/v1/meta` reports whether it is the legacy unverified snapshot or a source-backed rebuild. API availability does not make legacy records authoritative.

## Run

Development:

```bash
python -m pip install -r requirements.txt
python api_server.py
```

Container:

```bash
docker compose up --build
```

## Configuration

- `IRAN_CITIES_DATA_FILE`: absolute/relative path to the dataset; defaults to the repository JSON beside `api_server.py`.
- `HOST`: development-server bind host; defaults to `127.0.0.1`.
- `PORT`: defaults to `8000`.
- `FLASK_DEBUG`: disabled by default.
- `CORS_ORIGINS`: comma-separated allowed origins. CORS is disabled when unset.

## Endpoints

### `GET /health`

Returns process/dataset health, API version, dataset SHA-256, province count and record count.

### `GET /api/v1/meta`

Returns API/application version, dataset fingerprint and `data_status` (`legacy-unverified` or `source-backed`).

### `GET /api/v1/provinces`

Returns province summaries.

### `GET /api/v1/provinces/<id>`

Returns one province including its city records.

### `GET /api/v1/cities`

Query parameters:

- `page` — positive integer, default `1`.
- `per_page` — positive integer, default `100`, capped at `500`.
- `province_id` — optional numeric province filter.
- `q` — optional Persian/English search term.

Persian search normalizes Arabic/Persian kaf/yeh variants, ZWNJ, tatweel and repeated whitespace.

Example:

```text
GET /api/v1/cities?province_id=8&q=اسلام%20شهر&page=1&per_page=50
```

### `GET /api/v1/cities/<id>`

Returns a city/location record by its compatibility numeric ID.

### `GET /api/v1/search?q=<query>`

Searches province and city names and returns paginated mixed results with a `type` field.

## Response shape

Successful collection response:

```json
{
  "success": true,
  "data": [],
  "pagination": {
    "page": 1,
    "per_page": 100,
    "total": 0,
    "total_pages": 0,
    "has_next": false,
    "has_previous": false
  }
}
```

Error response:

```json
{
  "success": false,
  "error": {
    "code": "invalid_parameter",
    "message": "page must be greater than zero"
  }
}
```

## Compatibility

The following legacy aliases remain available in v2.1:

```text
/api/provinces
/api/provinces/<id>
/api/cities
/api/cities/<id>
/api/search
/api/meta
```

New integrations should use `/api/v1`.

## Production notes

Do not run Flask's built-in development server as an internet-facing service. The provided Docker image uses Gunicorn. Configure CORS explicitly and put TLS, request limits, observability and any public rate-limiting policy at the deployment layer.
