# Track A Runtime Validity

Reference implementation for experiments in runtime validity and revalidation
before consequential AI actions.

## Current Status

Early engineering and research implementation.

The current executable behavior establishes a minimal decision API boundary:

```text
POST /decide
valid request
→ PROCEED
```

This behavior does not yet implement runtime governance or revalidation logic.

## Requirements

- Python 3.12 or newer

## Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/getkeystone/track-a-runtime-validity.git
cd track-a-runtime-validity
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Run the API

Start the development server:

```bash
python -m uvicorn track_a.api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Exercise `/decide`

Send a valid request:

```bash
curl -i \
  -X POST \
  http://127.0.0.1:8000/decide \
  -H "Content-Type: application/json" \
  -d '{
    "action_proposal": "send customer notification",
    "prior_decision_id": "decision-123",
    "revalidation_mode": "full"
  }'
```

Expected response:

```text
HTTP/1.1 200 OK
```

```json
{"outcome":"PROCEED"}
```

## Run Tests

```bash
python -m pytest -v
```

Current automated coverage verifies:

- valid `/decide` requests return HTTP 200 and `PROCEED`
- invalid `revalidation_mode` values return HTTP 422

## Project Structure

```text
track-a-runtime-validity/
├── docs/
│   └── increments/
│       └── 001-executable-boundary.md
├── src/
│   └── track_a/
│       ├── __init__.py
│       └── api.py
├── tests/
│   └── test_api.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Scope

The current implementation establishes an executable and validated HTTP
boundary.

It does not yet provide evidence of:

- governance decision correctness
- material-change detection
- obligation-scoped revalidation
- stateful authorization
- action-boundary enforcement
- evidence reconstruction
