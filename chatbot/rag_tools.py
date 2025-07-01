from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.retrieval_qa.base import RetrievalQA
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from .llm_config import llm

def get_rag_chain():
    pdf_dir = "chatbot/bank_docs"
    all_docs = []

    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            loader = PyPDFLoader("chatbot/bank_docs/bank_info_view.pdf")
            all_docs.extend(loader.load())

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.environ["GOOGLE_API_KEY"])
    db = FAISS.from_documents(all_docs, embeddings)
    retriever = db.as_retriever()

    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
