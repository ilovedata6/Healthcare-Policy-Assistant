# app/config.py

from pathlib import Path
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ─── Environment & Paths ─────────────────────────────────────
    ENV_FILE: Path = Field(default=Path(".env"), description="Path to .env file")
    POLICY_DOCS_DIR: Path = Field(default=Path("policy_documents"), description="Dir for uploaded PDFs")
    VECTOR_STORE_DIR: Path = Field(default=Path("vector_store"), description="Dir to persist FAISS index")

    # ─── OpenAI / LLM ────────────────────────────────────────────
    OPENAI_API_KEY: SecretStr = Field(..., description="OpenAI API key")
    LLM_MODEL_NAME: str = Field(default="gpt-4-turbo", description="OpenAI chat model")
    LLM_TEMPERATURE: float = Field(default=0.0, ge=0.0, le=2.0, description="LLM sampling temperature")

    # ─── Embeddings ──────────────────────────────────────────────
    EMBEDDINGS_MODEL_NAME: str = Field(default="text-embedding-3-small")
    
    # ─── Text Splitting ──────────────────────────────────────────
    CHUNK_SIZE: int = Field(default=1000, ge=100, le=2000, description="Max chars per chunk")
    CHUNK_OVERLAP: int = Field(default=200, ge=0, le=500, description="Overlap between chunks")

    # ─── Retrieval ────────────────────────────────────────────────
    RETRIEVER_K: int = Field(default=4, ge=1, description="Number of docs to retrieve per query")

    # ─── Retry / HTTP ────────────────────────────────────────────
    HTTP_TIMEOUT: float = Field(default=30.0, description="HTTPX timeout in seconds")
    RETRY_MAX_ATTEMPTS: int = Field(default=3, ge=1, description="Max retry attempts for LLM calls")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        fields = {
            "OPENAI_API_KEY": {"env": "OPENAI_API_KEY"}
        }

    @field_validator("POLICY_DOCS_DIR", mode="before")
    def ensure_policy_docs_dir(cls, v):
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @field_validator("VECTOR_STORE_DIR", mode="before")
    def ensure_vector_store_dir(cls, v):
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return path


# Provide a singleton settings instance
settings = Settings()
