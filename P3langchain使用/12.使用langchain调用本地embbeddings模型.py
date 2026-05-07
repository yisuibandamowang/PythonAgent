from langchain_ollama import OllamaEmbeddings

model = OllamaEmbeddings(model="qwen3-embedding:8b-fp16")

res = model.embed_query("你好")
print(res)

