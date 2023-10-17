import streamlit as st

# Set the title and icon for the web app
st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="✅",
)

# Define the layout of the homepage
st.title("Welcome to PDF Chatbot")
# st.write("This is an example of a Streamlit homepage.")

# Add images to the homepage
st.image("images/img3.png", use_column_width=True)
st.image("images/img2.jpg", use_column_width=True, caption="AI Chatbot with PDFs")

# Create an interactive feature - a button
if st.button("Click Me!"):
    st.write("You clicked the button!")

# Add a slider for user interaction
slider_value = st.slider("Select a value:", 0, 100, 50)
st.write(f"You selected: {slider_value}")

# Add text and descriptions
st.header("About Streamlit")
st.write(
    "Streamlit is an open-source Python library that makes it easy to create web applications for data science and machine learning. "
    "With Streamlit, you can turn your data scripts into shareable web apps with minimal effort."
)

# Add a link to Streamlit's official website
st.subheader("Learn more about Streamlit")
st.markdown("[Official Streamlit Website](https://streamlit.io/)")