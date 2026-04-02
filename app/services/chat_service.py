"""Chat service — handles chat message processing.

Stage 1: Returns mock responses.
Stage 2+: Will integrate with LLM.
"""


async def process_message(message: str) -> str:
    """Process a user message and return a response.

    Args:
        message: The user's input message.

    Returns:
        A response string.
    """
    return (
        f"[AgroNexus Mock] Recibí tu mensaje: '{message}'. "
        "El sistema de IA será integrado en el siguiente stage."
    )
