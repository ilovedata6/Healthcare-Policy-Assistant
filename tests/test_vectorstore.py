from app.data_ingestion.store import VectorStoreManager
from app.data_ingestion.splitter import TextSplitter
from app.data_ingestion.loader import PDFLoader
from pathlib import Path

def test_vector_store_creation(tmp_path):
    loader = PDFLoader(docs_dir=Path("tests/assets"))
    docs = loader.load_pdfs()
    splitter = TextSplitter()
    chunks = splitter.split(docs)

    vsm = VectorStoreManager(store_dir=tmp_path)
    vs = vsm.create_store(chunks)
    assert vs is not None

    loaded = vsm.load_store()
    assert loaded is not None
