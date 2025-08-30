"""
FastAPI main application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import structlog

from backend.app.core.config import settings
from backend.app.core.logging import get_logger
from backend.app.db.database import init_db, close_db

# Import routers (will be created next)
# from backend.app.api.routers import auth, workflow, analytics, documents, compliance, clients

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("Starting application", app_name=settings.APP_NAME, version=settings.VERSION)
    
    # Initialize database
    if settings.APP_ENV != "testing":
        await init_db()
        logger.info("Database initialized")
    
    # Initialize other services here
    # TODO: Initialize ChromaDB, Redis, etc.
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    await close_db()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add X-Process-Time header to responses"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    logger.info(
        "Request received",
        method=request.method,
        url=str(request.url),
        client=request.client.host if request.client else None
    )
    
    try:
        response = await call_next(request)
        logger.info(
            "Request completed",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code
        )
        return response
    except Exception as e:
        logger.error(
            "Request failed",
            method=request.method,
            url=str(request.url),
            error=str(e),
            exc_info=True
        )
        raise


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
        "debug": settings.DEBUG
    }


# Include routers (uncomment when created)
# app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(workflow.router, prefix="/api/workflow", tags=["Workflow"])
# app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
# app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
# app.include_router(compliance.router, prefix="/api/compliance", tags=["Compliance"])
# app.include_router(clients.router, prefix="/api/clients", tags=["Clients"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(
        "Unhandled exception",
        error=str(exc),
        path=request.url.path,
        exc_info=True
    )
    
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc),
                "type": type(exc).__name__
            }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )