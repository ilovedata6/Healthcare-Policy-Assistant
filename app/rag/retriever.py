from langchain.schema import BaseRetriever
from langchain_community.vectorstores import FAISS
from app.config import settings
from app.logging_config import logger


def get_retriever(vector_store: FAISS) -> BaseRetriever:
    """
    Wraps the FAISS vector store into a LangChain retriever,
    using the configured 'k' for number of docs to return.
    """
    logger.info(f"Creating retriever k={settings.RETRIEVER_K}")
    return vector_store.as_retriever(search_kwargs={"k": settings.RETRIEVER_K})
