## How to Run

1. Clone the repository

   ```bash
   git clone https://github.com/Maoelan/simple-rag.git
   ```

2. Open the project in IDE, then open a terminal

3. Set up the virtual environment

   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Rename `.env.example` to `.env`, then fill in the following values

   ```env
   QDRANT_URL=http://localhost:6333
   COLLECTION_NAME=demo_collection
   VECTOR_SIZE=128
   DISTANCE=COSINE
   ```

5. _(Optional)_ Start Qdrant via Docker

   ```bash
   docker-compose up -d
   # or
   docker run -d -p 6333:6333 --name qdrant-container my-qdrant
   ```

   > **Note:** This step is optional. If Docker is not running, the app will automatically fall back to in-memory storage and still run normally.

6. Run the application

   ```bash
   uvicorn main:app --reload --port 8000
   ```

7. Open the API docs in your browser: [http://localhost:8000/docs](http://localhost:8000/docs)
