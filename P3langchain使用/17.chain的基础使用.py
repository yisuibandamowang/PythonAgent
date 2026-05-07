from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ALI_API_KEY")

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人，可以作诗"),
        MessagesPlaceholder("history"),
        ("human", "请再来一首唐诗"),
    ]
)

history_data = [
    ("human", "你是一个边塞诗人，可以作诗"),
    ("ai", "白日依山尽，黄河入海流。\n欲穷千里目，更上一层楼。"),
    ("human", "好诗，请再来一首"),
    ("ai", "西风瘦马，客输西风。")
]

model = ChatTongyi(model="qwen3-max", api_key=api_key)

# 组成链: 每一个接口都是runnable接口的子类
chain = chat_prompt_template | model

# 通过链去调用invoke 或 stream
res = chain.invoke({"history": history_data})
print(res.content)

# 通过 stream 流失输出
chain.stream({"history": history_data})

for chunk in chain.stream({"history": history_data}):
    print(chunk.content,end="",flush=True)

