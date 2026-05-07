from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
ali_api_key = os.getenv("ALI_API_KEY")

prompt_template = PromptTemplate.from_template("我的邻居是{lastname}，最喜欢{hobby}")

res = prompt_template.format(lastname="小黑",hobby="唱歌")
print(res,type(res))

res = prompt_template.invoke({"lastname":"小黑","hobby":"唱歌"})

print(res,type(res))

