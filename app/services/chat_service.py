"""Chat service — handles chat message processing with RAG.

Stage 2: Integrates with LLM via LangChain.
Stage 5+: Integrates Vector Retrieval from Supabase.
"""

from app.services.llm_service import generate_response
from app.services.retrieval_service import retrieve_context
from app.utils.prompt_loader import load_markdown_file


async def process_message(message: str) -> str:
    """Process a user message using full RAG pipeline.

    Args:
        message: The user's input message.

    Returns:
        A response string from the AI.
    """
    # 1. Recuperar contexto dinámico de Supabase (Stage 5+)
    # Esto busca fragmentos relevantes del knowledge.md basándose en el mensaje
    retrieved_context = await retrieve_context(message)

    # 2. Cargar contexto estático de sensores y tendencias (Stage 2)
    # Por ahora vienen de archivos, en Stage 6 final podrían venir del request
    sensor_context = load_markdown_file("database.md")
    trend_context = load_markdown_file("trend_context.md")

    # 3. Generar respuesta con el LLM inyectando TODO el contexto
    response = await generate_response(
        user_input=message,
        sensor_context=sensor_context,
        trend_context=trend_context,
        retrieved_context=retrieved_context,
    )

    return response
