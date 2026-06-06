# 智能客服RAG系统

基于 RAG（Retrieval-Augmented Generation）技术的本地智能客服系统，支持 FAISS 和 Milvus 两种向量数据库检索方式，并集成大语言模型（LLM）进行回答生成。

## 📁 项目结构

```
RAG/
├── main.py                 # FastAPI 后端服务入口
├── config.py               # 配置文件（向量数据库类型、路径等）
├── embedding.py            # 文本向量化模型封装（支持千问嵌入模型）
├── llm_client.py           # 大语言模型客户端（支持千问 LLM）
├── rag_service.py          # RAG 核心服务逻辑
├── init_knowledge.py       # 知识库初始化脚本
├── requirements.txt        # Python 依赖清单
├── .env                    # 环境变量配置
├── .env.example            # 环境变量配置示例（不含敏感信息）
├── .gitignore              # Git 忽略文件配置
├── vue.js                  # Vue.js 框架库
├── data/
│   ├── sample_knowledge.txt    # 示例知识库数据
│   └── faiss_index/            # FAISS 索引文件存储目录
├── vector_db/
│   ├── __init__.py             # 向量数据库工厂函数
│   ├── base.py                 # 向量数据库抽象基类
│   ├── faiss_db.py             # FAISS 实现
│   └── milvus_db.py            # Milvus 实现
└── templates/
    ├── index.html              # 原生 HTML 版前端聊天界面
    └── index-vue.html          # Vue 版前端聊天界面
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

**产出**：安装了所有必要的 Python 库（FastAPI、FAISS、pymilvus、sentence-transformers、openai 等）。

**意义**：
- `fastapi` + `uvicorn`：构建和运行 Web 服务
- `faiss-cpu`：轻量级本地向量数据库
- `pymilvus`：Milvus 向量数据库客户端
- `sentence-transformers`：文本向量化模型
- `openai`：调用大语言模型 API
- `requests`：HTTP 请求库

---

## 🔧 步骤 3：配置环境变量

复制并修改 `.env` 文件：

```bash
# 复制示例配置
cp .env.example .env

# 编辑配置文件（填入你的 API Key）
```

**配置项说明**：

| 配置项 | 值 | 说明 |
|--------|-----|------|
| `VECTOR_DB_TYPE` | `faiss` 或 `milvus` | 选择向量数据库类型 |
| `MILVUS_HOST` | `localhost` | Milvus 服务地址 |
| `MILVUS_PORT` | `19530` | Milvus 服务端口 |
| `FAISS_INDEX_PATH` | `./data/faiss_index` | FAISS 索引文件存储路径 |
| `EMBEDDING_MODEL` | `Qwen/Qwen3-Embedding-8B` | 向量化模型（千问嵌入模型） |
| `EMBEDDING_BASE_URL` | `https://api-inference.modelscope.cn/v1` | 嵌入模型 API 地址 |
| `EMBEDDING_API_KEY` | `your-api-key` | ModelScope API Key |
| `LLM_MODEL` | `Qwen/Qwen3-32B` | 大语言模型（千问 32B） |
| `LLM_BASE_URL` | `https://api-inference.modelscope.cn/v1` | LLM API 地址 |
| `LLM_API_KEY` | `your-api-key` | ModelScope API Key |
| `MAX_RESULTS` | `5` | 向量检索返回结果数量 |

**⚠️ 重要**：`.env` 文件包含敏感信息（API Key），**不要上传到 Git**！`.gitignore` 已配置排除该文件。

---

## 🔧 步骤 4：配置向量数据库

### 方式 A：使用 FAISS（默认，推荐本地开发）

无需额外配置，系统默认使用 FAISS。

**产出**：向量数据存储在本地文件系统，无需额外服务。

**适用场景**：单机开发、轻量级应用、演示环境。

### 方式 B：使用 Milvus（需要 Docker）

**修改配置文件** `.env`：
```env
VECTOR_DB_TYPE=milvus
```

**启动 Milvus 服务**（需要 Docker 已安装）：

```bash
# 方式 1：使用 docker-compose（推荐）
cd ~/milvus
wget https://github.com/milvus-io/milvus/releases/download/v2.4.4/milvus-standalone-docker-compose.yml -O docker-compose.yml
docker-compose up -d

# 方式 2：使用单容器（需要内嵌 etcd）
docker run -d \
  --name milvus-standalone \
  -p 19530:19530 \
  -p 9091:9091 \
  -v ~/milvus/data:/var/lib/milvus/data \
  -e ETCD_USE_EMBED=true \
  milvusdb/milvus:v2.4.4 standalone
```

**验证 Milvus 连接**：
```bash
python -c "from pymilvus import connections; connections.connect(); print('Milvus 连接成功')"
```

**产出**：启动了 Milvus 向量数据库服务，监听在 `localhost:19530`。

**适用场景**：大规模数据、生产环境、需要高可用和分布式部署。

---

## 🔧 步骤 5：初始化知识库

```bash
python init_knowledge.py
```

**预期输出**：
```
成功加载 10 条知识库文档
```

**产出**：
1. 将 `data/sample_knowledge.txt` 中的文本转换为向量（4096 维）
2. 向量存储到向量数据库（FAISS 或 Milvus）

**意义**：
- 文本向量化：将人类语言转为计算机可理解的向量
- 索引构建：建立向量索引，支持快速相似性搜索

---

## 🔧 步骤 6：启动服务

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

---

## 🔧 步骤 7：访问前端界面

### 版本选择

| 版本 | 地址 | 说明 |
|------|------|------|
| **原生 HTML 版** | `http://localhost:8000/` | 纯 JavaScript 实现 |
| **Vue 版** | `http://localhost:8000/vue` | Vue.js 响应式实现 |

### 界面功能

1. **状态显示**：显示服务状态和当前使用的向量数据库类型
2. **标签页切换**（Vue 版）：对话模式 / 知识库管理模式
3. **知识库管理**：可添加新的知识库文档（每行一条）
4. **聊天界面**：与智能客服对话，支持显示参考来源

### 使用流程

1. 在"添加知识库文档"区域输入知识内容，点击"添加文档"
2. 在底部输入框输入问题，点击"发送"或按 Enter
3. 系统会检索知识库并使用 LLM 生成自然语言回答

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
  "answer": "公司的办公时间是周一至周五，早上9点到下午6点。",
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
  "status": "healthy",
  "vector_db_type": "faiss"
}
```

---

## 🧠 RAG 工作原理

### 核心流程

```
用户提问 → 文本向量化 → 向量检索 → 上下文构建 → LLM 生成回答
```

### 详细步骤

1. **文本向量化**：使用 `Qwen/Qwen3-Embedding-8B` 模型将用户问题转为 4096 维向量
2. **向量检索**：在向量数据库中搜索与问题向量最相似的知识库向量（返回 top 5）
3. **上下文构建**：将检索到的相关知识片段拼接成提示词上下文
4. **LLM 生成**：调用 `Qwen/Qwen3-32B` 模型根据上下文生成自然语言回答

### 为什么需要向量数据库？

| 传统数据库 | 向量数据库 |
|------------|------------|
| 基于关键词匹配 | 基于语义相似度 |
| "办公时间" 只能匹配 "办公时间" | "几点上班" 能匹配 "办公时间为早9点" |
| 无法理解语义 | 理解语义相似性 |

### 为什么需要 LLM？

| 无 LLM | 有 LLM |
|--------|--------|
| 简单拼接检索结果 | 自然语言总结回答 |
| 格式固定、生硬 | 回答流畅、自然 |
| 无法理解上下文 | 可以总结归纳知识 |

---

## ⚙️ 配置说明

### 完整配置项

```env
# 向量数据库配置
VECTOR_DB_TYPE=faiss
MILVUS_HOST=localhost
MILVUS_PORT=19530
FAISS_INDEX_PATH=./data/faiss_index

# 嵌入模型配置
EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
EMBEDDING_BASE_URL=https://api-inference.modelscope.cn/v1
EMBEDDING_API_KEY=your-api-key

# 大语言模型配置
LLM_MODEL=Qwen/Qwen3-32B
LLM_BASE_URL=https://api-inference.modelscope.cn/v1
LLM_API_KEY=your-api-key

# 其他配置
DATA_DIR=./data
MAX_RESULTS=5
```

### 模型选择建议

| 模型 | 类型 | 维度 | 说明 |
|------|------|------|------|
| `Qwen/Qwen3-Embedding-8B` | 嵌入模型 | 4096 | 高精度，适合精确检索 |
| `all-MiniLM-L6-v2` | 嵌入模型 | 384 | 轻量级，适合快速检索 |
| `Qwen/Qwen3-32B` | LLM | - | 大模型，效果好但响应较慢 |
| `Qwen/Qwen2-7B-Chat` | LLM | - | 较小模型，响应较快 |

---

## 📊 技术栈对比

| 特性 | FAISS | Milvus |
|------|-------|--------|
| **部署方式** | 嵌入式（无需独立服务） | 需要独立服务（Docker/K8s） |
| **适用场景** | 单机、轻量应用 | 分布式、大规模数据 |
| **持久化** | 文件存储 | 专业数据库 |
| **GPU 加速** | 支持 | 支持 |
| **默认配置** | ✅ | ⏳ 需额外配置 |

---

## 🚫 Git 忽略文件

`.gitignore` 已配置排除以下文件：

| 文件/目录 | 说明 |
|-----------|------|
| `.env` | 环境变量（含敏感信息） |
| `*.pyc`, `__pycache__` | Python 编译文件 |
| `data/faiss_index/` | FAISS 索引文件 |
| `volumes/` | Milvus 持久化数据 |
| `.cache/` | 模型缓存 |
| `*.log` | 日志文件 |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License