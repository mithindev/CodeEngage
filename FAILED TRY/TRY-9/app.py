import os
from github import Github
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import CTransformers
from langchain.chains import LLMChain, RetrievalQA
from langchain import PromptTemplate
from typing import Dict
import json
import streamlit as st 
from fastapi import FastAPI, Form, Request, Response, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Define your FastAPI app
app = FastAPI()

# Serve static files (CSS, JavaScript, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory for Jinja2
templates = Jinja2Templates(directory="templates")

# Paths
DATA_PATH = 'data/'
DB_FAISS_PATH = 'vectorstore/db_faiss'

# Define a class for GitHub repository scraping
class GithubRepoScraper:
    def __init__(self, repo_name, github_token=None):
        self.github_token = github_token
        self.repo_name = repo_name

    def fetch_all_files(self):
        github_instance = Github(self.github_token)
        repo = github_instance.get_repo(self.repo_name)
        contents = repo.get_contents("")
        files_data = []

        def recursive_fetch_files(contents):
            for content_file in contents:
                if content_file.type == "dir":
                    recursive_fetch_files(repo.get_contents(content_file.path))
                else:
                    file_content = content_file.decoded_content.decode("utf-8")
                    files_data.append((content_file.path, file_content))

        recursive_fetch_files(contents)
        return files_data

    def write_to_file(self, files_data, output_file):
        with open(output_file, "w", encoding='utf-8') as f:
            for path, content in files_data:
                f.write(f"File: {path}\n")
                f.write(content)
                f.write('\n' + '-' * 50 + '\n')

    def scrape_repository(self, output_file):
        files_data = self.fetch_all_files()
        self.write_to_file(files_data, output_file)

# Function to create a vector database
def create_vector_db(data_path, db_faiss_path):
    loader = DirectoryLoader(data_path, glob='*.txt')

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='microsoft/unixcoder-base', model_kwargs={'device': 'cpu'})

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(db_faiss_path)

# Load a language model (LLM)
def load_llm():
    llm = CTransformers(
        model="stablecode-instruct-alpha-3b.ggmlv1.q5_1.bin",
        model_type="gpt_neox",
        max_new_tokens=512,
        temperature=0.7
    )
    return llm

# Set a custom prompt template for QA
def set_custom_prompt():
    custom_prompt_template = """Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=['context', 'question'])
    return prompt

# Initialize the QA bot
def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name='microsoft/unixcoder-base', model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=db.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True,
        chain_type_kwargs={'prompt': qa_prompt}
    )
    return qa

# Function to get the response from the QA bot
def final_result(query):
    qa_result = qa_bot()
    response = qa_result({'query': query})
    return response

# Define routes and handlers
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_response", response_model=Dict[str, str])
async def get_response(query: str = Form(...)):
    resp = final_result(query)
    result = resp['result']
    source_doc = None
    for i in resp.get('source_documents', []):
        if 'metadata' in i:
            source_doc = i[1]['source']
            break
    return {"result": result, "source_doc": source_doc}

if __name__ == "__main__":
    # Replace with your GitHub repository information
    repo_name = "mithindev/mithindev"
    github_token = "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"
    output_file = "data/repository_contents.txt"
    
    scraper = GithubRepoScraper(repo_name, github_token)
    scraper.scrape_repository(output_file)
    
    create_vector_db(DATA_PATH, DB_FAISS_PATH)
    
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)
