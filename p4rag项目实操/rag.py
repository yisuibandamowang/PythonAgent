from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_ollama import OllamaEmbeddings
from streamlit import session_state

from vector_stores import VectorStoreService
import config_data as config
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from dotenv import load_dotenv
import os
from file_history_store import getHistory

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
                ("system","并且我提供用户的历史会话记录如下"),
                MessagesPlaceholder("history"),
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

        def format_for_retriever(inputs):
            return inputs["input"]

        def format_for_prompt(inputs):
            new_value = {}
            new_value["input"] = inputs["input"]["input"]
            new_value["history"] = inputs["input"]["history"]
            new_value["context"] = inputs["context"]
            return new_value

        chain = (
                {
                    "input": RunnablePassthrough(),
                    "context": RunnableLambda(format_for_retriever) | retriever | format_document
                } | RunnableLambda(format_for_prompt) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser())

        conversation_chain = RunnableWithMessageHistory(
            chain,
            getHistory,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain

if __name__ == "__main__":
    # session_id 配置
    session_config = {
        "configurable":{
            "session_id": "user_001"
        }
    }
    service = RagService()
    res = service.chain.invoke({"input": "小王，你妈妈叫什么名字？"},session_config)
    print(res)