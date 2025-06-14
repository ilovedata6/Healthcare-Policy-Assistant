from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document

from app.config import settings
from app.logging_config import logger


class PDFLoader:
    """Loads all PDFs from a directory into LangChain Documents."""

    def __init__(self, docs_dir: Path = settings.POLICY_DOCS_DIR) -> None:
        self.docs_dir = docs_dir

    def load_pdfs(self) -> List[Document]:
        docs: List[Document] = []
        pdf_paths = list(self.docs_dir.glob("*.pdf"))
        if not pdf_paths:
            logger.warning(f"No PDF files found to load in directory: {self.docs_dir}")
            return docs

        for pdf_path in pdf_paths:
            try:
                loader = PyPDFLoader(str(pdf_path))
                loaded = loader.load()
                # annotate metadata.source for tracing
                for doc in loaded:
                    doc.metadata["source"] = pdf_path.name
                docs.extend(loaded)
                logger.info(f"Loaded PDF: {pdf_path}")
            except Exception as exc:
                logger.error(f"Failed to load PDF: {pdf_path} error: {exc}")
        return docs
