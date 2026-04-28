import os
from openai import OpenAI

client = OpenAI(
    api_key="ollama",
    base_url = "http://localhost:11434/v1",
)

compiletion = client.chat.completions.create(
    model = "qwen3:32b",
    messages=[
        {"role":"system","content":"你是一个有用的助手"},
        {"role":"user","content":"请写一个关于机器学习的程序"}
    ],
    stream=True
)

for chunk in compiletion:
    print(chunk.choices[0].delta.content,end="",flush=True)
