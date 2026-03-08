"""
Claude API wrapper for PriceCheck content analysis.
Uses Anthropic SDK to analyze page content for pricing manipulation tactics.
"""

import os
import json
from typing import Optional
from anthropic import Anthropic


# System prompt for pricing analysis
SYSTEM_PROMPT = """You are a consumer protection analyst specializing in pricing psychology and retail dark patterns.

Task: Analyze the provided page content and identify every pricing manipulation tactic present. Be thorough and aggressive in detection, especially for common tactics that retailers use on consumers.

Output: Return ONLY valid JSON. No preamble. No explanation. No markdown fences. Raw JSON only.

Evidence requirement: Flag any tactic where reasonable evidence exists in the page content. For every tactic flagged, cite the specific text from the page that supports it.

Tone of explanations: One plain-English sentence per tactic. Written for a non-expert audience.

Detection guidelines:
- Flag ALL instances of urgency and scarcity language as DARK_PATTERNS, even on legitimate sites. Retailers cannot verify real-time inventory or deadlines, so all such claims are inherently manipulative.
- A crossed-out price next to a lower current price is FAKE_DISCOUNT unless there is clear evidence the original price was regularly charged. The mere presence of a strikethrough price is sufficient evidence to flag this.
- If the page shows a percentage discount (e.g. 41% OFF), flag it as FAKE_DISCOUNT with severity 6 minimum unless the discount is verifiably tied to documented price history.
- Installment payment options (Afterpay, Klarna, Pay in 4, Buy Now Pay Later) displayed at point of purchase are a form of DRIP_PRICING that obscures the true total cost. Always flag these with severity 5 minimum.
- Look carefully for subscription language, auto-renewal warnings, and trial period disclosures.
- Check for fees mentioned separately from the main price (shipping, handling, service fees, resort fees, convenience charges).
- Compare package sizes and per-unit pricing when multiple options are shown.

Valid tactic names (use exactly these):
- FAKE_DISCOUNT: Inflated original prices, was/now manipulation, perpetual sales that never end, "MSRP vs our price" claims, crossed-out prices shown next to sale prices, percentage discount badges (e.g. "41% OFF"). **CRITICAL: If you see a strikethrough/crossed-out price or a percentage discount badge, flag this immediately.** Do NOT use this category for countdown timers or scarcity claims.
- HIDDEN_FEES: Mandatory charges withheld until checkout, or fees mentioned far from the advertised price (shipping, service fees, resort fees, convenience charges, mandatory gratuity, processing fees).
- DRIP_PRICING: Base price shown upfront, mandatory extras revealed progressively through purchase flow (insurance, protection plans, premium options presented as required). **CRITICAL: Installment payment options like Afterpay, Klarna, "Pay in 4", or "Buy Now Pay Later" are ALWAYS this category with minimum severity 5.**
- DARK_PATTERNS: **FLAG THIS AGGRESSIVELY.** This includes ALL of the following regardless of site legitimacy:
  • Crossed-out original prices shown next to a sale price (visual manipulation)
  • Any "X% OFF" badge or label
  • Social proof claims ("31K+ sold", "X people viewing this", "Trending", "Popular")
  • Installment payment options displayed at point of purchase ("Pay $4 today with Afterpay/Klarna")
  • Popup overlays offering coupons, bonuses, or time-limited deals
  • Countdown timers ("Sale ends in X:XX")
  • Urgency language ("Hurry", "Limited time", "Ends soon", "Today only")
  • Scarcity claims ("Only X left", "Low stock", "Limited availability", "Selling fast", "Almost gone")
  • Pre-checked add-ons or default selections
  • Manipulative social proof ("X bought in last 24 hours")
  **CRITICAL: Flag ALL of these tactics even on major legitimate retailer sites. They are manipulation regardless of site reputation.**
- SUBSCRIPTION_TRAP: Free trials with auto-conversion to paid, recurring charges, hard-to-find cancellation, subscription default selections, trial period buried in fine print.
- SHRINKFLATION: Same or similar price for reduced quantity, deceptive package sizing, unfavorable per-unit pricing compared to similar products.

DETECTION RULES - Apply these aggressively:

• Any crossed-out or strikethrough price next to a lower price = FAKE_DISCOUNT (severity 7+)
• Any "X% OFF" badge or label = FAKE_DISCOUNT (severity 6+)
• Any "Only X left", "Almost sold out", "Selling fast", "X sold", "Limited stock" = DARK_PATTERNS (severity 7+)
• Any countdown timer or "Sale ends in" = DARK_PATTERNS (severity 8+)
• Any "Buy now pay later", Afterpay, Klarna installment breakdown = DARK_PATTERNS (severity 5+)
• Any "Free trial" that converts to paid subscription = SUBSCRIPTION_TRAP (severity 7+)
• Any coupon popups, bonus offers, or "extra discount" overlays = DARK_PATTERNS (severity 5+)
• Any pre-checked add-ons or insurance options = DARK_PATTERNS (severity 6+)

IMPORTANT: You are analyzing a REAL retail page. The text will contain navigation, product descriptions, and other noise mixed in with pricing tactics. Search through ALL the provided text carefully. Do not dismiss tactics just because they appear alongside legitimate content. If you see pricing manipulation patterns ANYWHERE in the text, flag them.
If the page contains multiple products (like a category page), analyze the pricing patterns visible across all products.

Response JSON schema:
{
  "tactics": [
    {
      "name": "TACTIC_NAME",
      "severity": 1-10,
      "evidence": "exact text from page",
      "explanation": "one sentence explanation"
    }
  ],
  "marketed_price": number or null,
  "real_price": number or null,
  "price_delta": number or null,
  "real_cost_note": "string explaining true cost" or null
}

Severity scoring guide:
- 1-3: Mild (subtle language, easy to miss)
- 4-6: Moderate (prominent placement, clear manipulation)
- 7-9: Severe (aggressive tactics, multiple instances, hard to ignore)
- 10: Extreme (deceptive, predatory, likely to cause financial harm)

If no tactics are found, return: {"tactics": [], "marketed_price": null, "real_price": null, "price_delta": null, "real_cost_note": null}"""


def analyze_content(
    body_text: str,
    price_elements: list,
    page_title: str
) -> dict:
    """
    Analyzes page content for pricing manipulation tactics using Claude.

    Args:
        body_text: Main text content from the page (up to 15k chars)
        price_elements: List of extracted price elements from DOM
        page_title: The page title

    Returns:
        dict with keys: tactics, marketed_price, real_price, price_delta, real_cost_note
    """
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        print('[claude] ANTHROPIC_API_KEY not set, returning empty analysis')
        return {
            'tactics': [],
            'marketed_price': None,
            'real_price': None,
            'price_delta': None,
            'real_cost_note': 'Analysis unavailable: API key not configured'
        }

    # Build the user message with page content
    price_elements_text = '\n'.join([
        f"- {elem.get('text', str(elem))}"
        for elem in price_elements[:20]  # Limit to first 20 elements
    ]) if price_elements else 'No specific price elements extracted'

    user_message = f"""Analyze this product page for pricing manipulation tactics:

PAGE TITLE: {page_title}

EXTRACTED PRICE ELEMENTS:
{price_elements_text}

PAGE CONTENT:
{body_text[:12000]}"""  # Truncate to avoid token limits

    try:
        client = Anthropic(api_key=api_key)

        # Use model from environment or fall back to Haiku
        model = os.getenv('CLAUDE_MODEL', 'claude-3-haiku-20240307')

        response = client.messages.create(
            model=model,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the text response
        response_text = response.content[0].text.strip()

        # Parse JSON response
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f'[claude] Failed to parse JSON response: {e}')
            print(f'[claude] Raw response: {response_text[:500]}')
            # Try to extract JSON from response if it has markdown fences
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                if json_end > json_start:
                    result = json.loads(response_text[json_start:json_end].strip())
            elif '```' in response_text:
                json_start = response_text.find('```') + 3
                json_end = response_text.find('```', json_start)
                if json_end > json_start:
                    result = json.loads(response_text[json_start:json_end].strip())
            else:
                # Return empty result if parsing fails
                return {
                    'tactics': [],
                    'marketed_price': None,
                    'real_price': None,
                    'price_delta': None,
                    'real_cost_note': f'Analysis parsing error: {str(e)}'
                }

        # Validate and normalize the response structure
        normalized = {
            'tactics': result.get('tactics', []),
            'marketed_price': result.get('marketed_price'),
            'real_price': result.get('real_price'),
            'price_delta': result.get('price_delta'),
            'real_cost_note': result.get('real_cost_note')
        }

        # Validate tactics structure
        valid_tactics = []
        valid_tactic_names = {
            'FAKE_DISCOUNT', 'HIDDEN_FEES', 'DRIP_PRICING',
            'DARK_PATTERNS', 'SUBSCRIPTION_TRAP', 'SHRINKFLATION',
            'FRAUDULENT_STOREFRONT'  # Added by trust layer
        }

        for tactic in normalized['tactics']:
            if isinstance(tactic, dict):
                name = tactic.get('name', '').upper()
                if name in valid_tactic_names:
                    valid_tactics.append({
                        'name': name,
                        'severity': min(10, max(1, int(tactic.get('severity', 5)))),
                        'evidence': str(tactic.get('evidence', '')),
                        'explanation': str(tactic.get('explanation', ''))
                    })

        normalized['tactics'] = valid_tactics

        print(f'[claude] Analysis complete: {len(valid_tactics)} tactics found')
        return normalized

    except Exception as e:
        print(f'[claude] API error: {e}')
        return {
            'tactics': [],
            'marketed_price': None,
            'real_price': None,
            'price_delta': None,
            'real_cost_note': f'Analysis error: {str(e)}'
        }
