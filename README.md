# 智能客服RAG系统

基于 RAG（Retrieval-Augmented Generation）技术的本地智能客服系统，支持 FAISS 和 Milvus 两种向量数据库检索方式。

## 📁 项目结构

```
RAG/
├── main.py                 # FastAPI 后端服务入口
├── config.py               # 配置文件（向量数据库类型、路径等）
├── embedding.py            # 文本向量化模型封装
├── rag_service.py          # RAG 核心服务逻辑
├── start.py                # 服务启动脚本
├── init_knowledge.py       # 知识库初始化脚本
├── requirements.txt        # Python 依赖清单
├── .env                    # 环境变量配置
├── data/
│   ├── sample_knowledge.txt    # 示例知识库数据
│   └── faiss_index/            # FAISS 索引文件存储目录
├── vector_db/
│   ├── __init__.py             # 向量数据库工厂函数
│   ├── base.py                 # 向量数据库抽象基类
│   ├── faiss_db.py             # FAISS 实现
│   └── milvus_db.py            # Milvus 实现
└── templates/
    └── index.html              # 前端聊天界面
```

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Conda（推荐）或虚拟环境
- Docker（仅使用 Milvus 时需要）

---

## 🔧 步骤 1：创建并激活虚拟环境

```bash
# 使用 Conda 创建环境
conda create -n rag-chatbot python=3.10 -y

# 激活环境
conda activate rag-chatbot
```

**产出**：创建了一个名为 `rag-chatbot` 的隔离 Python 环境，避免依赖冲突。

**意义**：确保项目依赖与系统其他 Python 项目隔离，保证环境一致性。

---

## 🔧 步骤 2：安装依赖

```bash
# 进入项目目录
cd e:\RAG

# 安装基础依赖
pip install -r requirements.txt

# 如果遇到 NumPy 2.x 兼容性问题，执行：
pip install "numpy<2.0"

# 如果遇到 marshmallow 兼容性问题，执行：
pip install "marshmallow<3.20"
```

**产出**：安装了所有必要的 Python 库（FastAPI、FAISS、pymilvus、sentence-transformers 等）。

**意义**：
- `fastapi` + `uvicorn`：构建和运行 Web 服务
- `faiss-cpu`：轻量级本地向量数据库
- `pymilvus`：Milvus 向量数据库客户端
- `sentence-transformers`：文本向量化模型（用于将文字转为向量）

---

## 🔧 步骤 3：配置向量数据库

### 方式 A：使用 FAISS（默认，推荐本地开发）

无需额外配置，系统默认使用 FAISS。

**配置文件** `.env`：
```env
VECTOR_DB_TYPE=faiss
FAISS_INDEX_PATH=./data/faiss_index
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 方式 B：使用 Milvus（需要 Docker）

**修改配置文件** `.env`：
```env
VECTOR_DB_TYPE=milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

**启动 Milvus 服务**（需要 Docker 已安装）：
```bash
docker run -d --name milvus-standalone \
  -p 19530:19530 \
  -p 9091:9091 \
  -v ${PWD}/volumes/milvus:/var/lib/milvus \
  milvusdb/milvus:v2.4.4
```

**产出**：配置了向量数据库类型。

**意义**：选择适合的向量存储方案——FAISS 适合单机轻量场景，Milvus 适合大规模分布式场景。

---

## 🔧 步骤 4：初始化知识库

```bash
python init_knowledge.py
```

**预期输出**：
```
modules.json: 100%|██████████████████████████████████| 349/349
model.safetensors: 100%|█████████████████████████████| 90.9M/90.9M
...
成功加载 10 条知识库文档
```

**产出**：
1. 下载了 `all-MiniLM-L6-v2` 向量化模型（约 90MB）
2. 将 `data/sample_knowledge.txt` 中的 10 条文本转换为向量
3. 向量存储到 FAISS 索引文件（`data/faiss_index/index.faiss`）

**意义**：
- 模型下载：获取文本向量化能力
- 文本向量化：将人类语言转为计算机可理解的向量（384 维）
- 索引构建：建立向量索引，支持快速相似性搜索

---

## 🔧 步骤 5：启动服务

```bash
python main.py
```

**预期输出**：
```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**产出**：启动了一个 FastAPI Web 服务，监听在 `http://localhost:8000`。

**意义**：
- 提供 HTTP API 接口供前端调用
- 提供 WebSocket 或 RESTful 方式的问答服务
- 前端界面可直接访问

---

## 🔧 步骤 6：访问前端界面

打开浏览器，访问：
```
http://localhost:8000
```

**界面功能**：
1. **状态显示**：显示服务状态和当前使用的向量数据库类型
2. **知识库管理**：可添加新的知识库文档（每行一条）
3. **聊天界面**：与智能客服对话

**使用流程**：
1. 在"添加知识库文档"区域输入知识内容，点击"添加文档"
2. 在底部输入框输入问题，点击"发送"或按 Enter
3. 系统会检索知识库并返回相关答案

---

## 📡 API 接口说明

### 1. 查询问答
**POST** `/api/query`

请求体：
```json
{
  "query": "公司办公时间是什么时候？"
}
```

响应：
```json
{
  "answer": "根据知识库内容，为您解答如下：\n\n- 公司办公时间为周一至周五，早上9点到下午6点。\n\n如果您还有其他问题，请随时提问。",
  "sources": ["公司办公时间为周一至周五，早上9点到下午6点。"]
}
```

### 2. 添加文档
**POST** `/api/add_documents`

请求体：
```json
{
  "texts": ["第一条知识", "第二条知识", "第三条知识"]
}
```

响应：
```json
{
  "success": true,
  "message": "成功添加 3 条文档"
}
```

### 3. 清空知识库
**DELETE** `/api/clear_knowledge`

响应：
```json
{
  "success": true,
  "message": "知识库已清空"
}
```

### 4. 健康检查
**GET** `/api/health`

响应：
```json
{
  "status": "healthy"
}
```

---

## 🧠 RAG 工作原理

### 核心流程

```
用户提问 → 文本向量化 → 向量检索 → 上下文构建 → 生成回答
```

### 详细步骤

1. **文本向量化**：使用 `sentence-transformers` 模型将用户问题转为 384 维向量
2. **向量检索**：在向量数据库中搜索与问题向量最相似的知识库向量
3. **上下文构建**：将检索到的相关知识片段拼接成上下文
4. **生成回答**：根据上下文生成自然语言回答

### 为什么需要向量数据库？

| 传统数据库 | 向量数据库 |
|------------|------------|
| 基于关键词匹配 | 基于语义相似度 |
| "办公时间" 只能匹配 "办公时间" | "几点上班" 能匹配 "办公时间为早9点" |
| 无法理解语义 | 理解语义相似性 |

---

## ⚙️ 配置说明

配置文件 `.env` 详解：

| 配置项 | 值 | 说明 |
|--------|-----|------|
| `VECTOR_DB_TYPE` | `faiss` 或 `milvus` | 选择向量数据库类型 |
| `MILVUS_HOST` | `localhost` | Milvus 服务地址 |
| `MILVUS_PORT` | `19530` | Milvus 服务端口 |
| `FAISS_INDEX_PATH` | `./data/faiss_index` | FAISS 索引文件存储路径 |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | 向量化模型名称 |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License