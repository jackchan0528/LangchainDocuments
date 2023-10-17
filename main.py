import streamlit as st
import os
import shutil
from st_pages import Page, Section, show_pages, add_page_title

# Function to get relative paths of selected PDF files
def get_pdf_paths():
    st.header("PDF File List")
    st.write("Please store all PDFs required in the 'pdfs/' directory:")
    
    pdf_dir = 'pdfs'
    
    if not os.path.exists(pdf_dir):
        st.warning("The 'pdfs' directory does not exist or is empty.")
    else:
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
        if not pdf_files:
            st.warning("No PDF files found in the 'pdfs' directory.")
        else:
            st.subheader("PDF Files:")
            for pdf_file in pdf_files:
                st.write(pdf_file)

    # "Refresh" button to update the list
    if st.button("Refresh"):
        st.experimental_rerun()
    # st.header("PDF File Selector")
    # st.write("Select one or more PDF files to get their relative paths.")
    
    # # File uploader for multiple PDF files
    # uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    
    # if uploaded_files:
    #     st.subheader("Relative Paths of Selected PDF Files:")
    #     for file in uploaded_files:
    #         print(file)
    #         file_name = file.name
    #         # Use os.path.relpath to get the relative path
    #         # relative_path = os.path.relpath(file.name, start=os.getcwd())
    #         # Get the relative path from the current working directory
    #         relative_path = os.path.dirname(file_name)
    #         absolute_path = os.path.abspath(file.name)
    #         st.write(f"File: {file_name}, Absolute Path: {relative_path}")

    #      # "Update Database" button
    #     if st.button("Update Database"):
    #         for file in uploaded_files:
    #             # file_name = file.name
    #             destination_path = os.path.join("pdfs", file_name)
    #             shutil.copy(absolute_path, destination_path)
    #         st.success("PDF files have been copied to the 'pdfs' directory.")

# Function for Q&A with a chatbot using Langchain
def chatbot_qa():
    st.header("Q&A Chatbot")
    st.write("Ask questions and get answers from the chatbot.")
    
    # Input question
    question = st.text_input("Ask a question:")
    
    # if question:
    #     # Assuming you have a Langchain instance named 'langchain' for Q&A
    #     answer = langchain.answer_question(question)
    #     st.write("Answer:", answer)

# Main app
def main():
    add_page_title() # By default this also adds indentation

    # Specify what pages should be shown in the sidebar, and what their titles and icons
    # should be
    show_pages(
        [
            Page("home.py", "Home", "🏠"),
            Page("showPDF.py", "Show PDF List", "🔎"),
            Page("savePDF.py", "Save PDF", "💾"),
            Page("qnaPDF.py", "PDF Q&A", "🤖"),
            # Section("My section", icon="🎈️"),
            # # Pages after a section will be indented
            # Page("Another page", icon="💪"),
            # # Unless you explicitly say in_section=False
            # Page("Not in a section", in_section=False)
        ]
    )

    # st.title("PDF File List & Chatbot Q&A")
    
    # # Create tabs on the left-hand side
    # app_mode = st.sidebar.radio("Choose an App Mode", ["PDF File Selector", "Q&A Chatbot"])
    
    # if app_mode == "PDF File List":
    #     get_pdf_paths()
    # elif app_mode == "Q&A Chatbot":
    #     chatbot_qa()

if __name__ == "__main__":
    main()
