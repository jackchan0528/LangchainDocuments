from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings

# create the open-source embedding function
def read_api_key():
    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

embeddings = OpenAIEmbeddings(openai_api_key=read_api_key())

# Create a Chroma instance and load the database from disk
db2 = Chroma(collection_name='report', persist_directory="./chroma_db_temp2", embedding_function=embeddings)

# Define your query
query = "What is the performance of the company in the last year?"

# Perform a similarity search
docs = db2.similarity_search(query)

# Print the results
for doc in docs:
    print(doc.page_content)  # Access the content of each matching document
