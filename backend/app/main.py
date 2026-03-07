from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import AnalyzeRequest, AnalyzeResponse

app = FastAPI(
    title="PriceCheck API",
    description="Backend API for PriceCheck Chrome extension - exposes pricing manipulation tactics",
    version="1.0.0"
)

# CORS configuration for Chrome extension and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome-extension://*",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
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
    Main analysis endpoint
    Accepts page content from extension and returns gaslighting score and tactics
    """
    # TODO: Implement LangGraph pipeline
    # For now, return a placeholder response
    return AnalyzeResponse(
        gaslighting_score=0,
        severity_label="Honest Pricing",
        tactics=[],
        trust_score=100,
        trust_signals=["Analysis not yet implemented"],
        is_scam=False,
        marketed_price=None,
        real_price=None,
        price_delta=None,
        error=None
    )
