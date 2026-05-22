from openai import OpenAI
from config import config

class EmbeddingModel:
    _instance = None
    
    def __init__(self):
        self.client = OpenAI(
            base_url=config.EMBEDDING_BASE_URL,
            api_key=config.EMBEDDING_API_KEY
        )
        self.model = config.EMBEDDING_MODEL
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = EmbeddingModel()
        return cls._instance
    
    def encode(self, texts):
        if isinstance(texts, str):
            response = self.client.embeddings.create(
                model=self.model,
                input=texts,
                encoding_format="float"
            )
            return response.data[0].embedding
        
        results = []
        for text in texts:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
                encoding_format="float"
            )
            results.append(response.data[0].embedding)
        return results