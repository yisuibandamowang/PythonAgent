import os
import sys

# 将项目所在的父目录加入 sys.path，使得 `p6agent智能体_rag项目` 这个包可以被正常导入
# （项目内部多处使用了 from p6agent智能体_rag项目.xxx import ... 的绝对导入写法）
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_CURRENT_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)

import streamlit as st
from p6agent智能体_rag项目.agent.react_agent import ReactAgent

st.title("智能扫地机器人客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for messages in st.session_state["messages"]:
    st.chat_message(messages["role"]).write(messages["content"])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role":"user","content":prompt})

    response_messages = []

    with st.spinner("思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture_stream(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture_stream(res_stream,response_messages))

        st.session_state["messages"].append({"role":"assistant","content":response_messages[-1]})
        #刷新页面 用于模型回答之后在页面上隐藏思考过程 参考其他网页助手
        st.rerun()