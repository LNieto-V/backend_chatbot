"""Vercel serverless entry point.

Re-exports the FastAPI app instance for @vercel/python runtime.
"""

from app.main import app

__all__ = ["app"]
