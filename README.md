# Korea Garden Plant Finder

AI-assisted plant knowledge and planting design support for ecological and naturalistic planting.

## Project goals

1. Maintain structured botanical and horticultural plant data.
2. Recommend plants based on site conditions using explainable, rule-based scoring.
3. Generate an initial planting shortlist grouped by ecological and design criteria.
4. Keep the data-access layer replaceable so the project can later connect to the existing Korea Garden Plant Finder database.

> Important: This repository is an independent development scaffold. It does not modify or connect to the production 정원백과 database. The current production database schema, API, and hosting environment must be confirmed before integration.

## Current status

- [x] FastAPI application scaffold
- [x] Plant data model
- [x] CSV sample-data repository
- [x] Plant search endpoint
- [x] Explainable plant recommendation endpoint
- [x] Basic planting shortlist endpoint
- [x] Unit test example
- [ ] Production database adapter
- [ ] Verified botanical data import
- [ ] Authentication and authorization
- [ ] Frontend integration
- [ ] AI/LLM explanation layer with source-grounded outputs

## Architecture

```text
Client / Existing Website
          |
          v
     FastAPI routes
          |
          +----------------------+
          |                      |
          v                      v
 Plant recommendation      Planting design
          |                      |
          +----------+-----------+
                     |
                     v
              Plant repository
                     |
          +----------+-----------+
          |                      |
          v                      v
       CSV adapter        Future DB adapter
                               |
                               v
                   Existing 정원백과 database
```

The initial repository uses CSV sample data. Replace `CsvPlantRepository` with an adapter for the existing database only after its schema and access method have been verified.

## Requirements

- Python 3.10+
- pip

## Run locally

### 1. Create and activate a virtual environment

Windows CMD:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
```

PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the API

```bash
uvicorn app.main:app --reload
```

Open:

- API health: http://127.0.0.1:8000/health
- Interactive API docs: http://127.0.0.1:8000/docs
- Plant list: http://127.0.0.1:8000/plants

## API examples

### Search plants

```http
GET /plants?q=국화
```

Optional filters:

```http
GET /plants?sun=full_sun&moisture=medium
```

### Recommend plants for a site

```http
POST /recommend
Content-Type: application/json

{
  "sun": "full_sun",
  "moisture": "medium",
  "soil": "loam",
  "purpose": ["pollinator", "long_bloom"],
  "limit": 10
}
```

Each recommendation includes a score and reasons. The score is a transparent heuristic, not a scientifically validated suitability probability.

### Create a planting shortlist

```http
POST /planting-plan
Content-Type: application/json

{
  "site": {
    "sun": "full_sun",
    "moisture": "medium",
    "soil": "loam",
    "purpose": ["pollinator"]
  },
  "plant_count": 5
}
```

This endpoint creates a preliminary shortlist only. It does not calculate planting quantities, spacing, mature canopy coverage, or construction specifications.

## Plant data fields

The sample schema includes:

- `plant_id`: stable internal identifier
- `scientific_name`: scientific name
- `korean_name`: Korean common name
- `sun`: `full_sun`, `partial_shade`, `shade`, or `unknown`
- `moisture`: `dry`, `medium`, `moist`, `wet`, or `unknown`
- `soil`: `sand`, `loam`, `clay`, `varied`, or `unknown`
- `height_cm`: typical mature height in cm, if known
- `flowering_start_month`, `flowering_end_month`: approximate flowering period
- `purposes`: controlled tags such as `pollinator`, `groundcover`, `wetland`, `long_bloom`
- `native_status`: `native`, `introduced`, or `unknown`
- `data_source`, `data_confidence`: provenance and confidence metadata

Do not fill unknown values by guessing. Use `unknown` or leave optional numeric values blank, and record the source for verified facts.

## Data governance

For production use:

1. Keep the original source and source URL for each important trait.
2. Record the date checked and the person or process responsible for verification.
3. Distinguish measured data, published references, expert judgment, and AI-generated suggestions.
4. Never present an AI-generated value as verified botanical data.
5. Check source licensing and database reuse permissions before importing existing data.

## Tests

```bash
pytest
```

## Next integration step

Before connecting to the existing website, document:

- Current database engine and version
- Relevant table names and primary keys
- Existing plant identifier and taxonomy conventions
- Read-only API or database access method
- Hosting environment and deployment process

Do not put production passwords, API keys, or database credentials in GitHub. Use environment variables or a secret manager.
