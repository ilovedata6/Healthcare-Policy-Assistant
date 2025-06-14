from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from app.config import settings
from app.logging_config import logger


class TextSplitter:
    """Splits Documents into overlapping chunks for embeddings/indexing."""

    def __init__(
        self,
        chunk_size: int = settings.CHUNK_SIZE,
        chunk_overlap: int = settings.CHUNK_OVERLAP,
    ) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split(self, docs: List[Document]) -> List[Document]:
        try:
            chunks = self.splitter.split_documents(docs)
            logger.info(f"Split {len(docs)} documents into {len(chunks)} chunks")
            return chunks
        except Exception as exc:
            logger.error(f"Failed to split documents: {exc}")
            return []
