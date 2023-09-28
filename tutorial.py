# import
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings

# load the document and split it into chunks
loader = PyPDFLoader("./ignorable/annualreport.pdf")
documents = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

# create the open-source embedding function
# embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
def read_api_key():
    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key
import os
os.environ['OPENAI_API_KEY'] = read_api_key()

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])


# # load it into Chroma
# db = Chroma.from_documents(docs, embeddings)

# save to disk
db = Chroma.from_documents(docs, embeddings, collection_name='report', persist_directory="./chroma_db_temp")


# query it
query = "What is the performance of the company in the last year?"
docs = db.similarity_search(query)

# print results
# print(docs[0].page_content)
for i in docs:
    print(i)