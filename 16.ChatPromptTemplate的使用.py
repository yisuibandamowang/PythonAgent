import os

from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from dotenv import load_dotenv
import os

load_dotenv()
ali_api_key = os.getenv("ALI_API_KEY")

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个边塞诗人，可以作诗"),
        MessagesPlaceholder("history"),
        ("human","请再来一首唐诗"),
    ]
)

hisroty = [
    {"role":"system","content":"你是一个边塞诗人，可以作诗"},
    {"role":"user","content":"请来一首唐诗"},
    {"role":"assistant","content":"唐诗：白日依山尽，黄河入海流。"},
    {"role":"user","content":"请来一首唐诗"},
    {"role":"assistant","content":"唐诗：白日依山尽，黄河入海流。"},
]

prompt_text = chat_template.invoke({"history":hisroty})

model = Tongyi(model="qwen-max",api_key=ali_api_key)

res = model.invoke(prompt_text)

print(res)