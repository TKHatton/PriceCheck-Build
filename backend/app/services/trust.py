"""
Trust checking service for PriceCheck.
Evaluates domain legitimacy using multiple signals.
"""

import os
import re
import httpx
from datetime import datetime, timezone
from urllib.parse import urlparse
from typing import Optional


# Major brand domains for mismatch detection
MAJOR_BRANDS = {
    'nike': ['nike.com'],
    'adidas': ['adidas.com'],
    'amazon': ['amazon.com', 'amazon.co.uk', 'amazon.de'],
    'walmart': ['walmart.com'],
    'target': ['target.com'],
    'ebay': ['ebay.com'],
    'apple': ['apple.com'],
    'samsung': ['samsung.com'],
    'microsoft': ['microsoft.com'],
    'sony': ['sony.com'],
    'bestbuy': ['bestbuy.com'],
    'macys': ['macys.com'],
    'nordstrom': ['nordstrom.com'],
    'wayfair': ['wayfair.com'],
    'homedepot': ['homedepot.com'],
    'lowes': ['lowes.com'],
}


async def check_trust(
    url: str,
    page_title: str = '',
    body_text: str = ''
) -> dict:
    """
    Evaluates domain trustworthiness using multiple signals.

    Args:
        url: The URL being analyzed
        page_title: Page title for brand mismatch detection
        body_text: Page content for price and contact checks

    Returns:
        {
            'trust_score': int (0-100),
            'trust_signals': list[str] (human-readable warnings)
        }
    """
    trust_score = 100
    trust_signals = []

    # Parse domain from URL
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if not domain:
            trust_signals.append('Invalid URL format')
            return {'trust_score': 0, 'trust_signals': trust_signals}
    except Exception as e:
        trust_signals.append(f'URL parsing error: {e}')
        return {'trust_score': 0, 'trust_signals': trust_signals}

    # Signal 1: Domain age check (WHOIS)
    domain_age_result = await check_domain_age(domain)
    if domain_age_result:
        trust_score -= domain_age_result['deduction']
        trust_signals.extend(domain_age_result['signals'])

    # Signal 2: Brand mismatch
    brand_result = check_brand_mismatch(domain, page_title)
    if brand_result:
        trust_score -= brand_result['deduction']
        trust_signals.extend(brand_result['signals'])

    # Signal 3: Price implausibility
    price_result = check_price_implausibility(body_text)
    if price_result:
        trust_score -= price_result['deduction']
        trust_signals.extend(price_result['signals'])

    # Signal 4: Contact legitimacy
    contact_result = check_contact_legitimacy(body_text)
    if contact_result:
        trust_score -= contact_result['deduction']
        trust_signals.extend(contact_result['signals'])

    # Ensure score stays within bounds
    trust_score = max(0, min(100, trust_score))

    return {
        'trust_score': trust_score,
        'trust_signals': trust_signals if trust_signals else ['No trust issues detected']
    }


async def check_domain_age(domain: str) -> Optional[dict]:
    """
    Check domain registration age via WHOIS API.
    Deducts 35 points if domain is less than 90 days old.
    """
    whois_api_key = os.getenv('WHOIS_API_KEY')

    if not whois_api_key:
        print('[trust] WHOIS_API_KEY not set, skipping domain age check')
        return None

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Using WHOIS API (whoisxmlapi.com format)
            response = await client.get(
                f'https://www.whoisxmlapi.com/whoisserver/WhoisService',
                params={
                    'apiKey': whois_api_key,
                    'domainName': domain,
                    'outputFormat': 'JSON'
                }
            )

            if response.status_code != 200:
                print(f'[trust] WHOIS API error: {response.status_code}')
                return None

            data = response.json()
            whois_record = data.get('WhoisRecord', {})
            created_date_str = whois_record.get('createdDate')

            if not created_date_str:
                print('[trust] WHOIS API returned no creation date')
                return None

            # Parse creation date
            created_date = datetime.fromisoformat(created_date_str.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            age_days = (now - created_date).days

            if age_days < 90:
                return {
                    'deduction': 35,
                    'signals': [f'Domain registered less than 90 days ago ({age_days} days)']
                }

    except Exception as e:
        print(f'[trust] WHOIS check failed: {e}')
        return None

    return None


def check_brand_mismatch(domain: str, page_title: str) -> Optional[dict]:
    """
    Detects if page claims to be a major brand but domain doesn't match.
    Deducts 40 points for mismatch.
    """
    if not page_title:
        return None

    page_title_lower = page_title.lower()

    # Check if page title mentions a major brand
    for brand, official_domains in MAJOR_BRANDS.items():
        if brand in page_title_lower:
            # Check if domain matches any official domain
            domain_matches = any(official in domain for official in official_domains)

            if not domain_matches:
                # Domain claims to be a brand but doesn't match official domain
                # This is suspicious even if brand name appears in domain (e.g., nike-outlet-sale.shop)
                return {
                    'deduction': 40,
                    'signals': [
                        f'Page claims to be {brand.title()} but domain does not match official site'
                    ]
                }

    return None


def check_price_implausibility(body_text: str) -> Optional[dict]:
    """
    Detects implausibly low prices (>70% discount).
    Deducts 20 points if found.
    """
    if not body_text:
        return None

    body_lower = body_text.lower()

    # Look for discount patterns: "70% off", "80% off", "90% off"
    discount_pattern = r'(\d+)\s*%\s*off'
    matches = re.findall(discount_pattern, body_lower)

    for match in matches:
        discount_percent = int(match)
        if discount_percent >= 70:
            return {
                'deduction': 20,
                'signals': [
                    f'Prices appear implausibly low for this product category ({discount_percent}% off)'
                ]
            }

    # Also check for "was/now" patterns with >70% reduction
    was_now_pattern = r'was\s*\$?\s*([\d,]+(?:\.\d{2})?)\s*.*?now\s*\$?\s*([\d,]+(?:\.\d{2})?)'
    was_now_matches = re.findall(was_now_pattern, body_lower, re.IGNORECASE)

    for was_price_str, now_price_str in was_now_matches:
        try:
            was_price = float(was_price_str.replace(',', ''))
            now_price = float(now_price_str.replace(',', ''))

            if was_price > 0:
                discount_percent = ((was_price - now_price) / was_price) * 100

                if discount_percent >= 70:
                    return {
                        'deduction': 20,
                        'signals': [
                            f'Prices appear implausibly low (${now_price:.2f} from ${was_price:.2f}, {discount_percent:.0f}% off)'
                        ]
                    }
        except (ValueError, ZeroDivisionError):
            continue

    return None


def check_contact_legitimacy(body_text: str) -> Optional[dict]:
    """
    Detects free email services used for business contact.
    Deducts 25 points if found.
    """
    if not body_text:
        return None

    body_lower = body_text.lower()

    # Free email providers that businesses shouldn't use
    free_email_patterns = [
        r'contact[:\s]+[^\s]*@gmail\.com',
        r'contact[:\s]+[^\s]*@yahoo\.com',
        r'contact[:\s]+[^\s]*@hotmail\.com',
        r'contact[:\s]+[^\s]*@outlook\.com',
        r'support[:\s]+[^\s]*@gmail\.com',
        r'support[:\s]+[^\s]*@yahoo\.com',
        r'email[:\s]+[^\s]*@gmail\.com',
        r'email[:\s]+[^\s]*@yahoo\.com',
        # Also catch standalone emails in contact sections
        r'@gmail\.com',
        r'@yahoo\.com',
    ]

    for pattern in free_email_patterns:
        if re.search(pattern, body_lower):
            # Extract which service was found
            if '@gmail.com' in body_lower:
                service = 'Gmail'
            elif '@yahoo.com' in body_lower:
                service = 'Yahoo'
            elif '@hotmail.com' in body_lower:
                service = 'Hotmail'
            elif '@outlook.com' in body_lower:
                service = 'Outlook'
            else:
                service = 'free email service'

            return {
                'deduction': 25,
                'signals': [
                    f'Business contact uses {service}, indicating potential lack of legitimacy'
                ]
            }

    return None
