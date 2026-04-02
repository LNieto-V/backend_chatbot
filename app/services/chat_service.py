"""Chat service — handles chat message processing.

Stage 2: Integrates with LLM via LangChain.
"""

from app.services.llm_service import generate_response
from app.utils.prompt_loader import load_markdown_file


async def process_message(message: str) -> str:
    """Process a user message and return a response from the LLM.

    Args:
        message: The user's input message.

    Returns:
        A response string from the AI.
    """
    # Load basic context for Stage 2 (static markdown files)
    sensor_context = load_markdown_file("database.md")
    trend_context = load_markdown_file("trend_context.md")

    # In Stage 2, there is no RAG yet,
    # so retrieved_context will be empty or a generic placeholder.
    retrieved_context = (
        "En esta etapa aún no se realiza la recuperación de conocimiento específico."
    )

    # Call the LLM to generate the response
    response = await generate_response(
        user_input=message,
        sensor_context=sensor_context,
        trend_context=trend_context,
        retrieved_context=retrieved_context,
    )

    return response
