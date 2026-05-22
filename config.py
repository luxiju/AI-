import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "faiss")
    MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
    MILVUS_PORT = int(os.getenv("MILVUS_PORT", 19530))
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./data/faiss_index")
    EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-8B"
    EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "https://api-inference.modelscope.cn/v1")
    EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "")
    LLM_MODEL = "Qwen/Qwen3-32B"
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api-inference.modelscope.cn/v1")
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")
    DATA_DIR = "./data"
    MAX_RESULTS = 5

config = Config()