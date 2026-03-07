from pydantic import BaseModel, Field
from typing import Optional


class AnalyzeRequest(BaseModel):
    """Request model for /analyze endpoint"""
    input_type: str = Field(..., description="Type of input: 'page' | 'image' | 'manual'")
    page_url: str = Field(..., description="URL of the page being analyzed")
    page_title: str = Field(..., description="Page title from document.title")
    body_text: str = Field(..., description="Visible text content from page (truncated to 15k chars)")
    price_elements: list = Field(default_factory=list, description="Extracted price elements from DOM")
    raw_image: Optional[bytes] = Field(None, description="Raw image bytes if using screenshot input")
    manual_text: Optional[str] = Field(None, description="Manual text input if user typed directly")


class TacticDetail(BaseModel):
    """Individual manipulation tactic detected"""
    name: str = Field(..., description="Tactic category name (e.g., FAKE_DISCOUNT)")
    severity: int = Field(..., description="Severity score 0-10")
    evidence: str = Field(..., description="Specific text from page supporting this finding")
    explanation: str = Field(..., description="Plain English explanation for user")


class AnalyzeResponse(BaseModel):
    """Response model for /analyze endpoint"""
    gaslighting_score: int = Field(..., description="Overall manipulation score 0-100")
    severity_label: str = Field(..., description="Text label: Honest Pricing | Mildly Misleading | Actively Deceptive | Full Gaslighting")
    tactics: list[TacticDetail] = Field(default_factory=list, description="List of detected manipulation tactics")
    trust_score: int = Field(..., description="Domain trust score 0-100")
    trust_signals: list[str] = Field(default_factory=list, description="Human-readable trust signals")
    is_scam: bool = Field(..., description="True if site is likely fraudulent")
    marketed_price: Optional[float] = Field(None, description="Price shown to user")
    real_price: Optional[float] = Field(None, description="Actual price after fees/manipulations")
    price_delta: Optional[float] = Field(None, description="Difference between marketed and real price")
    error: Optional[str] = Field(None, description="Error message if analysis failed")
