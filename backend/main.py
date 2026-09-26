from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import get_settings
from backend.routes import router

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0", description="AI-powered legal document drafting API")
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.get("/")
def root():
    return {"message": "LegalEase API is running", "docs": "/docs", "health": "/health"}
