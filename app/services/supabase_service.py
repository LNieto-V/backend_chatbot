"""Supabase client initialization and setup."""

from supabase import Client, create_client

from app.core.config import get_settings


def get_supabase_client() -> Client:
    """Initialize and return a Supabase client instance.

    Returns:
        Supabase Client ready to interact with the database.

    Raises:
        ValueError: If Supabase credentials are not found in the environment.
    """
    settings = get_settings()

    if not settings.supabase_url or not settings.supabase_key:
        raise ValueError(
            "Supabase credentials are not configured. "
            "Please set SUPABASE_URL and SUPABASE_KEY."
        )

    return create_client(settings.supabase_url, settings.supabase_key)
