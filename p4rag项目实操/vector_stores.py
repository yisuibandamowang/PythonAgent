from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import config_data as config

class VectorStoreService(object):
    def __init__(self,embedding):
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=OllamaEmbeddings(model="qwen3-embedding:8b-fp16"),
            persist_directory=config.persist_directory
        )
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k":config.similarity_threshold})

if __name__ == "__main__":
    from langchain_ollama import OllamaEmbeddings
    embedding = OllamaEmbeddings(model="qwen3-embedding:8b-fp16")
    service = VectorStoreService(embedding=embedding)
    retriever = service.get_retriever()
    res = retriever.invoke("我的身高173，体重67KG，我该选择什么尺码的衣服？")
    print(res)