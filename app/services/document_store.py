from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

class DocumentStore:
    def __init__(self, embedding_service) :
        self.embedding_service = embedding_service
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
    
    def add(self, text: str):
        emb = self.embedding_service.embed(text)
        doc_id = len(self.docs)
        payload = {"text": text}

        if self.using_qdrant:
            self.qdrant.upsert(
                collection_name="demo_collection",
                points=[PointStruct(id=doc_id, vector=emb, payload=payload)]
            )
        else :
            self.docs.append(text)
        return doc_id

    def search(self, query: str) -> list[str]:
        emb = self.embedding_service.embed(query)
        result = []
        if self.using_qdrant:
            hits = self.qdrant.search(collection_name="demo_collection", query_vector=emb, limit=2)
            for hit in hits:
                result.append(hit.payload["text"])
        else:
            for doc in self.docs:
                if query.lower() in doc.lower():
                    result.append(doc)
            if not result and self.docs:
                result = [self.docs[0]]
        return result