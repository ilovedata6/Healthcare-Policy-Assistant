import time
from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document

from app.config import settings
from app.logging_config import logger
from app.rag.prompt import get_prompt_template
from app.rag.retriever import get_retriever


class RAGService:
    """
    Encapsulates the RAG pipeline: retrieval, prompting, LLM call, and parsing.
    """

    def __init__(self, vector_store) -> None:
        self.logger = logger  # Use standard logger
        self.retriever = get_retriever(vector_store)
        self.prompt = get_prompt_template()
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL_NAME,
            temperature=settings.LLM_TEMPERATURE,
            api_key=settings.OPENAI_API_KEY,
        )
        self.parser = StrOutputParser()

        # Build the runnable chain
        # Input mapping: {"context": retriever, "question": passthrough}
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | self.parser
        )

    def ask(self, question: str) -> str:
        """
        Ask the RAG pipeline a question and return the answer.
        """
        self.logger.info(f"RAG ask started: {question}")
        start = time.time()
        answer = self.chain.invoke(question)
        elapsed = time.time() - start
        self.logger.info(f"RAG ask completed: {answer} (latency: {round(elapsed, 2)}s)")
        return answer

    def get_sources(self, question: str) -> List[Document]:
        """
        Return the raw documents retrieved for a given question.
        """
        return self.retriever.get_relevant_documents(question)
