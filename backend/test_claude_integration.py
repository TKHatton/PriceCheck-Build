"""
Test script for Claude API integration
Demonstrates expected behavior with valid API key
"""

from dotenv import load_dotenv
load_dotenv()

from app.graph.graph import compiled_graph
import json


def test_manipulative_content():
    """Test 1: Content with obvious manipulation tactics"""
    print("=" * 70)
    print("TEST 1: Manipulative Content")
    print("=" * 70)
    print()

    test_state = {
        'input_type': 'page',
        'page_url': 'https://example.com/product',
        'page_title': 'Amazing Deal - Limited Time Only!',
        'body_text': 'WAS $299 NOW ONLY $79! SALE ENDS IN 09:47! Only 3 left! Free trial, cancel anytime $49/month after',
        'price_elements': [
            {'text': 'WAS $299'},
            {'text': 'NOW $79'},
            {'text': '$49/month'}
        ],
        'raw_image': None,
        'manual_text': None,
        'trust_score': 100,
        'trust_signals': [],
        'trust_gate_pass': True,
        'tactics': [],
        'marketed_price': None,
        'real_price': None,
        'price_delta': None,
        'real_cost_note': None,
        'gaslighting_score': 0,
        'severity_label': 'Honest Pricing',
        'is_scam': False,
        'error': None,
    }

    print("Input:")
    print(f"  body_text: {test_state['body_text']}")
    print()

    result = compiled_graph.invoke(test_state)

    print()
    print("Result:")
    print(f"  Tactics found: {len(result.get('tactics', []))}")

    if result.get('tactics'):
        print()
        for i, tactic in enumerate(result.get('tactics', []), 1):
            print(f"  {i}. {tactic.get('name')} (severity: {tactic.get('severity')})")
            print(f"     Evidence: \"{tactic.get('evidence', '')}\"")
            print(f"     Explanation: {tactic.get('explanation', '')}")
            print()

    print(f"  Marketed price: ${result.get('marketed_price')}")
    print(f"  Real price: ${result.get('real_price')}")
    print(f"  Price delta: ${result.get('price_delta')}")
    print(f"  Gaslighting score: {result.get('gaslighting_score')}")
    print(f"  Severity label: {result.get('severity_label')}")

    if result.get('error'):
        print(f"  Error: {result.get('error')}")

    print()
    print("Expected with valid API key:")
    print("  - 3+ tactics (FAKE_DISCOUNT, DARK_PATTERNS, SUBSCRIPTION_TRAP)")
    print("  - Marketed price: $79")
    print("  - Real price: ~$49-79 (depends on analysis)")
    print("  - Gaslighting score: 40-70 (Mildly Misleading to Actively Deceptive)")
    print()


def test_clean_content():
    """Test 2: Clean content with no manipulation"""
    print("=" * 70)
    print("TEST 2: Clean Content (No Manipulation)")
    print("=" * 70)
    print()

    test_state = {
        'input_type': 'page',
        'page_url': 'https://example.com/product',
        'page_title': 'Quality Product',
        'body_text': 'Premium quality item for $120. Fast shipping available. Contact our support team if you have questions.',
        'price_elements': [
            {'text': '$120'}
        ],
        'raw_image': None,
        'manual_text': None,
        'trust_score': 100,
        'trust_signals': [],
        'trust_gate_pass': True,
        'tactics': [],
        'marketed_price': None,
        'real_price': None,
        'price_delta': None,
        'real_cost_note': None,
        'gaslighting_score': 0,
        'severity_label': 'Honest Pricing',
        'is_scam': False,
        'error': None,
    }

    print("Input:")
    print(f"  body_text: {test_state['body_text']}")
    print()

    result = compiled_graph.invoke(test_state)

    print()
    print("Result:")
    print(f"  Tactics found: {len(result.get('tactics', []))}")

    if result.get('tactics'):
        print()
        for i, tactic in enumerate(result.get('tactics', []), 1):
            print(f"  {i}. {tactic.get('name')} (severity: {tactic.get('severity')})")

    print(f"  Gaslighting score: {result.get('gaslighting_score')}")
    print(f"  Severity label: {result.get('severity_label')}")

    if result.get('error'):
        print(f"  Error: {result.get('error')}")

    print()
    print("Expected with valid API key:")
    print("  - 0 tactics or 1 low-severity item")
    print("  - Gaslighting score: 0-20 (Honest Pricing)")
    print()


if __name__ == "__main__":
    test_manipulative_content()
    test_clean_content()

    print("=" * 70)
    print("TROUBLESHOOTING")
    print("=" * 70)
    print()
    print("If you see '404 - not_found_error' for models:")
    print("  1. Check ANTHROPIC_API_KEY is valid and not expired")
    print("  2. Verify key has access to Claude models")
    print("  3. Try generating a new API key at console.anthropic.com")
    print()
    print("If you see 'ANTHROPIC_API_KEY not set':")
    print("  1. Ensure .env file exists in backend/ directory")
    print("  2. Check .env has: ANTHROPIC_API_KEY=sk-ant-...")
    print("  3. python-dotenv should be installed")
    print()
