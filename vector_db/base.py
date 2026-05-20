from abc import ABC, abstractmethod
from typing import List, Tuple

class VectorDB(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def create_collection(self, collection_name: str):
        pass

    @abstractmethod
    def insert_vectors(self, collection_name: str, vectors: List[List[float]], texts: List[str]):
        pass

    @abstractmethod
    def search(self, collection_name: str, query_vector: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass

    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        pass