# LangGraph state = plain dict
def simple_retrieve(state):
    query = state["question"]
    results = []
    emb = fake_embed(query)

    if USING_QDRANT:
        hits = qdrant.search(collection_name="demo_collection", query_vector=emb, limit=2)
        for hit in hits:
            results.append(hit.payload["text"])
    else:
        for doc in docs_memory:
            if query.lower() in doc.lower():
                results.append(doc)
        if not results and docs_memory:
            results = [docs_memory[0]]  # Just grab first

    state["context"] = results
    return state