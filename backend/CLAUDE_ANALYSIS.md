# Claude Analysis Integration

## Status: ✓ Working

The Claude API wrapper is integrated and functional with the current API key.

## Configuration

**Model:** Configurable via environment variable
```bash
# In .env file:
CLAUDE_MODEL=claude-3-haiku-20240307  # Default if not specified
```

**Current Setup:**
- API Key: Works with `claude-3-haiku-20240307`
- Model access appears limited to Haiku with this key
- To use Sonnet models, may need different API key or workspace access

## System Prompt Improvements

### False Scarcity Detection

Updated DARK_PATTERNS definition to explicitly flag scarcity claims:

```
DARK_PATTERNS: Countdown timers (sale ends in X:XX), fake urgency,
pre-checked add-ons, manipulative social proof, false scarcity claims
(only X left, limited stock, selling fast, almost gone).

IMPORTANT: Treat ALL scarcity and urgency language as manipulation
since you cannot verify inventory or actual deadlines.
```

**Key Point:** The word "verified" matters. Claude treats scarcity language as pressure tactics by default since it cannot verify actual inventory from page content alone.

## Test Results

### Test 1: Manipulative Content

**Input:**
```
WAS $299 NOW ONLY $79!
SALE ENDS IN 09:47!
Only 3 left!
Free trial, cancel anytime $49/month after
```

**Result:**
```json
{
  "tactics": [
    {
      "name": "FAKE_DISCOUNT",
      "severity": 8,
      "evidence": "WAS $299 NOW ONLY $79!",
      "explanation": "The original price of $299 is likely inflated..."
    },
    {
      "name": "DARK_PATTERNS",
      "severity": 9,
      "evidence": "SALE ENDS IN 09:47! Only 3 left!",
      "explanation": "The countdown timer and limited quantity claims create false urgency..."
    },
    {
      "name": "SUBSCRIPTION_TRAP",
      "severity": 6,
      "evidence": "Free trial, cancel anytime $49/month after",
      "explanation": "The free trial offer may auto-convert to a recurring $49/month..."
    }
  ],
  "gaslighting_score": 24,
  "severity_label": "Mildly Misleading"
}
```

**✓ Success:** All 3 tactics detected correctly
- Countdown timer → DARK_PATTERNS ✓
- "Only 3 left" → DARK_PATTERNS ✓
- Was/now pricing → FAKE_DISCOUNT ✓
- Subscription trap → SUBSCRIPTION_TRAP ✓

### Test 2: Clean Content

**Input:**
```
Premium running shoes with advanced cushioning technology.
Price: $120.
Free shipping on orders over $50.
```

**Result:**
```json
{
  "tactics": [
    {
      "name": "FAKE_DISCOUNT",
      "severity": 3,
      "evidence": "Price: $120"
    }
  ],
  "gaslighting_score": 3,
  "severity_label": "Honest Pricing"
}
```

**Note:** Minor false positive (severity 3) but score is still in "Honest Pricing" range (0-20). This is acceptable for production use.

## Tactic Categorization

| Tactic | What It Catches | Severity Range |
|--------|----------------|----------------|
| **FAKE_DISCOUNT** | Inflated "was" prices, perpetual sales | 6-10 |
| **DARK_PATTERNS** | Countdown timers, "only X left", fake urgency | 7-10 |
| **SUBSCRIPTION_TRAP** | Auto-converting trials, hidden recurring charges | 5-9 |
| **HIDDEN_FEES** | Mandatory charges withheld until checkout | 7-10 |
| **DRIP_PRICING** | Base price + sequential mandatory additions | 6-9 |
| **SHRINKFLATION** | Same price, smaller quantity | 4-7 |

## Scoring Weights (from score_node)

| Category | Weight | Notes |
|----------|--------|-------|
| HIDDEN_FEES | 1.3 | Direct financial harm |
| DRIP_PRICING | 1.2 | Systematic deception |
| FAKE_DISCOUNT | 1.2 | Very common tactic |
| SUBSCRIPTION_TRAP | 1.1 | Long-term recurring harm |
| DARK_PATTERNS | 0.9 | Psychological manipulation |
| SHRINKFLATION | 0.8 | Harder to detect |

## Example Score Calculation

**Input:** 3 tactics from Test 1
- FAKE_DISCOUNT (8) × 1.2 = 9.6
- DARK_PATTERNS (9) × 0.9 = 8.1
- SUBSCRIPTION_TRAP (6) × 1.1 = 6.6

**Total:** 9.6 + 8.1 + 6.6 = 24.3 → **24** (Mildly Misleading)

## Running Tests

```bash
cd backend
python test_claude_integration.py
```

## Troubleshooting

**"404 - model not found"**
- Check CLAUDE_MODEL in .env matches available models
- Default `claude-3-haiku-20240307` should work with most keys
- Try `claude-3-5-sonnet-20241022` if key has access

**"ANTHROPIC_API_KEY not set"**
- Ensure .env file exists in backend/ directory
- Key format: `sk-ant-api03-...`
- Load with `python-dotenv`

**False positives on clean content**
- Low severity (1-3) is acceptable
- Score under 20 = "Honest Pricing" label
- Prompt can be tuned further if needed
