from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("ALI_API_KEY")

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatTongyi(model="qwen3-max",api_key=api_key)

#第一个提示词模版
first_prompt = PromptTemplate.from_template(
    "我邻居{lastname}，最喜欢{hobby}，刚生了{gender}，请帮我起名字，仅需要回复名字，无需额外内容,"
    "并封装为json格式，要求key是name，value就是你起的名字，请严格遵守格式"
)

second_prompt = PromptTemplate.from_template(
    "名字是{name},请帮我解析这名字的含义"
)

# 函数的入参：AiMessage -> dict ({"name":"xxx"})
my_func = RunnableLambda(lambda ai_msg: {"name":ai_msg.content})

# 构建chain
chain = first_prompt | model | my_func | second_prompt | model | str_parser

res = chain.invoke({"lastname":"刘","hobby":"唱歌","gender":"男孩"})
print(res)