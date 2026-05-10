
md5_path = "./md5.text"

# chroma
collection_name = "rag"
persist_directory = "./chroma_db"

chunk_size = 500
chunk_overlap = 50
separators = ["\n\n", "\n", " ", "",".","!","?","。","！","？"]

max_split_char_num = 500

# 相似度检索的阈值
similarity_threshold = 2     #每次检索返回匹配的文档数量
embedding_model_name = "qwen3-embedding:8b-fp16"

session_config = {
    "configurable":{
        "session_id": "user_001"
    }
}
