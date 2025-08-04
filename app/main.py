from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from app.routes.chat import router as chat_router
from app.routes.ingest import router as ingest_router
from app.utils.config import settings
from app.schemas.request_model import HealthResponse

# Validate settings on startup
try:
    settings.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your .env file and ensure OPENAI_API_KEY is set.")
    exit(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("🚀 Starting ContextAgent...")
    print(f"📊 Model: {settings.OPENAI_MODEL}")
    print(f"🗄️  Vector Store: {settings.VECTOR_STORE_TYPE}")
    print(f"🌐 Server: {settings.HOST}:{settings.PORT}")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down ContextAgent...")

# Create FastAPI app
app = FastAPI(
    title="ContextAgent",
    description="A modular AI assistant backend with RAG and LangChain agents",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)
app.include_router(ingest_router)

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with health check."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        components={
            "openai": "configured" if settings.OPENAI_API_KEY else "missing",
            "vector_store": settings.VECTOR_STORE_TYPE,
            "search_tool": "available" if settings.SERP_API_KEY else "unavailable"
        }
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        components={
            "openai": "configured" if settings.OPENAI_API_KEY else "missing",
            "vector_store": settings.VECTOR_STORE_TYPE,
            "search_tool": "available" if settings.SERP_API_KEY else "unavailable"
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    ) 