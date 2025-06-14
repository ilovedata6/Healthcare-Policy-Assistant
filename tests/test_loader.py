from app.data_ingestion.loader import PDFLoader
from pathlib import Path

def test_pdf_loader_empty(tmp_path):
    loader = PDFLoader(docs_dir=tmp_path)
    docs = loader.load_pdfs()
    assert docs == []

def test_pdf_loader_sample():
    loader = PDFLoader(docs_dir=Path("tests/assets"))  # put sample.pdf here
    docs = loader.load_pdfs()
    assert isinstance(docs, list)
    assert all("source" in d.metadata for d in docs)
