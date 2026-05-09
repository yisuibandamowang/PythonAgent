from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma


load_dotenv()
ali_api_key = os.getenv("ALI_API_KEY")

vector_store = Chroma(
    collection_name="test",
    embedding_function=DashScopeEmbeddings(dashscope_api_key=ali_api_key),
    persist_directory="./chromadb"
)

loader = CSVLoader(
    file_path="./data/stu.csv",
    encoding="utf-8",
)

documents = loader.load()

vector_store.add_documents(
    documents=documents,
    ids=["id" + str(i) for i in range(1,len(documents) + 1)]
)

#删除
vector_store.delete(ids=["id1","id2"])

#检索
result = vector_store.similarity_search(query="浩",k=2,filter={"":""})

print(result)
