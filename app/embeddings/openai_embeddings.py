from app.config import settings
from app.logging_config import logger
from langchain_openai import OpenAIEmbeddings
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import RateLimitError, APIError
import openai
import httpx


# Configure OpenAI client globally (optional, for lower‑level control)
openai.api_key = settings.OPENAI_API_KEY


@retry(
    retry=retry_if_exception_type((RateLimitError, APIError, httpx.HTTPError)),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(settings.RETRY_MAX_ATTEMPTS),
    reraise=True,
)
def get_embeddings() -> OpenAIEmbeddings:
    """
    Factory for OpenAIEmbeddings with retry logic.
    Reads model name and API key from settings.
    """
    logger.info(f"Initializing OpenAIEmbeddings model={settings.EMBEDDINGS_MODEL_NAME}")
    return OpenAIEmbeddings(
        model=settings.EMBEDDINGS_MODEL_NAME,
        api_key=settings.OPENAI_API_KEY,
        timeout=settings.HTTP_TIMEOUT,
    )
