import tempfile

# Import os to set API key
import os
# Import OpenAI as main LLM service
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import TextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Bring in streamlit for UI/app interface
import streamlit as st

# Import PDF document loaders...there's other ones as well!
from langchain.document_loaders import PyPDFLoader
# Import chroma as the vector store 
from langchain.vectorstores import Chroma

# Read from chromadb_disk_tp
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings

from langchain.document_loaders import DirectoryLoader
# -----------------------------------------------------------

# Import vector store stuff
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)

# Set APIkey for OpenAI Service
# Can sub this out for other LLM providers
def read_api_key():
    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

os.environ['OPENAI_API_KEY'] = read_api_key()

# -----------------------------------------------------------

def savePDFtoDisk():
    # Create instance of OpenAI LLM
    llm = OpenAI(temperature=0.1, verbose=True)
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

    loader = DirectoryLoader('./Source_PDF/', glob="./*.pdf", loader_cls=PyPDFLoader)

    documents = loader.load()

    print(len(documents))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    texts = text_splitter.split_documents(documents=documents)

    print(len(texts))
    print(texts[1])
    # texts = loader.load_and_split(text_splitter=text_splitter)

    # # Create an empty list to store the PDF file names
    # pdf_files = []
    # source_directory = './Source_PDF'
    # # Get the pdf name
    # for filename in os.listdir(source_directory):
    #     if filename.endswith('.pdf'):
    #         # If it's a PDF file, add its name to the list
    #         pdf_files.append(filename)
    
    # all_pages = []

    # for pdf_file in pdf_files:
    #     # Create and load PDF Loader
    #     loader = PyPDFLoader(os.path.join(source_directory, pdf_file))
    #     # Split pages from pdf 
    #     # pages = loader.load_and_split()
    #     pages = loader.load_and_split(text_splitter=text_splitter)

    #     all_pages.extend(pages)
    
    
    persist_directory = './chromadb_disk_tp'
    store = Chroma.from_documents(documents=texts, 
                                  embedding=embeddings, 
                                  persist_directory=persist_directory)
    # store = Chroma.from_documents(documents=texts, embedding=embeddings, metadatas=[{"source": s} for s in pdf_files], persist_directory=persist_directory)

    store.persist()
    # store = None

    # # Now we can load the persisted database from disk, and use it as normal. 
    # store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    # # qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=vectordb)

    # # # Save Chromadb locally
    # # persist_directory = 'chroma_database.db'
    # store.save_to_file(persist_directory)


savePDFtoDisk()