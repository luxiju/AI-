docker run -d \
  --name milvus-standalone \
  --restart=always \
  -p 19530:19530 \
  -p 9091:9091 \
  -v ~/milvus/data:/var/lib/milvus/data \
  -v ~/milvus/logs:/var/lib/milvus/logs \
  -v ~/milvus/config:/var/lib/milvus/config \
  milvusdb/milvus:v2.4.4 \
  milvus run standalone
