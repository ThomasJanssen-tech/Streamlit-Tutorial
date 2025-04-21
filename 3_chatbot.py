import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = init_chat_model(
    os.getenv("CHAT_MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=0.5
)

st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

    st.session_state.messages.append(SystemMessage("Act like an astronaut"))


for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)



prompt = st.chat_input("Ask me anything!")

if prompt:

    with st.chat_message("user"):
        st.write(prompt)

        st.session_state.messages.append(HumanMessage(prompt))


    output = llm.invoke(st.session_state.messages)
    with st.chat_message("assistant"):
        st.write(output.content)

        st.session_state.messages.append(AIMessage(output.content))