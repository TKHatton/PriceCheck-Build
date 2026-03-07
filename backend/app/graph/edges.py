"""
LangGraph edge router functions for PriceCheck analysis pipeline.
These functions determine conditional routing between nodes.
"""

from typing import Literal
from app.graph.state import PriceCheckState


def route_by_input_type(state: PriceCheckState) -> Literal['content_node', 'ocr_node', 'manual_node']:
    """
    Routes from input_router based on input_type field.

    Returns:
        'content_node' if input_type == 'page'
        'ocr_node' if input_type == 'image'
        'manual_node' if input_type == 'manual'
    """
    input_type = state.get('input_type', 'page')

    if input_type == 'image':
        return 'ocr_node'
    elif input_type == 'manual':
        return 'manual_node'
    else:
        # Default to page/content processing
        return 'content_node'


def route_by_trust(state: PriceCheckState) -> Literal['output_node', 'analyze_node']:
    """
    Routes from trust_gate based on trust_score.

    If trust_score < 30: routes to output_node (scam exit, skip analysis)
    If trust_score >= 30: routes to analyze_node (continue analysis)

    Returns:
        'output_node' if trust_score < 30 (scam detected)
        'analyze_node' if trust_score >= 30 (site trusted enough to analyze)
    """
    trust_score = state.get('trust_score', 100)

    if trust_score < 30:
        return 'output_node'
    else:
        return 'analyze_node'
