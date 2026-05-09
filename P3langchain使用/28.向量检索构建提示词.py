from langchain_community.chat_models import ChatTongyi
from dotenv import load_dotenv
import os

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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

result = vector_store.similarity_search(input_text,2)

for i in result:
    print(i.page_content)

def print_prompt(inputs):
    print("=" * 20 ,inputs.to_string() ,"=" * 20)
    return inputs

chain = prompt | print_prompt | model | StrOutputParser()

res = chain.invoke({"question": input_text,"context":result})

print(res)
