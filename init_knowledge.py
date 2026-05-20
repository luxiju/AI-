import os
from rag_service import rag_service

def load_sample_knowledge():
    knowledge_file = "./data/sample_knowledge.txt"
    
    if not os.path.exists(knowledge_file):
        print("未找到示例知识库文件")
        return
    
    with open(knowledge_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    texts = [line.strip() for line in lines if line.strip()]
    
    if texts:
        rag_service.add_documents(texts)
        print(f"成功加载 {len(texts)} 条知识库文档")
    else:
        print("知识库文件为空")

if __name__ == "__main__":
    load_sample_knowledge()