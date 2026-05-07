from openai import OpenAI, api_key
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ALI_API_KEY")
print(api_key)
client = OpenAI(
    api_key=api_key,
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

compiletion = client.chat.completions.create(
    model = "qwen3-max",
    messages=[
        {"role":"system","content":"你是一个有用的助手"},
        {"role":"user","content":"你是谁"}
    ],
    stream=True
)

for chunk in compiletion:
    print(chunk.choices[0].delta.content,end="",flush=True)
