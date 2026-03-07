"""
Claude API wrapper for PriceCheck content analysis.
Uses Anthropic SDK to analyze page content for pricing manipulation tactics.
"""

import os
import json
from typing import Optional
from anthropic import AsyncAnthropic


# System prompt for pricing analysis
SYSTEM_PROMPT = """You are a consumer protection analyst specializing in pricing psychology and retail dark patterns.

Task: Analyze the provided page content and identify every pricing manipulation tactic present.

Output: Return ONLY valid JSON. No preamble. No explanation. No markdown fences. Raw JSON only.

Evidence requirement: For every tactic flagged, cite the specific text from the page that supports it. Do not speculate. Only flag what is present in the provided content.

Tone of explanations: One plain-English sentence per tactic. Written for a non-expert audience.

Constraint: If no manipulation is detected for a category, do not include it. Only flag what is actually present.

Valid tactic names (use exactly these):
- FAKE_DISCOUNT: Inflated original prices, was/now manipulation, perpetual sales. NOTE: Do NOT use this for countdown timers or scarcity claims.
- HIDDEN_FEES: Mandatory charges withheld until checkout
- DRIP_PRICING: Base price shown upfront, mandatory extras added through purchase flow
- DARK_PATTERNS: Countdown timers (sale ends in X:XX), fake urgency, pre-checked add-ons, manipulative social proof, false scarcity claims (only X left, limited stock, selling fast, almost gone). IMPORTANT: Treat ALL scarcity and urgency language as manipulation since you cannot verify inventory or actual deadlines. This includes countdown timers and limited quantity claims.
- SUBSCRIPTION_TRAP: Free trials that auto-convert, hard-to-cancel recurring charges
- SHRINKFLATION: Same price, smaller quantity

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

If no tactics are found, return: {"tactics": [], "marketed_price": null, "real_price": null, "price_delta": null, "real_cost_note": null}"""


async def analyze_content(
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

PRICE ELEMENTS FOUND:
{price_elements_text}

PAGE CONTENT:
{body_text[:12000]}"""  # Truncate to avoid token limits

    try:
        client = AsyncAnthropic(api_key=api_key)

        # Use model from environment or fall back to working model
        model = os.getenv('CLAUDE_MODEL', 'claude-3-haiku-20240307')

        response = await client.messages.create(
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
