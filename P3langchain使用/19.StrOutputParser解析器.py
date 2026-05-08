from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ALI_API_KEY")

parser = StrOutputParser()
model = ChatTongyi(model="qwen3-max",api_key=api_key)
prompt = PromptTemplate.from_template(
    "请帮我写一篇关于{topic}的文章"
)

chain = prompt | model | parser | model

res = chain.invoke({"topic":"机器学习"})
print(res.content)