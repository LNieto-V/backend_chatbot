"""Chat request and response models."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming chat message from the user."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User message to the agricultural assistant",
    )


class ChatResponse(BaseModel):
    """Response from the agricultural assistant."""

    response: str = Field(..., description="AI-generated response")
