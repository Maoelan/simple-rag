# Super basic in-memory "storage" fallback
docs_memory = []

# Qdrant setup (assumes local instance)
try:
    qdrant = QdrantClient("http://localhost:6333")
    qdrant.recreate_collection(
        collection_name="demo_collection",
        vectors_config=VectorParams(size=128, distance=Distance.COSINE)
    )
    USING_QDRANT = True
except Exception as e:
    print("⚠️  Qdrant not available. Falling back to in-memory list.")
    USING_QDRANT = False