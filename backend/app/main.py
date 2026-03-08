import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import AnalyzeRequest, AnalyzeResponse, TacticDetail
from app.graph.graph import compiled_graph

app = FastAPI(
    title="PriceCheck API",
    description="Backend API for PriceCheck Chrome extension - exposes pricing manipulation tactics",
    version="1.0.0"
)

# CORS configuration for Chrome extension, Netlify, and local development
allowed_origins = [
    "chrome-extension://*",
    "http://localhost:5173",
    "http://localhost:3000",
]

# Add Netlify domains
allowed_origins.append("https://pricecheck-extension.netlify.app")

# Add custom frontend URL if set
frontend_url = os.getenv('FRONTEND_URL')
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Main analysis endpoint.
    Accepts page content from extension, runs LangGraph pipeline,
    and returns gaslighting score and tactics.
    """
    try:
        # Convert request to state dict for LangGraph
        initial_state = {
            "input_type": request.input_type,
            "page_url": request.page_url,
            "page_title": request.page_title,
            "body_text": request.body_text,
            "price_elements": request.price_elements,
            "raw_image": request.raw_image,
            "manual_text": request.manual_text,
            # Initialize output fields with defaults
            "trust_score": 100,
            "trust_signals": [],
            "trust_gate_pass": True,
            "tactics": [],
            "marketed_price": None,
            "real_price": None,
            "price_delta": None,
            "real_cost_note": None,
            "gaslighting_score": 0,
            "severity_label": "Honest Pricing",
            "is_scam": False,
            "error": None,
        }

        # Invoke the LangGraph pipeline
        result_state = compiled_graph.invoke(initial_state)

        # Convert tactics to TacticDetail models
        tactics = [
            TacticDetail(
                name=t.get("name", ""),
                severity=t.get("severity", 0),
                evidence=t.get("evidence", ""),
                explanation=t.get("explanation", "")
            )
            for t in result_state.get("tactics", [])
        ]

        # Build and return response
        return AnalyzeResponse(
            gaslighting_score=result_state.get("gaslighting_score", 0),
            severity_label=result_state.get("severity_label", "Honest Pricing"),
            tactics=tactics,
            trust_score=result_state.get("trust_score", 100),
            trust_signals=result_state.get("trust_signals", []),
            is_scam=result_state.get("is_scam", False),
            marketed_price=result_state.get("marketed_price"),
            real_price=result_state.get("real_price"),
            price_delta=result_state.get("price_delta"),
            error=result_state.get("error"),
        )

    except Exception as e:
        # Log the error and return error response
        print(f"[analyze] Error during analysis: {e}")
        return AnalyzeResponse(
            gaslighting_score=0,
            severity_label="Error",
            tactics=[],
            trust_score=0,
            trust_signals=[],
            is_scam=False,
            marketed_price=None,
            real_price=None,
            price_delta=None,
            error=str(e),
        )


@app.post("/debug-input")
async def debug_input(request: AnalyzeRequest):
    """
    Debug endpoint that echoes back what was received from the extension.
    Returns the first 1000 characters of body_text, full price_elements array,
    page_title, and page_url.
    """
    return {
        "page_title": request.page_title,
        "page_url": request.page_url,
        "body_text_preview": request.body_text[:1000] if request.body_text else "",
        "body_text_length": len(request.body_text) if request.body_text else 0,
        "price_elements": request.price_elements,
        "has_price_16": "$16" in (request.body_text or ""),
        "has_41_off": "41%" in (request.body_text or ""),
        "has_27_50": "27.50" in (request.body_text or ""),
    }
