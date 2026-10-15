from app.rag.embedder import embed_texts

def test_embed_texts_returns_list():
    texts = ["The pacemaker lead exhibited undersensing."]
    embeddings = embed_texts(texts)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 1

def test_embed_texts_correct_dimensions():
    texts = ["The device failed during use."]
    embeddings = embed_texts(texts)
    assert len(embeddings[0]) == 384

def test_embed_multiple_texts():
    texts = ["Report one.", "Report two.", "Report three."]
    embeddings = embed_texts(texts)
    assert len(embeddings) == 3