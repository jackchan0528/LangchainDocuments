# langchain               0.0.150
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.llms import OpenAI
import os

# create the open-source embedding function
def read_api_key():
    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

os.environ['OPENAI_API_KEY'] = read_api_key()
# embeddings = OpenAIEmbeddings(openai_api_key=read_api_key())
embeddings = OpenAIEmbeddings()

llm = OpenAI(temperature=0.1, verbose=True)

# Create a Chroma instance and load the database from disk
# db2 = Chroma(collection_name='report', persist_directory="./chromadb_disk_tp", embedding_function=embeddings)
vectorstore = Chroma(persist_directory="./chromadb_disk_tp", embedding_function=embeddings)


# # Define your query
# # query = "What is the performance of the company in the last year?"
# query = "What is the profit of FY2022?"

# # Perform a similarity search
# docs = db2.similarity_search(query)

# # Print the results
# for doc in docs:
#     print(doc.page_content)  # Access the content of each matching document


memory = ConversationSummaryMemory(llm=llm,memory_key="chat_history",return_messages=True)

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

llm = ChatOpenAI()
retriever = vectorstore.as_retriever()
qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

print(qa("What is the profit in FY2022?"))