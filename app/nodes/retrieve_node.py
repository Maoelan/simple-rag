class RetrieveNode:
    def __init__(self, embedding_service, document_store):
        self.embedding_service = embedding_service
        self.document_store = document_store
    
    def run(self, state):
        query = state["question"]
        result = []
        emb = self.embedding_service.embed(query)

        if self.document_store.using_qdrant:
            hits = self.document_store.qdrant.search(collection_name="demo_collection", query_vector=emb, limit=2)
            for hit in hits:
                result.append(hit.payload["text"])
        else:
            for doc in self.document_store.docs:
                if query.lower() in doc.lower():
                    result.append(doc)
            if not result and self.document_store.docs:
                result = [self.document_store.docs[0]]
        
        state["context"] = result
        return state