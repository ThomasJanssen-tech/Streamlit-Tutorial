import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from languages import *

from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate


llm = init_chat_model(
    os.getenv("CHAT_MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=0
)


prompt = PromptTemplate.from_template(
    """You are a translator. Translate the following text to {target_language}: {source_text}
    
    Do not add any extra information or explanation. Just provide the translation."""
)

st.title("Language Translator")

source_text = st.text_area("Enter the text to be translated:")

target_language = st.selectbox("Target language", languages)

translate = st.button("Translate now!")

if translate:

    executed_prompt = prompt.invoke({"target_language": target_language, "source_text": source_text})

    output = llm.invoke(executed_prompt)

    st.write(f"{output.content}")