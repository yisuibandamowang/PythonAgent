from langchain_ollama import OllamaLLM

model = OllamaLLM(model="qwen3:32b")

res = model.stream(input="你是谁？能做什么？")

for chunk in res:
    print(chunk,end="",flush=True)