"""Chat controller — orchestrates chat request handling."""

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_message


async def handle_chat(request: ChatRequest) -> ChatResponse:
    """Handle an incoming chat request.

    Args:
        request: Validated chat request with user message.

    Returns:
        ChatResponse with the generated response.
    """
    response = await process_message(request.message)
    return ChatResponse(response=response)
