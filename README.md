# Early Observation (main.py monolith structure)

## Setup

- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt

## Run Qdrant (using Docker with fallback using if condition - no problem if fallback is triggered)

- docker-compose up -d
- docker run -d -p 6333:6333 --name qdrant-container my-qdrant

## Observations

### Global Variables Identified

- `docs_memory` : in-memory document storage
- `qdrant` : Qdrant client instance
- `USING_QDRANT` : Qdrant connection flag
- `chain` : compiled LangGraph workflow

## Refactor Plan

- `fake_embed` > EmbeddingService
- `docs_memory` + `qdrant` > DocumentStore
- `simple_retrieve` > RetrieveNode
- `simple_answer` > AnswerNode
- `workflow` > RagWorkflow
- `/ask`, `/add`, `/status` > Router

---

# Refactor Version (Separation of Concerns)

## Layers

- **API Layer** : Router, Schemas
- **Business Logic Layer** : RagWorkflow, RetrieveNode, AnswerNode
- **Infrastructure Layer** : DocumentStore, EmbeddingService

## Folder Structure

```
simple-rag/
│
├── app/
│   ├── api/
│   │   ├── router.py
│   │   └── schemas.py
│   │
│   ├── nodes/
│   │   ├── answer_node.py
│   │   └── retrieve_node.py
│   │
│   ├── services/
│   │   ├── document_store.py
│   │   ├── embedding_service.py
│   │   └── rag_workflow.py
│   │
│   └── config.py
│
├── main.py
├── notes.md
├── README.md
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── .gitignore
```

## How to Run

1. Clone the repository

   ```bash
   git clone https://github.com/Maoelan/simple-rag.git
   ```

2. Open the project in VS Code, then open a terminal (`Ctrl + Shift + P` > **Terminal: Create New Terminal**)

3. Set up the virtual environment

   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. _(Optional)_ Start Qdrant via Docker

   ```bash
   docker-compose up -d
   # or
   docker run -d -p 6333:6333 --name qdrant-container my-qdrant
   ```

5. Run the application

   ```bash
   uvicorn main:app --reload --port 8000
   ```

6. Open the API docs in your browser: [http://localhost:8000/docs](http://localhost:8000/docs)
