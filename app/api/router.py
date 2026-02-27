@app.post("/ask")
def ask_question(req: QuestionRequest):
    start = time.time()
    try:
        result = chain.invoke({"question": req.question})
        return {
            "question": req.question,
            "answer": result["answer"],
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def add_document(req: DocumentRequest):
    try:
        emb = fake_embed(req.text)
        doc_id = len(docs_memory)  # super unsafe ID!
        payload = {"text": req.text}

        if USING_QDRANT:
            qdrant.upsert(
                collection_name="demo_collection",
                points=[PointStruct(id=doc_id, vector=emb, payload=payload)]
            )
        else:
            docs_memory.append(req.text)

        return {"id": doc_id, "status": "added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
def status():
    return {
        "qdrant_ready": USING_QDRANT,
        "in_memory_docs_count": len(docs_memory),
        "graph_ready": chain is not None
    }