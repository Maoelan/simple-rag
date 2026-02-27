class EmbeddingService:
    def __init__(self) :
        self.vector_size = 128

    def embed(self, text: str) -> list[float]:
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.vector_size)]