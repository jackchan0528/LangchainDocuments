from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.chains import ConversationChain
import os

# Set APIkey for OpenAI Service
# Can sub this out for other LLM providers
def read_api_key():
    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

os.environ['OPENAI_API_KEY'] = read_api_key()

llm = OpenAI(model_name='text-davinci-003', 
             temperature=0, 
             max_tokens = 256)

memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=memory
)
     
conversation.predict(input="Hi there! I am Jack")