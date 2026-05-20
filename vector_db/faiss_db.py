import os
import pickle
import faiss
import numpy as np
from typing import List, Tuple
from .base import VectorDB
from config import config

class FaissDB(VectorDB):
    def __init__(self):
        self.index = None
        self.texts = {}
        self.next_id = 0
        os.makedirs(config.FAISS_INDEX_PATH, exist_ok=True)

    def connect(self):
        index_path = os.path.join(config.FAISS_INDEX_PATH, "index.faiss")
        texts_path = os.path.join(config.FAISS_INDEX_PATH, "texts.pkl")
        
        if os.path.exists(index_path) and os.path.exists(texts_path):
            self.index = faiss.read_index(index_path)
            with open(texts_path, 'rb') as f:
                data = pickle.load(f)
                self.texts = data['texts']
                self.next_id = data['next_id']
        else:
            self.index = faiss.IndexFlatL2(384)
            self.texts = {}
            self.next_id = 0

    def disconnect(self):
        index_path = os.path.join(config.FAISS_INDEX_PATH, "index.faiss")
        texts_path = os.path.join(config.FAISS_INDEX_PATH, "texts.pkl")
        
        faiss.write_index(self.index, index_path)
        with open(texts_path, 'wb') as f:
            pickle.dump({'texts': self.texts, 'next_id': self.next_id}, f)

    def create_collection(self, collection_name: str):
        pass

    def insert_vectors(self, collection_name: str, vectors: List[List[float]], texts: List[str]):
        vectors_np = np.array(vectors).astype('float32')
        self.index.add(vectors_np)
        
        for text in texts:
            self.texts[self.next_id] = text
            self.next_id += 1

    def search(self, collection_name: str, query_vector: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        query_np = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_np, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                results.append((self.texts.get(idx, ""), float(distances[0][i])))
        return results

    def delete_collection(self, collection_name: str):
        self.index = faiss.IndexFlatL2(384)
        self.texts = {}
        self.next_id = 0

    def collection_exists(self, collection_name: str) -> bool:
        return True