import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = 'sk-proj-PZpvaGFYWawlD2XEUxjET3BlbkFJPGllPygNyNox23rDon0e'

# Streamlit app interface
st.title("PDF QA Chatbot")
st.write("Upload a PDF file and ask questions about its content.")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    # Read data from the file and put it into a variable called pdf_text
    reader = PdfReader(uploaded_file)
    pdf_text = ''
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text

    # Define text splitter
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 100000, # thousand characters
        chunk_overlap = 200,
        length_function = len,
    )
    text_chunks = text_splitter.split_text(pdf_text)
    
    # Convert text to embeddings using OpenAI embeddings
    embeddings = OpenAIEmbeddings()
    pdf_embeddings = FAISS.from_texts(text_chunks, embeddings)
    
    # Load QA chain
    chain = load_qa_chain(OpenAI(), chain_type="stuff")
    
    # User input for questions
    query = st.text_input("Ask a question about the PDF content:")
    
    if query:
        # Perform similarity search
        docs = pdf_embeddings.similarity_search(query)
        
        # Get the answer from the QA chain
        answer = chain.run(input_documents=docs, question=query)
        
        # Display the answer
        st.write("Answer:", answer)