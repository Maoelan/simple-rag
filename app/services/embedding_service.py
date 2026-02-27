import random
from config import settings

class EmbeddingService:
    def __init__(self) :
        self.vector_size = settings.vector_size

    def embed(self, text: str) -> list[float]:
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.vector_size)]