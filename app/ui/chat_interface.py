import streamlit as st
from app.rag.chain import RAGService
from app.logging_config import logger


def render_chat(rag: RAGService) -> None:
    """
    Renders the chat interface. Takes a preconfigured RAGService.
    Maintains full session history.
    """
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # [(role, message)]

    # Display previous messages
    for role, content in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(content)

    # New user input
    question = st.chat_input("Ask a policy question…")
    if not question:
        return

    # Store user message
    with st.chat_message("user"):
        st.write(question)
    st.session_state.chat_history.append(("user", question))

    # Get and display assistant response
    with st.chat_message("assistant", avatar="⚕️"):
        with st.spinner("🔎 Searching policies..."):
            try:
                answer = rag.ask(question)
                st.write(answer)
                st.session_state.chat_history.append(("assistant", answer))
            except Exception as exc:
                logger.error(f"Error during RAG ask: {exc}")
                st.error("Something went wrong. Please try again.")

            # Show source excerpts
            sources = rag.get_sources(question)
            if sources:
                with st.expander("View source excerpts"):
                    for i, doc in enumerate(sources, start=1):
                        meta = doc.metadata
                        source = meta.get("source", "unknown")
                        page = meta.get("page", "?")
                        st.caption(f"Source {i}: {source} (page {page})")
                        st.text(doc.page_content[:300].strip() + "…")