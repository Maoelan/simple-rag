# Observe & Run

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run Qdrant

```bash
docker-compose up -d
```

## Run App

```bash
uvicorn main:app --reload --port 8000
```

Open browser: http://localhost:8000/docs

---

## Observations

### Global Variables Identified

| Variable       | Type                        |
| -------------- | --------------------------- |
| `docs_memory`  | In-memory document storage  |
| `qdrant`       | Qdrant client instance      |
| `USING_QDRANT` | Qdrant connection flag      |
| `chain`        | Compiled LangGraph workflow |

### Refactor Plan

| Original                  | Class              |
| ------------------------- | ------------------ |
| `fake_embed`              | `EmbeddingService` |
| `docs_memory` + `qdrant`  | `DocumentStore`    |
| `simple_retrieve`         | `RetrieveNode`     |
| `simple_answer`           | `AnswerNode`       |
| `workflow`                | `RagWorkflow`      |
| `/ask`, `/add`, `/status` | `Router`           |
