# Leveraging Your Own Documents in a Langchain Pipeline
This project highlights how to leverage a ChromaDB vectorstore in a Langchain pipeline to create *drumroll please* a GPT Investment Banker (ergh, I cringed as I wrote that, but alas it's actually pretty practical). You can load in a pdf based document and use it alongside an LLM without the need for fine tuning. 

## See it live and in action 📺
[![Tutorial](https://i.imgur.com/M7GcwGH.jpg)](https://youtu.be/u8vQyTzNGVY 'Tutorial')

# Startup 🚀
1. Create a virtual environment `python -m venv pdfbotenv`
2. Activate it: 
   - Windows:`.\pdfbotenv\Scripts\activate`
   - Mac: `source pdfbotenv/bin/activate`
3. Install the required dependencies `pip install -r requirements.txt`
4. Add your OpenAI APIKey to a file called "api_key.txt" by pasting it there.
5. Add your PDF to Source_PDF/
6. Start the app `streamlit run app.py` 
