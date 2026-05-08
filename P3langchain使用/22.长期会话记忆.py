import os,json
from typing import Sequence

from dotenv import load_dotenv
from langchain_core.messages import messages_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()
api_key = os.getenv("ALI_API_KEY")

class FileChatMessageHistory(BaseChatMessageHistory):
    #
    def __init__(self, session_id, storage_path):
        self.session_id = session_id        # 会话id
        self.storage_path = storage_path    # 不同会话id所在的不同文件夹路径
        # 完整的文件路径（加 .json 后缀便于识别）
        self.file_path = os.path.join(self.storage_path, f"{self.session_id}.json")

        # 确保文件夹存在
        os.makedirs(self.storage_path, exist_ok=True)

    # 注意：父类抽象方法名是 add_messages（复数），写错名字框架就不会调用你的实现
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)      # 新的和已有的融合成一个

        # messages_to_dict 接受的是"消息列表"，直接整体转换，不要对每条消息单独调用
        new_messages = messages_to_dict(all_messages)

        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f, ensure_ascii=False, indent=2)

    @property         # 该注解将方法变为成员属性
    def messages(self) -> list[BaseMessage]:
        # 文件内是 list[dict]，需用 messages_from_dict 还原成 BaseMessage 列表
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_dict = json.load(f)
                return messages_from_dict(messages_dict)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f)




load_dotenv()
api_key = os.getenv("ALI_API_KEY")
model = ChatTongyi(model="qwen3-max",api_key=api_key)

prompt = PromptTemplate.from_template(
    "你需要根据会话历史回应用户问题。对话历史：{chat_history},用户问题：{user_question}，请根据会话历史回答用户问题"
)

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

def print_prompt(inputs):
    print("=" * 20 ,inputs.to_string() ,"=" * 20)
    return inputs

base_chain = prompt | print_prompt | model | str_parser


def getHistory(session_id):
    return FileChatMessageHistory(session_id,"./history")

# 创建一个新的 chain 增强原始 chain
conversation_chain = RunnableWithMessageHistory(
    base_chain, #被增强的原有链
    getHistory, # 通过会话id获取历史数据
    input_messages_key="user_question", #用户输入在模版中的占位符
    history_messages_key="chat_history", #历史数据在模版中的占位符
)

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id": "user_001"
        }
    }
    res = conversation_chain.invoke(input={"user_question": "小明有1只狗"}, config=session_config)
    print(res)

    res = conversation_chain.invoke(input={"user_question": "小刚有4只猫"}, config=session_config)
    print(res)

    # res = conversation_chain.invoke(input={"user_question": "总共有几只宠物？"}, config=session_config)
    # print(res)

