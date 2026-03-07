# Trust Layer Implementation

## Overview

The trust checking service evaluates domain legitimacy using 4 signals. Trust score starts at 100 and deductions are applied for each red flag detected.

## Implementation

**File**: `app/services/trust.py`

### Signals

| Signal | Deduction | Trigger |
|--------|-----------|---------|
| **Domain Age** | -35 | Domain registered < 90 days (requires WHOIS_API_KEY) |
| **Brand Mismatch** | -40 | Page claims to be major brand but domain doesn't match official site |
| **Price Implausibility** | -20 | Prices >70% off (e.g., "85% off" or "Was $299 now $49") |
| **Contact Legitimacy** | -25 | Business contact uses free email (@gmail.com, @yahoo.com, etc.) |

### Trust Score Thresholds

| Score Range | Outcome | Behavior |
|-------------|---------|----------|
| **0-29** | SCAM | Sets `is_scam=True`, `gaslighting_score=95`, routes directly to output (skips analysis) |
| **30-69** | WARNING | Shows amber notice, continues analysis |
| **70-100** | PASS | No notice, normal analysis |

## Test Results

### Scam Site (Score: 15)
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "page",
    "page_url": "https://nike-clearance-outlet.shop",
    "page_title": "Nike Official - 95% OFF All Shoes",
    "body_text": "Contact: sales@gmail.com. Everything 95% off!",
    "price_elements": []
  }'
```

**Response:**
```json
{
  "trust_score": 15,
  "trust_signals": [
    "Page claims to be Nike but domain does not match official site",
    "Prices appear implausibly low for this product category (95% off)",
    "Business contact uses Gmail, indicating potential lack of legitimacy"
  ],
  "is_scam": true,
  "gaslighting_score": 95,
  "severity_label": "Fraudulent Storefront"
}
```

**Deductions:** 40 (brand) + 20 (price) + 25 (contact) = 85 → Score = 15

### Suspicious Site (Score: 80)
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "page",
    "page_url": "https://example.com/product",
    "page_title": "Amazing Discount",
    "body_text": "Special sale: 85% off all items today!",
    "price_elements": []
  }'
```

**Response:**
```json
{
  "trust_score": 80,
  "trust_signals": [
    "Prices appear implausibly low for this product category (85% off)"
  ],
  "is_scam": false,
  "gaslighting_score": 0
}
```

**Deductions:** 20 (price) → Score = 80

### Clean Site (Score: 100)
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "page",
    "page_url": "https://nike.com/shoes/air-max",
    "page_title": "Nike Air Max - Official Nike Store",
    "body_text": "Premium running shoes at $120. Contact: support@nike.com",
    "price_elements": []
  }'
```

**Response:**
```json
{
  "trust_score": 100,
  "trust_signals": ["No trust issues detected"],
  "is_scam": false,
  "gaslighting_score": 0
}
```

## Integration

The trust checking is integrated into the LangGraph pipeline:

1. **trust_node** (nodes.py:50) calls `check_trust()` service
2. **trust_gate** (nodes.py:80) evaluates trust_score
3. If trust_score < 30: routes to **output_node** (skips analysis)
4. If trust_score >= 30: routes to **analyze_node** (continues)

## Configuration

### Optional: WHOIS API
To enable domain age checking, set environment variable:
```bash
WHOIS_API_KEY=your_key_here
```

Without this key, domain age check is skipped (no crash, logged warning).

### Brand Detection
Major brands detected (can be extended in `MAJOR_BRANDS` dict):
- Nike, Adidas, Amazon, Walmart, Target, eBay
- Apple, Samsung, Microsoft, Sony
- Best Buy, Macy's, Nordstrom, Wayfair, Home Depot, Lowe's

## Technical Notes

- Uses `nest_asyncio` to allow async calls within sync LangGraph nodes
- Async WHOIS API calls with 10s timeout
- Regex patterns for price and contact detection
- Returns structured dict: `{trust_score: int, trust_signals: list[str]}`

## Testing

Run unit tests:
```bash
cd backend
python test_trust.py
```

Expected output:
- Test 1: Brand mismatch → 60
- Test 2: 90% off → 80
- Test 3: Was/now price → 80
- Test 4: Gmail contact → 75
- Test 5: Multiple signals → 15
- Test 6: Clean site → 100
