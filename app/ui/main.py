import streamlit as st
from pathlib import Path

from app.config import settings
from app.logging_config import logger
from app.data_ingestion.loader import PDFLoader
from app.data_ingestion.splitter import TextSplitter
from app.data_ingestion.store import VectorStoreManager
from app.rag.chain import RAGService

    # Sidebar handles upload & indexing; returns updated vector_store
from app.ui.sidebar import render_sidebar
from app.ui.chat_interface import render_chat


def main() -> None:
    # Page config
    st.set_page_config(page_title="Healthcare Policy Assistant", page_icon="⚕️")
    st.title("⚕️ Healthcare Policy Assistant")
    st.caption("Ask questions about insurance coverage, claims, and medication policies")

    # Initialize or load vector store
    vsm = VectorStoreManager(settings.VECTOR_STORE_DIR)
    if (settings.VECTOR_STORE_DIR / "index.pkl").exists():
        try:
            vector_store = vsm.load_store()
        except Exception:
            st.error("Failed to load existing index. Please reprocess documents.")
            vector_store = None
    else:
        vector_store = None
        vector_store = render_sidebar(vector_store)


    if vector_store is None:
        st.info("⚠️ Please upload policy documents to begin")
        st.stop()

    # Instantiate RAG
    rag = RAGService(vector_store)

    render_chat(rag)


if __name__ == "__main__":
    logger.info("Starting Streamlit app")
    main()
