import streamlit as st
import os
import shutil
from st_pages import Page, Section, show_pages, add_page_title

# Function to get relative paths of selected PDF files
def showPDF():
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

showPDF()