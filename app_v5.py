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

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 1000,
    chunk_overlap  = 200,
    # length_function = len,
    # is_separator_regex = False,
)

def savePDFtoDisk():
        # Create instance of OpenAI LLM
    llm = OpenAI(temperature=0.1, verbose=True)
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

    # Create an empty list to store the PDF file names
    pdf_files = []
    source_directory = './Source_PDF'
    # Get the pdf name
    for filename in os.listdir(source_directory):
        if filename.endswith('.pdf'):
            # If it's a PDF file, add its name to the list
            pdf_files.append(filename)
    
    all_pages = []

    print("all_pages", all_pages)

    for pdf_file in pdf_files:
        # Create and load PDF Loader
        loader = PyPDFLoader(os.path.join(source_directory, pdf_file))
        # Split pages from pdf 
        # pages = loader.load_and_split()
        pages = loader.load_and_split(text_splitter=text_splitter)


        all_pages.extend(pages)

def chatbot():
    # # Load documents into vector database aka ChromaDB
    persist_directory = './chromadb_disk_tp'
    # store = Chroma.from_documents(all_pages, embeddings,  persist_directory=persist_directory)

    # store.persist()
    # store = None

    # Now we can load the persisted database from disk, and use it as normal. 
    store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    # qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=vectordb)

    # # Save Chromadb locally
    # persist_directory = 'chroma_database.db'
    # store.save_to_file(chromadb_filename)

    # # Load Chromadb from local drive
    # store = Chroma.from_file(chromadb_filename)


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

    return agent_executor, store

# -----------------------------------------------------------

# Define the "Define PDF Paths" page
def define_pdf_paths():
    st.header("Define PDF Paths")
    
    # Create a list to store relative PDF paths
    pdf_paths = []

    # Allow users to upload PDF files using a file picker
    pdf_files = st.file_uploader("Upload PDF Files (multiple allowed)", type=["pdf"], accept_multiple_files=True)

    # Handle uploaded PDF files
    if pdf_files:
        with tempfile.TemporaryDirectory() as tmpdir:
            for pdf_file in pdf_files:
                # Save the uploaded file to the temporary directory
                file_path = os.path.join(tmpdir, pdf_file.name)
                with open(file_path, "wb") as f:
                    f.write(pdf_file.read())

                # Calculate and store the relative path
                relative_path = os.path.relpath(file_path, tmpdir)
                pdf_paths.append(relative_path)

    # Display the list of relative PDF paths
    st.subheader("List of PDF Paths:")
    for path in pdf_paths:
        st.write(path)

    # You can use these relative PDF paths for further processing

# Define the "Perform Q&A" page
def perform_qa(pdf_paths):
    st.header("Perform Q&A")
    
    # # Allow users to select a PDF file for Q&A
    # selected_relative_path = st.selectbox("Select a PDF file for Q&A", pdf_paths)

    # # Get the full path from the relative path
    # selected_pdf_path = os.path.join(tempfile.gettempdir(), selected_relative_path)

    # # Use the PyPDFLoader to load the PDF document
    # pdf_loader = PyPDFLoader(selected_pdf_path)
    # pdf_text = pdf_loader.extract_text()

    # Perform Q&A logic here with the extracted text
    # You can use your Q&A logic with the text from the PDF
    
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

    # Create a Chroma instance and load the database from disk
    db2 = Chroma(collection_name='report', persist_directory="./chroma_db_temp2", embedding_function=embeddings)

    # Define your query
    query = "What is the performance of the company in the last year?"

    # Perform a similarity search
    docs = db2.similarity_search(query)

    # Print the results
    # for doc in docs:
    #     print(doc.page_content)  # Access the content of each matching document


    if st.button("Start Q&A"):
        agent_executor, store = chatbot()
        # Create a text input box for the user
        prompt = st.text_input('Input your question here 👇')
        # Then pass the prompt to the LLM
        response = agent_executor.run(prompt)
        # ...and write it out to the screen
        st.write(response)
        # if docs:
        #     st.success(f"Q&A completed.")
        #     for doc in docs:
        #         st.write(doc.page_content) 
            
        # else:
        #     st.error("Please select a PDF file for Q&A.")

# Define the main function
def main():
    st.title("Langchain App")

    # Create a sidebar for navigation
    page = st.sidebar.selectbox("Select a Page", ["Define PDF Paths", "Perform Q&A"])

    # Initialize PDF relative paths list
    pdf_relative_paths = []

    # Display the selected page content
    if page == "Define PDF Paths":
        define_pdf_paths()
    elif page == "Perform Q&A":
        perform_qa(pdf_relative_paths)

if __name__ == "__main__":
    main()
