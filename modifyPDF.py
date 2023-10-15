# import
# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import Chroma
# from langchain.document_loaders import TextLoader

# langchain               0.0.150
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings

import os
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# create the open-source embedding function
def read_api_key():
    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

embeddings = OpenAIEmbeddings(openai_api_key=read_api_key())

# Create a Chroma instance and load the database from disk
# db2 = Chroma(collection_name='report', persist_directory="./chromadb_disk_tp", embedding_function=embeddings)
db2 = Chroma(persist_directory="./chromadb_disk_tp", embedding_function=embeddings)

# embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

loader = DirectoryLoader('./New_PDFs/', glob="./*.pdf", loader_cls=PyPDFLoader)

documents = loader.load()

print(len(documents))

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
texts = text_splitter.split_documents(documents=documents)

# TODO: find out what version of chromadb works
db2.add_documents(texts)