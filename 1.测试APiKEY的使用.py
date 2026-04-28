import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-78fa1ce05c7b48d2bc69e7b28baa64f3",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
)

compiletion = client.chat.completions.create(
    model = "qwen-plus",
    messages=[
        {"role":"system","content":"你是一个有用的助手"},
        {"role":"user","content":"请写一个关于机器学习的程序"}
    ],
    stream=True
)

for chunk in compiletion:
    print(chunk.choices[0].delta.content,end="",flush=True)
