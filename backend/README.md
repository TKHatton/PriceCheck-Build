# PriceCheck Backend

FastAPI backend with LangGraph agent pipeline for analyzing pricing manipulation tactics.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
```
GET /health
Returns: {"status": "ok"}
```

### Analyze
```
POST /analyze
Content-Type: application/json

Request body:
{
  "input_type": "page",
  "page_url": "https://example.com/product",
  "page_title": "Product Name",
  "body_text": "Page content...",
  "price_elements": [],
  "raw_image": null,
  "manual_text": null
}

Response:
{
  "gaslighting_score": 0-100,
  "severity_label": "Honest Pricing",
  "tactics": [...],
  "trust_score": 0-100,
  "trust_signals": [...],
  "is_scam": false,
  "marketed_price": 99.99,
  "real_price": 99.99,
  "price_delta": 0,
  "error": null
}
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app, routes, CORS
│   ├── models/
│   │   └── schemas.py       # Pydantic request/response models
│   ├── graph/
│   │   ├── state.py         # PriceCheckState TypedDict
│   │   ├── graph.py         # LangGraph pipeline (TODO)
│   │   ├── nodes.py         # Node functions (TODO)
│   │   └── edges.py         # Edge routers (TODO)
│   ├── services/
│   │   ├── trust.py         # Domain trust checks (TODO)
│   │   └── claude.py        # Claude API wrapper (TODO)
│   └── prompts/
│       └── analysis.py      # System prompts (TODO)
├── requirements.txt
├── .env.example
└── README.md
```

## Development Status

- [x] FastAPI app structure
- [x] CORS configuration
- [x] Health endpoint
- [x] Request/response schemas
- [x] State definition
- [ ] LangGraph pipeline
- [ ] Trust layer integration
- [ ] Claude analysis node
- [ ] Scoring algorithm

## CORS Configuration

The API accepts requests from:
- `chrome-extension://*` (Chrome extension)
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative dev server)
