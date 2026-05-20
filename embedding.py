from sentence_transformers import SentenceTransformer
from config import config

class EmbeddingModel:
    _instance = None
    
    def __init__(self):
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = EmbeddingModel()
        return cls._instance
    
    def encode(self, texts):
        if isinstance(texts, str):
            return self.model.encode(texts).tolist()
        return [self.model.encode(text).tolist() for text in texts]