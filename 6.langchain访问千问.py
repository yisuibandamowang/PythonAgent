from langchain_community.llms.tongyi import Tongyi
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ALI_API_KEY")
print(api_key)

model = Tongyi(model="qwen-max", api_key=api_key)

res = model.invoke(input="你是谁？能做什么？")

print(res)