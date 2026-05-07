from langchain_ollama import OllamaLLM

model = OllamaLLM(model="qwen3:32b")

res = model.invoke(input="你是谁？能做什么？")

print(res)