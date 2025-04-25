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

st.title("File Question Answering Application")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

question = st.text_area("Ask a question about the file:",disabled=not uploaded_file)

submit = st.button("Submit",
    disabled=not uploaded_file or not question
)

if submit:
    # Read the PDF file
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
   

    prompt = PromptTemplate.from_template("""
    Answer the following question based on the provided text:
    <question>
    {question} 
    </question>

    Document:
    <text>
    {text}
    </text>                  

    """)

    executed_prompt = prompt.invoke({"question": question, "text": text})
    output = llm.invoke(executed_prompt)

    st.write(f"{output.content}")
