import streamlit as st
from pathlib import Path
from app.config import settings
from app.logging_config import logger
from app.data_ingestion.loader import PDFLoader
from app.data_ingestion.splitter import TextSplitter
from app.data_ingestion.store import VectorStoreManager
from langchain.schema import Document
from typing import Optional, Any
import os


def render_sidebar(current_store) -> Optional[Any]:
    """Renders sidebar for uploading & indexing PDF policies."""
    st.sidebar.header("📂 Policy Documents")
    uploaded_files = st.sidebar.file_uploader(
        "Upload policy PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files and st.sidebar.button("Process Documents"):
        status = st.sidebar.empty()
        status.info("📥 Saving uploads...")
        docs_dir = settings.POLICY_DOCS_DIR
        docs_dir.mkdir(exist_ok=True)

        # Save uploads
        for file in uploaded_files:
            dst = docs_dir / file.name
            with open(dst, "wb") as f:
                f.write(file.getbuffer())
            logger.info(f"Saved uploaded PDF: {dst}")

        # Load → Split → Index
        loader = PDFLoader(docs_dir)
        docs = loader.load_pdfs()  # type: list[Document]

        splitter = TextSplitter()
        chunks = splitter.split(docs)

        status.info(f"🔍 Creating vector store from {len(chunks)} chunks...")
        vsm = VectorStoreManager(settings.VECTOR_STORE_DIR)
        try:
            new_store = vsm.create_store(chunks)
            status.success("✅ Indexing complete!")
            return new_store
        except Exception:
            status.error("❌ Indexing failed. Check logs.")
            return current_store

    return current_store
