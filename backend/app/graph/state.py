from typing import TypedDict, Optional


class PriceCheckState(TypedDict):
    """
    Shared state object for LangGraph pipeline
    All nodes read from and write to this state
    """
    # Input -- from content script via popup
    input_type: str           # 'page' | 'image' | 'manual'
    page_url: str             # current tab URL
    page_title: str           # document.title
    body_text: str            # document.body.innerText (truncated 15k chars)
    price_elements: list      # targeted price DOM extracts
    raw_image: Optional[bytes]   # if screenshot path used
    manual_text: Optional[str]   # if manual entry path used

    # After trust check
    trust_score: int          # 0 to 100
    trust_signals: list[str]  # human-readable flag descriptions
    trust_gate_pass: bool     # whether trust check passed threshold

    # After Claude analysis
    tactics: list[dict]       # {name, severity, evidence, explanation}
    marketed_price: Optional[float]
    real_price: Optional[float]
    price_delta: Optional[float]
    real_cost_note: Optional[str]

    # After scoring
    gaslighting_score: int    # 0 to 100
    severity_label: str       # Honest Pricing | Mildly Misleading | Actively Deceptive | Full Gaslighting

    # Flags
    is_scam: bool             # True if trust_score < 30
    error: Optional[str]      # Error message if analysis fails
