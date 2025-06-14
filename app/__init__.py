# Initialize the app module

# Import necessary submodules to ensure proper module recognition
from . import config
from . import logging_config
from .data_ingestion import loader, splitter, store
from .embeddings import openai_embeddings
from .rag import chain, prompt, retriever
from .ui import chat_interface, main, sidebar
from .utils import exceptions