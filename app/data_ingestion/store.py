from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain.schema import Document

from app.config import settings
from app.logging_config import logger
from app.embeddings.openai_embeddings import get_embeddings


class VectorStoreManager:
    """Handles creation, persistence, and loading of the FAISS vector store."""

    def __init__(self, store_dir: Path = settings.VECTOR_STORE_DIR) -> None:
        self.store_dir = store_dir

    def create_store(self, docs: List[Document]) -> FAISS:
        """Builds a new FAISS index from Documents and saves it locally."""
        embeddings = get_embeddings()
        try:
            vs = FAISS.from_documents(docs, embeddings)
            vs.save_local(str(self.store_dir))
            logger.info(f"Vector store created and saved in directory: {self.store_dir}")
            return vs
        except Exception as exc:
            logger.error(f"Failed to create vector store: {exc}")
            raise

    def load_store(self) -> FAISS:
        """Loads an existing FAISS index from disk."""
        embeddings = get_embeddings()
        try:
            vs = FAISS.load_local(str(self.store_dir), embeddings, allow_dangerous_deserialization=True)
            logger.info(f"Vector store loaded from directory: {self.store_dir}")
            return vs
        except Exception as exc:
            logger.error(f"Failed to load vector store: {exc}")
            raise
