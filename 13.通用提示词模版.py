from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
tongyi_api_key = os.getenv("ALI_API_KEY")

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},你帮我起个名字，简单回答"
)

# prompt_text = prompt_template.format(lastname="陈", gender="儿子")
#
model = Tongyi(model="qwen-max",api_key=tongyi_api_key)


# res = model.invoke(input=prompt_text)
# print(res)


chain = prompt_template | model

res = chain.invoke(input={"lastname":"陈","gender":"儿子"})
print(res)