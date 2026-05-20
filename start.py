import os
import sys

def main():
    print("=== 智能客服RAG系统 ===")
    print("正在启动服务...")
    
    os.system("python -m uvicorn main:app --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main()