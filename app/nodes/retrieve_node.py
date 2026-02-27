class RetrieveNode:
    def __init__(self, document_store):
        self.document_store = document_store
    
    def run(self, state):
        query = state["question"]
        state["context"] = self.document_store.search(query)
        return state