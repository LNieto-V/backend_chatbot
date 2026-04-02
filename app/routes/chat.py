"""Chat route — POST /chat endpoint."""

from fastapi import APIRouter

from app.controllers.chat_controller import handle_chat
from app.models.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post(
    "",
    response_model=ChatResponse,
    summary="Send a message to the agricultural assistant",
    description="Sends a user message and receives an AI-generated response "
    "with agricultural monitoring insights.",
)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message."""
    return await handle_chat(request)
