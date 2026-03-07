"""
LangGraph StateGraph definition for PriceCheck analysis pipeline.

Graph structure from PRD Part 5.3:
    START → input_router
    input_router → content_node | ocr_node | manual_node (conditional)
    content_node → trust_node
    ocr_node → trust_node
    manual_node → trust_node
    trust_node → trust_gate
    trust_gate → output_node | analyze_node (conditional)
    analyze_node → score_node
    score_node → output_node
    output_node → END
"""

from langgraph.graph import StateGraph, START, END

from app.graph.state import PriceCheckState
from app.graph.nodes import (
    input_router,
    content_node,
    ocr_node,
    manual_node,
    trust_node,
    trust_gate,
    analyze_node,
    score_node,
    output_node,
)
from app.graph.edges import route_by_input_type, route_by_trust


def build_graph() -> StateGraph:
    """
    Builds and returns the PriceCheck analysis StateGraph.
    """
    # Initialize the graph with PriceCheckState schema
    graph = StateGraph(PriceCheckState)

    # Add all nodes
    graph.add_node("input_router", input_router)
    graph.add_node("content_node", content_node)
    graph.add_node("ocr_node", ocr_node)
    graph.add_node("manual_node", manual_node)
    graph.add_node("trust_node", trust_node)
    graph.add_node("trust_gate", trust_gate)
    graph.add_node("analyze_node", analyze_node)
    graph.add_node("score_node", score_node)
    graph.add_node("output_node", output_node)

    # Add entry edge: START → input_router
    graph.add_edge(START, "input_router")

    # Add conditional edge from input_router based on input_type
    graph.add_conditional_edges(
        "input_router",
        route_by_input_type,
        {
            "content_node": "content_node",
            "ocr_node": "ocr_node",
            "manual_node": "manual_node",
        }
    )

    # Add edges from content processors to trust_node
    graph.add_edge("content_node", "trust_node")
    graph.add_edge("ocr_node", "trust_node")
    graph.add_edge("manual_node", "trust_node")

    # Add edge from trust_node to trust_gate
    graph.add_edge("trust_node", "trust_gate")

    # Add conditional edge from trust_gate based on trust_score
    graph.add_conditional_edges(
        "trust_gate",
        route_by_trust,
        {
            "output_node": "output_node",
            "analyze_node": "analyze_node",
        }
    )

    # Add edge from analyze_node to score_node
    graph.add_edge("analyze_node", "score_node")

    # Add edge from score_node to output_node
    graph.add_edge("score_node", "output_node")

    # Add terminal edge: output_node → END
    graph.add_edge("output_node", END)

    return graph


# Build and compile the graph for export
_graph = build_graph()
compiled_graph = _graph.compile()
