import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "faiss")
    MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
    MILVUS_PORT = int(os.getenv("MILVUS_PORT", 19530))
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./data/faiss_index")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2") #词嵌入模型
    DATA_DIR = "./data"
    MAX_RESULTS = 5

config = Config()