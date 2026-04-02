"""Retrieval service — searches for relevant context in Supabase."""

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import get_settings
from app.services.supabase_service import get_supabase_client

settings = get_settings()


def get_embeddings_model():
    """Initialize the embeddings model."""
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=settings.google_api_key
    )


async def retrieve_context(query: str, top_k: int = 5) -> str:
    """Retrieve relevant knowledge chunks based on query similarity.

    Args:
        query: The user message or question.
        top_k: Number of relevant fragments to retrieve.

    Returns:
        A concatenated string of relevant contexts.
    """
    try:
        # 1. Generar embedding de la búsqueda
        embeddings = get_embeddings_model()
        query_embedding = embeddings.embed_query(query)

        # 2. Llamar a la función RPC match_documents en Supabase
        supabase = get_supabase_client()
        response = supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_count": top_k,
                "filter": {},
            },
        ).execute()

        # 3. Formatear resultados
        if not response.data:
            return "No se encontró contexto relevante en la base de conocimientos."

        contexts = [item["content"] for item in response.data]
        return "\n\n---\n\n".join(contexts)

    except Exception as e:
        print(f"⚠️ Error en retrieval: {e}")
        return f"Error al recuperar contexto: {str(e)}"
