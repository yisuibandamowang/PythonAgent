from langchain_community.chat_models import ChatTongyi
from dotenv import load_dotenv
import os

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore

load_dotenv()
api_key = os.getenv("ALI_API_KEY")

model = ChatTongyi(model="qwen3-max",api_key=api_key)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的资料作为参考，使用简洁专业的回答来回答用户提问，参考资料：{context}"),
        ("user", "用户提问{question}"),
    ]
)

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(dashscope_api_key=api_key),
)

vector_store.add_texts(
    ["减肥需要少吃多动","在减脂期间吃东西很重要，清淡少油控制卡路里摄入并运动起来","跑步是一个很好的运动"]
)

input_text = "怎么减肥?"

#langchain 中 使用 as_retriever 创建一个向量搜索器  可以返回一个 Runnable 接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

def format_func(inputs: list[Document]):
    if not inputs:
        return "无相关参考资料"
    format_str = "["
    for doc in inputs:
        format_str += doc.page_content
    format_str += "]"
    return format_str
#chain
chain = ({"question":RunnablePassthrough(),"context": retriever | format_func} | prompt | model | StrOutputParser())

res = chain.invoke(input_text)
print(res)

