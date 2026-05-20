from .base import VectorDB
from .faiss_db import FaissDB
from .milvus_db import MilvusDB
from config import config

def get_vector_db() -> VectorDB:
    if config.VECTOR_DB_TYPE == "milvus":
        return MilvusDB()
    else:
        return FaissDB()