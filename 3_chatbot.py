import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = init_chat_model(
    os.getenv("CHAT_MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=0.5
)

st.title("🤖 Astronaut Chatbot")


if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content="You are an astronaut. Act like an astronaut."
        )
    ]

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

prompt = st.chat_input("Ask me anything about the universe!")

if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)

        st.session_state.messages.append(HumanMessage(content=prompt))

    with st.chat_message("assistant"):

        output = llm.invoke(st.session_state.messages)

        st.markdown(output.content)
        st.session_state.messages.append(AIMessage(content=output.content))
