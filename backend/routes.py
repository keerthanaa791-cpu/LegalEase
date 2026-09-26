from fastapi import APIRouter, HTTPException
from backend.config import get_settings
from backend.schemas import DocumentRequest, DocumentResponse
from backend.ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()

@router.get("/health")
def health():
    settings = get_settings()
    return {"status": "ok", "service": settings.app_name, "model": settings.gemini_model}

@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    settings = get_settings()
    try:
        clauses = [x.strip() for x in request.terms.split(";") if x.strip()]
        if len(clauses) > settings.max_terms:
            raise HTTPException(status_code=422, detail=f"Maximum {settings.max_terms} terms are allowed")
        generator = GeminiDocumentGenerator(settings)
        content = generator.generate_document(request.document_type, request.parties, request.terms, request.effective_date)
        if len(content) > settings.max_text_length:
            raise HTTPException(status_code=502, detail="Generated document is unexpectedly large")
        return DocumentResponse(document_type=request.document_type, content=content, terms=clauses, model=settings.gemini_model)
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Document generation failed: {exc}") from exc
