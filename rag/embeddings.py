from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

class ChromaEmbeddingWrapper:
    """Wraps ChromaDB's built-in ONNX embedding function for use with LangChain."""

    def __init__(self):
        self._fn = ONNXMiniLM_L6_V2()

    def embed_documents(self, texts):
        return self._fn(texts)

    def embed_query(self, text):
        return self._fn([text])[0]


def get_embeddings():
    # Uses ChromaDB's built-in ONNX MiniLM model
    # No transformers/huggingface_hub dependency — works offline out of the box
    return ChromaEmbeddingWrapper()
