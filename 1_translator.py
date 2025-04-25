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

st.title("Translator Application")

source_text = st.text_area(
    "Enter the text you want to translate:",
    placeholder="Type your text here...",
    height=200
)

target_language = st.selectbox(
    "Select the target language:",
    languages
)

button = st.button("Translate",
    disabled=not source_text or not target_language
)

if button:

    prompt = PromptTemplate.from_template("""
    Translate the following text to {target_language}.:
    
    <text>
    {text}
    </text>
                                          
    Only proviude the translated text without any additional information.
    """)

    executed_prompt = prompt.invoke({"target_language": target_language, "text": source_text})
    output = llm.invoke(executed_prompt)

    st.write(f"Translated text: {output.content}")