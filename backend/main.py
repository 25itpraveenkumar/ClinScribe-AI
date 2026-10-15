"""ClinScribe-AI FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.documentation import router as documentation_router

app = FastAPI(
    title="ClinScribe-AI API",
    description=(
        "Consent-gated clinical documentation prototype. Generates conservative "
        "SOAP drafts with source traceability; clinician approval is mandatory. "
        "Not validated for production clinical use and does not persist to an EHR."
    ),
    version="0.2.0",
)

# Restrict origins through environment/configuration before deployment. This
# permissive setting is convenient for a local hackathon frontend only.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8501", "http://localhost:8501", "http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
app.include_router(documentation_router)


@app.get("/", tags=["Health"], summary="API welcome")
def root() -> dict[str, str]:
    return {"service": "ClinScribe-AI API", "status": "running", "docs": "/docs"}


@app.get("/health", tags=["Health"], summary="Health check")
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "clinscribe-ai"}
