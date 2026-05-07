from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
ali_api_key = os.getenv("ALI_API_KEY")

model = DashScopeEmbeddings(dashscope_api_key=ali_api_key)
embed_query = model.embed_query("我喜欢你")
print(embed_query)