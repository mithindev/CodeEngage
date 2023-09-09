from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def create_vector_db(data_path, db_faiss_path):
    loader = DirectoryLoader(data_path, glob='*.txt')

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='microsoft/unixcoder-base', model_kwargs={'device': 'cpu'})

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(db_faiss_path)

if __name__ == "__main__":
    DATA_PATH = 'data/'  # Replace with your desired data path
    DB_FAISS_PATH = 'vectorstore/db_faiss'  # Replace with your desired DB Faiss path
    create_vector_db(DATA_PATH, DB_FAISS_PATH)
