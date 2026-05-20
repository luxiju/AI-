from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import uvicorn
from rag_service import rag_service
import os

app = FastAPI(title="智能客服RAG系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

class DocumentRequest(BaseModel):
    texts: List[str]

class DocumentResponse(BaseModel):
    success: bool
    message: str

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        answer = rag_service.generate_response(request.query)
        results = rag_service.search_knowledge(request.query)
        sources = [text for text, _ in results]
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/add_documents", response_model=DocumentResponse)
async def add_documents(request: DocumentRequest):
    try:
        rag_service.add_documents(request.texts)
        return DocumentResponse(success=True, message=f"成功添加 {len(request.texts)} 条文档")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/clear_knowledge", response_model=DocumentResponse)
async def clear_knowledge():
    try:
        rag_service.clear_knowledge()
        return DocumentResponse(success=True, message="知识库已清空")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

os.makedirs("templates", exist_ok=True)

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)