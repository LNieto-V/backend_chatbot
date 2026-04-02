"""LLM service — provides interface to Gemini via LangChain."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings
from app.utils.prompt_loader import load_markdown_file

settings = get_settings()


def get_gemini_model() -> ChatGoogleGenerativeAI:
    """Initialize the Gemini model for chat completion."""
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=settings.google_api_key,
        temperature=0.2,
    )


async def generate_response(
    user_input: str,
    sensor_context: str = "No current sensor data provided.",
    trend_context: str = "No trend data provided.",
    retrieved_context: str = "No additional context found.",
) -> str:
    """Generate a response using the Gemini model and a structured prompt.

    Args:
        user_input: The user's message.
        sensor_context: Relevant sensor readings.
        trend_context: Analysis of the sensor reading evolution.
        retrieved_context: Context from the knowledge base (Stage 5+).

    Returns:
        The generated response string.
    """
    # Load system prompt template and rules
    system_prompt = load_markdown_file("system_prompt.md")
    rules = load_markdown_file("rules.md")

    # Prepare the prompt template
    # The PromptTemplate class from LangChain can handle variables between curly braces
    prompt = PromptTemplate.from_template(system_prompt)

    # Prepare chain
    model = get_gemini_model()
    chain = prompt | model | StrOutputParser()

    # Invoke the chain
    response = await chain.ainvoke(
        {
            "sensor_context": sensor_context,
            "trend_context": trend_context,
            "retrieved_context": retrieved_context,
            "rules": rules,
            "input": user_input,
        }
    )

    return response
