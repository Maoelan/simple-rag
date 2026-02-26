import os
import time
import random
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

app = FastAPI(title="Learning RAG Demo")

# Pretend this is a real embedding model
def fake_embed(text: str):
    # Seed based on input so it's "deterministic"
    random.seed(abs(hash(text)) % 10000)
    return [random.random() for _ in range(128)]  # Small vector for demo

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

def simple_answer(state):
    ctx = state["context"]
    if ctx:
        answer = f"I found this: '{ctx[0][:100]}...'"
    else:
        answer = "Sorry, I don't know."
    state["answer"] = answer
    return state

# Build graph
workflow = StateGraph(dict)
workflow.add_node("retrieve", simple_retrieve)
workflow.add_node("answer", simple_answer)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "answer")
workflow.add_edge("answer", END)
chain = workflow.compile()

# --- API ENDPOINTS ---
class QuestionRequest(BaseModel):
    question: str

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

class DocumentRequest(BaseModel):
    text: str

@app.post("/add")
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