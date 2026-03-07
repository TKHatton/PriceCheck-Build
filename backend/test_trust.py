"""
Test script for trust checking functionality
"""

import asyncio
from app.services.trust import check_trust


async def test_brand_mismatch():
    """Test brand mismatch detection"""
    print("=== Test 1: Brand Mismatch ===")
    result = await check_trust(
        url="https://nike-outlet-clearance.shop",
        page_title="Nike Official Store - 90% Off All Shoes",
        body_text="Buy authentic Nike shoes at discount prices"
    )
    print(f"Trust score: {result['trust_score']}")
    print(f"Signals: {result['trust_signals']}")
    print()


async def test_price_implausibility():
    """Test price implausibility detection"""
    print("=== Test 2: Price Implausibility (percentage) ===")
    result = await check_trust(
        url="https://example.com",
        page_title="Great Deals",
        body_text="Everything 90% OFF today only! Limited time offer!"
    )
    print(f"Trust score: {result['trust_score']}")
    print(f"Signals: {result['trust_signals']}")
    print()

    print("=== Test 3: Price Implausibility (was/now) ===")
    result = await check_trust(
        url="https://example.com",
        page_title="Amazing Deals",
        body_text="Was $299 Now $49! Save big on electronics!"
    )
    print(f"Trust score: {result['trust_score']}")
    print(f"Signals: {result['trust_signals']}")
    print()


async def test_contact_legitimacy():
    """Test contact email detection"""
    print("=== Test 4: Contact Legitimacy ===")
    result = await check_trust(
        url="https://example.com",
        page_title="Contact Us",
        body_text="For support, email us at: support@gmail.com or call 555-1234"
    )
    print(f"Trust score: {result['trust_score']}")
    print(f"Signals: {result['trust_signals']}")
    print()


async def test_multiple_signals():
    """Test multiple signals triggering"""
    print("=== Test 5: Multiple Signals ===")
    result = await check_trust(
        url="https://nike-super-deals.shop",
        page_title="Nike Official - 95% Off Everything",
        body_text="Contact: sales@gmail.com. All Nike shoes 95% OFF! Was $299 now $15!"
    )
    print(f"Trust score: {result['trust_score']}")
    print(f"Signals: {result['trust_signals']}")
    expected_deductions = 40 + 20 + 25  # brand + price + contact = 85
    expected_score = 100 - expected_deductions  # = 15
    print(f"Expected score: ~{expected_score} (actual deductions may vary)")
    print()


async def test_clean_site():
    """Test legitimate site with no signals"""
    print("=== Test 6: Clean Site ===")
    result = await check_trust(
        url="https://nike.com/products/shoe",
        page_title="Nike Air Max - Official Nike Store",
        body_text="Premium running shoes at regular retail price $120. Contact: support@nike.com"
    )
    print(f"Trust score: {result['trust_score']}")
    print(f"Signals: {result['trust_signals']}")
    print()


async def main():
    print("Testing Trust Checking Service")
    print("=" * 50)
    print()

    await test_brand_mismatch()
    await test_price_implausibility()
    await test_contact_legitimacy()
    await test_multiple_signals()
    await test_clean_site()

    print("=" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
