import os
from abc import ABC, abstractmethod
from typing import Optional

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_core.embeddings import Embeddings
from p6agent智能体_rag项目.utils.config_handler import rag_conf
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("ALI_API_KEY")

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[BaseChatModel]:
        return ChatTongyi(model=rag_conf["chat_model_name"],api_key=api_key)

class EmbeddingsModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"],dashscope_api_key=api_key)

chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsModelFactory().generator()

