from typing import List, Tuple
from vector_db import get_vector_db
from embedding import EmbeddingModel
from config import config

class RAGService:
    _instance = None
    
    def __init__(self):
        self.vector_db = get_vector_db()
        self.embedding_model = EmbeddingModel.get_instance()
        self.collection_name = "knowledge_base"
        self.vector_db.connect()
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RAGService()
        return cls._instance
    
    def add_documents(self, texts: List[str]):
        vectors = self.embedding_model.encode(texts)
        self.vector_db.insert_vectors(self.collection_name, vectors, texts)
        self.vector_db.disconnect()
        self.vector_db.connect()
    
    def search_knowledge(self, query: str, top_k: int = config.MAX_RESULTS) -> List[Tuple[str, float]]:
        query_vector = self.embedding_model.encode(query)
        results = self.vector_db.search(self.collection_name, query_vector, top_k)
        return results
    
    def generate_response(self, query: str) -> str:
        results = self.search_knowledge(query)
        
        if not results:
            return "抱歉，我没有找到相关的知识信息。"
        
        context = "\n".join([f"- {text}" for text, _ in results])
        response = f"根据知识库内容，为您解答如下：\n\n{context}\n\n如果您还有其他问题，请随时提问。"
        return response
    
    def clear_knowledge(self):
        self.vector_db.delete_collection(self.collection_name)

rag_service = RAGService()