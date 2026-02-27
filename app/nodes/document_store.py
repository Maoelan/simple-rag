from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

class DocumentStore:
    def __init__(self) :
        self.docs = []
        self.using_qdrant = False
        self.qdrant = None

        try:
            self.qdrant = QdrantClient("http://localhost:6333")
            self.qdrant.recreate_collection(
                collection_name="demo_collection",
                vectors_config=VectorParams(size=128, distance=Distance.COSINE)
            )
            self.using_qdrant = True
        except Exception as e:
            print("⚠️  Qdrant not available. Falling back to in-memory list.")