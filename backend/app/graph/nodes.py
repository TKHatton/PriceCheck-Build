"""
LangGraph node functions for PriceCheck analysis pipeline.
Each node reads from and writes to the shared PriceCheckState.
"""

import asyncio
from app.graph.state import PriceCheckState
from app.services.trust import check_trust
from app.services.claude import analyze_content

# Allow nested event loops


def input_router(state: PriceCheckState) -> PriceCheckState:
    """
    Entry node that routes based on input_type.
    This is a pass-through node; routing logic is in edges.py.
    """
    print(f"[input_router] Processing input_type: {state.get('input_type', 'unknown')}")
    return state


def content_node(state: PriceCheckState) -> PriceCheckState:
    """
    Processes pre-extracted page data from content script.
    Formats body_text and price_elements for analysis.
    """
    print(f"[content_node] Processing page: {state.get('page_url', 'unknown')}")
    # TODO: Format and prepare content for Claude analysis
    return state


def ocr_node(state: PriceCheckState) -> PriceCheckState:
    """
    Processes raw_image bytes using Claude Vision.
    Extracts pricing text from screenshots.
    """
    print("[ocr_node] Processing image with Claude Vision")
    # TODO: Send raw_image to Claude Vision API for OCR
    return state


def manual_node(state: PriceCheckState) -> PriceCheckState:
    """
    Processes manually entered text.
    Copies manual_text into content fields.
    """
    print("[manual_node] Processing manual text input")
    # TODO: Copy manual_text to appropriate content fields
    return state


def trust_node(state: PriceCheckState) -> PriceCheckState:
    """
    Performs domain trust checks using URLScan + WHOIS APIs.
    Evaluates: domain age, brand vs URL mismatch, price plausibility,
    contact legitimacy, legal copy quality.
    """
    print(f"[trust_node] Checking trust for: {state.get('page_url', 'unknown')}")

    # Call async trust check service
    page_url = state.get('page_url', '')
    page_title = state.get('page_title', '')
    body_text = state.get('body_text', '')

    # Run async function in sync context
    trust_result = asyncio.run(check_trust(
        url=page_url,
        page_title=page_title,
        body_text=body_text
    ))

    updated_state = dict(state)
    updated_state['trust_score'] = trust_result['trust_score']
    updated_state['trust_signals'] = trust_result['trust_signals']
    updated_state['trust_gate_pass'] = trust_result['trust_score'] >= 30

    print(f"[trust_node] Trust score: {trust_result['trust_score']}, Signals: {len(trust_result['trust_signals'])}")

    return updated_state


def trust_gate(state: PriceCheckState) -> PriceCheckState:
    """
    Evaluates trust_score and sets is_scam flag.
    Routing to output_node or analyze_node is handled by edges.py.
    """
    trust_score = state.get('trust_score', 100)
    print(f"[trust_gate] Trust score: {trust_score}")

    updated_state = dict(state)

    if trust_score < 30:
        updated_state['is_scam'] = True
        updated_state['trust_gate_pass'] = False
        updated_state['gaslighting_score'] = 95  # Minimum score for scam sites
        updated_state['severity_label'] = 'Fraudulent Storefront'
        print("[trust_gate] SCAM DETECTED - routing to output")
    else:
        updated_state['is_scam'] = False
        updated_state['trust_gate_pass'] = True
        print("[trust_gate] Trust passed - routing to analyze")

    return updated_state


def analyze_node(state: PriceCheckState) -> PriceCheckState:
    """
    Core analysis node using Claude API.
    Sends formatted page content to Claude and receives structured JSON
    with tactics array, marketed_price, real_price, price_delta.
    """
    print("[analyze_node] Analyzing with Claude API")

    # Extract content from state
    body_text = state.get('body_text', '')
    price_elements = state.get('price_elements', [])
    page_title = state.get('page_title', '')

    # Call Claude API for analysis
    analysis_result = asyncio.run(analyze_content(
        body_text=body_text,
        price_elements=price_elements,
        page_title=page_title
    ))

    updated_state = dict(state)
    updated_state['tactics'] = analysis_result.get('tactics', [])
    updated_state['marketed_price'] = analysis_result.get('marketed_price')
    updated_state['real_price'] = analysis_result.get('real_price')
    updated_state['price_delta'] = analysis_result.get('price_delta')
    updated_state['real_cost_note'] = analysis_result.get('real_cost_note')

    print(f"[analyze_node] Found {len(updated_state['tactics'])} tactics")

    return updated_state


def score_node(state: PriceCheckState) -> PriceCheckState:
    """
    Calculates gaslighting_score from detected tactics.
    Applies category weights and normalizes to 0-100.
    Pure Python logic, no API calls.

    Category weights from PRD:
    - HIDDEN_FEES: 1.3
    - DRIP_PRICING: 1.2
    - FAKE_DISCOUNT: 1.2
    - SUBSCRIPTION_TRAP: 1.1
    - DARK_PATTERNS: 0.9
    - SHRINKFLATION: 0.8
    - FRAUDULENT_STOREFRONT: Override to minimum 95
    """
    print("[score_node] Calculating gaslighting score")

    # Category weights
    WEIGHTS = {
        'HIDDEN_FEES': 1.3,
        'DRIP_PRICING': 1.2,
        'FAKE_DISCOUNT': 1.2,
        'SUBSCRIPTION_TRAP': 1.1,
        'DARK_PATTERNS': 0.9,
        'SHRINKFLATION': 0.8,
        'FRAUDULENT_STOREFRONT': 1.0,  # Override handled separately
    }

    tactics = state.get('tactics', [])
    is_scam = state.get('is_scam', False)
    updated_state = dict(state)

    # Calculate weighted score
    if not tactics:
        updated_state['gaslighting_score'] = 0
        updated_state['severity_label'] = 'Honest Pricing'
        return updated_state

    total_score = 0
    for tactic in tactics:
        name = tactic.get('name', '')
        severity = tactic.get('severity', 0)
        weight = WEIGHTS.get(name, 1.0)
        total_score += severity * weight

    # Normalize to 0-100 scale (max raw score ~100 with 10 tactics at severity 10)
    normalized_score = min(100, int(total_score))

    # If is_scam flag is set (fraudulent storefront), ensure minimum score of 95
    if is_scam:
        normalized_score = max(95, normalized_score)

    # Assign severity label
    if normalized_score <= 20:
        label = 'Honest Pricing'
    elif normalized_score <= 45:
        label = 'Mildly Misleading'
    elif normalized_score <= 70:
        label = 'Actively Deceptive'
    else:
        label = 'Full Gaslighting'

    updated_state['gaslighting_score'] = normalized_score
    updated_state['severity_label'] = label

    print(f"[score_node] Final score: {normalized_score} ({label})")
    return updated_state


def output_node(state: PriceCheckState) -> PriceCheckState:
    """
    Terminal node that prepares final state for API response.
    Ensures all required fields are present.
    """
    print("[output_node] Preparing final output")

    updated_state = dict(state)

    # Ensure all required fields have defaults
    updated_state.setdefault('gaslighting_score', 0)
    updated_state.setdefault('severity_label', 'Honest Pricing')
    updated_state.setdefault('tactics', [])
    updated_state.setdefault('trust_score', 100)
    updated_state.setdefault('trust_signals', [])
    updated_state.setdefault('is_scam', False)
    updated_state.setdefault('marketed_price', None)
    updated_state.setdefault('real_price', None)
    updated_state.setdefault('price_delta', None)
    updated_state.setdefault('error', None)

    return updated_state
