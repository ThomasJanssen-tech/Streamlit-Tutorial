import os
from dotenv import load_dotenv
import streamlit as st
from pypdf import PdfReader

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate


llm = init_chat_model(
    os.getenv("CHAT_MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=0
)

st.title("Ask questions about a PDF file")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

question = st.text_input(
    "Enter your question about the PDF file:",
    placeholder="What is the main topic of the document?",
    disabled=not uploaded_file)

submit = st.button("Ask now!",
    disabled=not question)

if submit and uploaded_file and question:

    reader = PdfReader(uploaded_file)

    all_text = ""
    for page in reader.pages:
        all_text += page.extract_text()

    prompt = PromptTemplate.from_template("""
    Answer the following question based on the provided text.

    Question:

    <question>
    {question}
    </question>

    Text:
    <text>
    {text}
    </text>
    """)

    executed_prompt = prompt.invoke({"question": question, "text": all_text})
    output = llm.invoke(executed_prompt)

    st.write(f"{output.content}")