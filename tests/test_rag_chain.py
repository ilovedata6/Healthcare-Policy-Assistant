from app.rag.chain import RAGService
from app.data_ingestion.store import VectorStoreManager

def test_rag_inference():
    vsm = VectorStoreManager()
    vs = vsm.load_store()
    rag = RAGService(vs)

    result = rag.ask("Does this policy cover maternity?")
    assert isinstance(result, str)
    assert len(result) > 0
