import streamlit as st
import time
from rag import RagService
import config_data as config

st.title("智能客服")
st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"有什么可以帮你"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])


prompt = st.chat_input("请输入问题")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    res = st.session_state["rag"].chain.invoke({"input":prompt},config.session_config)
    st.chat_message("assistant").write(res)
    st.session_state["message"].append({"role":"assistant","content":res})
