# Import os to set API key
import os
# Import OpenAI as main LLM service
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
# Bring in streamlit for UI/app interface
import streamlit as st

# Import PDF document loaders...there's other ones as well!
from langchain.document_loaders import PyPDFLoader
# Import chroma as the vector store 
from langchain.vectorstores import Chroma

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

# Create instance of OpenAI LLM
llm = OpenAI(temperature=0.1, verbose=True)
embeddings = OpenAIEmbeddings()

# Create an empty list to store the PDF file names
pdf_files = []
source_directory = './Source_PDF'
# Get the pdf name
for filename in os.listdir(source_directory):
    if filename.endswith('.pdf'):
        # If it's a PDF file, add its name to the list
        pdf_files.append(filename)
# Create and load PDF Loader
loader = PyPDFLoader(os.path.join(source_directory, pdf_files[0]))
# Split pages from pdf 
pages = loader.load_and_split()
# Load documents into vector database aka ChromaDB
store = Chroma.from_documents(pages, embeddings, collection_name='report')

# Create vectorstore info object - metadata repo?
vectorstore_info = VectorStoreInfo(
    name="general-pdf-report",
    description="general document as a pdf",
    vectorstore=store
)

# Convert the document store into a langchain toolkit
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

# Add the toolkit to an end-to-end LC
agent_executor = create_vectorstore_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

# st.title('🦜🔗 GPT Investment Banker')
st.title('Talk to your PDF')

# # Ask the user to provide an openai API key
# api_key = st.text_input('Input your OpenAI API Key here 👇',
#                         type='password')

# print(api_key)

# Create a text input box for the user
prompt = st.text_input('Input your question here 👇')

# print(prompt)

# # Allow advanced settings
# with st.expander('Advanced settings'):
#     # Slider for creativity
#     temperature = st.slider('The level of creativity', 0, 1, 0.05)

# f = st.file_uploader("Upload a file", type=(["tsv","csv","txt","tab","xlsx","xls"]))
# if f is not None:
#     path_in = f.name
#     print(path_in)
# else:
#     path_in = None

# If the user hits enter
# if prompt:
if st.button("Ask Me!"):
    # Then pass the prompt to the LLM
    response = agent_executor.run(prompt)
    # ...and write it out to the screen
    st.write(response)

    # With a streamlit expander  
    with st.expander('Document Similarity Search'):
        # Find the relevant pages
        search = store.similarity_search_with_score(prompt) 
        # Write out the first 
        st.write(search[0][0].page_content) 