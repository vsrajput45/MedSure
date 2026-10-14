import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import api_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=f"{settings.PROJECT_NAME} API",
    description=f"AI-Powered Healthcare Cost Transparency, Medical Bill Auditing & Fair-Price Estimation Platform. Tagline: {settings.TAGLINE} ({settings.HINDI_TAGLINE})",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

import logging
from fastapi.exceptions import HTTPException, RequestValidationError

logger = logging.getLogger("medsure")

# CORS Configuration for local frontend and test runners
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Performance & Request Logging Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Global Exception Handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    if isinstance(exc, RequestValidationError):
        return JSONResponse(status_code=422, content={"detail": exc.errors()})
    
    logger.exception("Unhandled server exception processing %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please contact MEDSURE support."}
    )

# Include API v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "tagline": settings.TAGLINE,
        "hindi_tagline": settings.HINDI_TAGLINE,
        "demo_mode": settings.DEMO_MODE_ENABLED
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "tagline": settings.TAGLINE,
        "hindi_tagline": settings.HINDI_TAGLINE,
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
