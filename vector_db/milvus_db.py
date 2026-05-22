from typing import List, Tuple
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from .base import VectorDB
from config import config

class MilvusDB(VectorDB):
    def __init__(self):
        self.client = None

    def connect(self):
        connections.connect(
            alias="default",
            host=config.MILVUS_HOST,
            port=config.MILVUS_PORT
        )

    def disconnect(self):
        connections.disconnect("default")

    def create_collection(self, collection_name: str):
        if utility.has_collection(collection_name):
            return
        
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=4096),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
        ]
        schema = CollectionSchema(fields, "RAG knowledge base")
        self.client = Collection(collection_name, schema)
        
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }
        self.client.create_index("vector", index_params)

    def insert_vectors(self, collection_name: str, vectors: List[List[float]], texts: List[str]):
        if not utility.has_collection(collection_name):
            self.create_collection(collection_name)
        
        self.client = Collection(collection_name)
        entities = [
            {"vector": vectors[i], "text": texts[i]} 
            for i in range(len(vectors))
        ]
        self.client.insert(entities)
        self.client.flush()

    def search(self, collection_name: str, query_vector: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        if not utility.has_collection(collection_name):
            return []
        
        self.client = Collection(collection_name)
        self.client.load()
        
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10}
        }
        
        results = self.client.search(
            data=[query_vector],
            anns_field="vector",
            param=search_params,
            limit=top_k,
            expr=None,
            output_fields=["text"]
        )
        
        self.client.release()
        
        output = []
        for hit in results[0]:
            output.append((hit.entity.get("text"), hit.distance))
        return output

    def delete_collection(self, collection_name: str):
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)

    def collection_exists(self, collection_name: str) -> bool:
        return utility.has_collection(collection_name)