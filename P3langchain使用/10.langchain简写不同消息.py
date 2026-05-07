from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatTongyi(model="qwen3-max",api_key=os.getenv("ALI_API_KEY"))

messages = [
    ("system","你是一个大四的后端开发工程师，现在已入职某大厂，虽然是大厂但是薪资是大厂里面最差的"),
    ("human","写一首自我调侃的诗"),
    ("ai","《大厂螺丝钉自嘲》工牌挂成狗牌晃，格子间里码农忙。月薪三千五险一，咖啡续命到天光。需求改得亲妈懵，bug修到头发荒。同窗年薪七位数，我领泡面当奖金。"),
    ("human","参照上面的诗，再写一个更惨的"),
]

res = model.stream(input=messages)

for chunk in res:
    print(chunk.content,end="",flush=True)