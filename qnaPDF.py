import streamlit as st
import os
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import json

# Load the API key from a file
def read_api_key():
    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

os.environ['OPENAI_API_KEY'] = read_api_key()

# Create an OpenAI embeddings instance
embeddings = OpenAIEmbeddings()

# Initialize the Langchain components
# llm = OpenAI(temperature=0.1, verbose=True)
llm = ChatOpenAI(temperature=0.1, verbose=True)

vectorstore = Chroma(persist_directory="./chromadb", embedding_function=embeddings)
memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)

retriever = vectorstore.as_retriever()
qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

# Function for the chatbot interaction
def chat_with_chatbot():
    # st.title("Chat with Chatbot")
    # st.write("Chat with the chatbot using the input box below:")
    
    # user_input = st.text_input("You:", key="user_input")
    
    # if st.button("Ask"):
    #     if user_input:
    #         response = qa(user_input)
    #         print(response)
    #         st.write("Chatbot:", response.answer)

    st.title("Chat with Chatbot")
    st.write("Chat with the chatbot using the input box below:")
    
    # Initialize the chat history
    chat_history = {
        'question': '',
        'chat_history': [],
        'answer': ''
    }
    
    user_input = st.text_input("You:", key="user_input")

    if st.button("Ask"):
        if user_input:
            # Append the user input to the chat history
            chat_history['question'] = user_input
            chat_history['chat_history'].append({'content': user_input})
            
            # Ask the question
            chat_history['answer'] = qa(user_input)
            
            # Append the chatbot response to the chat history
            chat_history['chat_history'].append({'content': chat_history['answer'], 'role': 'system'})
            
            # print(chat_history)
            st.subheader("Answer:")
            st.text_area(chat_history['answer']['answer'], value=chat_history['answer']['answer'], height=50, key="chat_answer")

            st.subheader("Chat History:")
            st.text_area("Chat History:", value=chat_history, height=400, key="chat_history")

# Main app with tabs using st.page
def main():
    chat_with_chatbot()

if __name__ == "__main__":
    main()