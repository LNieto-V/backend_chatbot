"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.routes.iot import router as iot_router

app = FastAPI(
    title="AgroNexus AI",
    description="Agricultural monitoring backend with RAG capabilities",
    version="0.1.0",
)

# CORS — allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(iot_router, prefix="/iot", tags=["IoT"])


@app.get("/", tags=["Health"])
async def root():
    """Service information endpoint."""
    return {"status": "ok", "service": "AgroNexus AI", "version": "0.1.0"}


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
