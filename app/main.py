from services.embedding_service import EmbeddingService
from services.document_store import DocumentStore
from services.rag_workflow import RagWorkflow
from nodes.retrieve_node import RetrieveNode
from nodes.answer_node import AnswerNode
from fastapi import FastAPI
from api.router import create_router

app = FastAPI(title="Learning RAG Demo")

embedding_service = EmbeddingService()
document_store = DocumentStore(embedding_service)
retrieve_node = RetrieveNode(document_store)
answer_node = AnswerNode()
rag_workflow = RagWorkflow(retrieve_node, answer_node)

router = create_router(rag_workflow, document_store)
app.include_router(router)