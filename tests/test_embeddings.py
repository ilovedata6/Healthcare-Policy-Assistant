from app.embeddings.openai_embeddings import get_embeddings

def test_embedding_instance():
    embeddings = get_embeddings()
    assert embeddings is not None
    assert hasattr(embeddings, "embed_query")
