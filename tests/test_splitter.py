from app.data_ingestion.splitter import TextSplitter
from langchain.schema import Document

def test_splitter_basic():
    doc = Document(page_content="A" * 3000, metadata={})
    splitter = TextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split([doc])
    assert len(chunks) >= 2
    assert all(len(chunk.page_content) <= 1000 for chunk in chunks)
