from fastapi import APIRouter, HTTPException
import time
from .schemas import QuestionRequest, DocumentRequest

def create_router(rag_workflow, document_store):
    router = APIRouter()

    @router.post("/ask")
    def ask_question(req: QuestionRequest):
        start = time.time()
        try:
            result = rag_workflow.run(req.question)
            return {
                "question": req.question,
                "answer": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/add")
    def add_document(req: DocumentRequest):
        try:
            doc_id = document_store.add(req.text)
            return {
                "id": doc_id,
                "status": "added",
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/status")
    def status():
        return {
            "qdrant_ready": document_store.using_qdrant,
            "in_memory_docs_count": len(document_store.docs),
            "graph_ready": rag_workflow.chain is not None
        }

    return router