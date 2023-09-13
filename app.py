# SCRAPING
import os
import git
import shutil

# CONVERTING TO VECTOR
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 

# MODEL
from langchain.llms import CTransformers
from langchain.chains import LLMChain, RetrievalQA
from langchain import PromptTemplate
import streamlit as st 
import json
from fastapi import FastAPI, Form, Request, Response, File, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from typing import Dict
import uvicorn


def clone_and_convert_to_text(repo_url, repo_dir, output_dir):
    # Remove the existing directory if it exists
    # if os.path.exists(repo_dir):
    #     shutil.rmtree(repo_dir)

    # Clone the repository to the local directory
    repo = git.Repo.clone_from(repo_url, repo_dir)

    # Create the output directory for text files if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        # Delete existing text files in the output directory
        for file_name in os.listdir(output_dir):
            if file_name.endswith('.txt'):
                file_path = os.path.join(output_dir, file_name)
                os.remove(file_path)

    # Walk through the local repository directory, read the content of each file,
    # and save it as a text file in the output directory
    for root, _, files in os.walk(repo_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Check if the file is a binary file (e.g., images, binaries) and skip it
            if os.path.isfile(file_path) and not file_name.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()

                # Save the content as a text file in the output directory with the same name
                txt_file_path = os.path.join(output_dir, file_name + ".txt")
                with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(content)

    # Clean up by removing the cloned repository
    # shutil.rmtree(repo_dir)

def create_vector_db(data_path, db_faiss_path):
    loader = DirectoryLoader(data_path, glob='*.txt')

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='microsoft/unixcoder-base', model_kwargs={'device': 'cpu'})

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(db_faiss_path)


    # <------------------------------------------------MODEL------------------------------------------------>

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

DB_FAISS_PATH = 'vectorstore/db_faiss'

custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt

#Loading the model
def load_llm():
    llm = CTransformers(
        model = "stablecode-instruct-alpha-3b.ggmlv1.q5_1.bin",
        model_type="gpt_neox",
        max_new_tokens = 512,
        temperature = 0.7
    )
    return llm

#Retrieval QA Chain
def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt}
                                       )
    return qa_chain

def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name='microsoft/unixcoder-base',
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)

    return qa

#output function
def final_result(query):
    qa_result = qa_bot()
    response = qa_result({'query': query})
    return response

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_response")
async def get_response(request: Request, query: str = Form(...)):
    resp = final_result(query)    
    result = resp['result']
    print(resp)
    for i in resp['source_documents'][0]:
        if 'metadata' in i:
            source_doc = i[1]['source']
    # print(resp['source_documents'][0]['metadata']['source'])
    response_data = jsonable_encoder(json.dumps({"result": result, "source_doc": source_doc}))
    res = Response(response_data)
    return res

    # <------------------------------------------------MAIN------------------------------------------------>


if __name__ == "__main__":
    repo_url = "https://github.com/HarishVijayV/Tic-Tac-Toe_jack"
    repo_dir = "cloned_repo"
    output_dir = "data"

    DATA_PATH = 'data/'
    DB_FAISS_PATH = 'vectorstore/db_faiss'

    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    clone_and_convert_to_text(repo_url, repo_dir, output_dir)
    print("Done with cloning!")

    create_vector_db(DATA_PATH, DB_FAISS_PATH)
    print("Done with creating the vector database!")

    # uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)