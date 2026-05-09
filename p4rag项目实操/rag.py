from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaEmbeddings
from vector_stores import VectorStoreService
import config_data as config
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatTongyi
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ALI_API_KEY")

def print_prompt(inputs):
    print("=" * 20 ,inputs.to_string() ,"=" * 20)
    return inputs

class RagService(object):
    def __init__(self):
        self.vector_store = VectorStoreService(
            embedding=OllamaEmbeddings(model=config.embedding_model_name)
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的参考资料为主，使用简洁专业的语言回答用户的问题。参考资料{context}"),
                ("user","请回答用户提问{input}")
            ]
        )
        self.chat_model = ChatTongyi(model="qwen3-max",api_key=api_key)
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_store.get_retriever()

        def format_document(docs):
            if not docs:
                return ""
            format_str = ""
            for doc in docs:
                format_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}"
            return format_str

        chain = (
                {
                    "input": RunnablePassthrough(),
                    "context": retriever | format_document
                } | self.prompt_template | print_prompt | self.chat_model | StrOutputParser())

        return chain

if __name__ == "__main__":
    service = RagService()
    res = service.chain.invoke(input="小王，你妈妈叫什么名字？")
    print(res)