#pip install google-generativeai google-ai-generativelanguage langchain_core langchain-google-genai langchain_experimental

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import HumanMessage

import requests
import os

from langchain.chat_models import ChatVertexAI
from langchain_core.output_parsers import StrOutputParser

# Set Environment in your Shell
#export GCP_PROJECT='work-mylab-machinelearning'     # Change this
#export GCP_REGION='us-central1'                     # If you change this, make sure the region is supported.

#Using Vertex AI (not using the Bard API or Free Google AI Studio)
from google.cloud import aiplatform
import vertexai
PROJECT_ID = os.environ.get('GCP_PROJECT') #Your Google Cloud Project ID
LOCATION = os.environ.get('GCP_REGION')   #Your Google Cloud Project Region
vertexai.init(project=PROJECT_ID, location=LOCATION)

def get_langchain_gemini(
    vInput: str, model_name: str = "gemini-pro", temperature: float = 0.7, max_tokens: int = 1024
) -> str:
    """
    Creates a LangChain with Vertex AI, allowing for customization of prompt, model, temperature, and max tokens.
    Args:
        vInput (str): The input prompt to be sent to the model.
        model_name (str, optional): The name of the Vertex AI model to use (defaults to "gemini-pro").
        temperature (float, optional): The randomness of the model's output. Defaults to 0.7.
        max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 150.
    Returns:
        str: The output generated by the Vertex AI model.
    """
    vPrompt = vInput
    _prompt = ChatPromptTemplate.from_template("{vPrompt}")
    _model = ChatVertexAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens)
    _output_parser = StrOutputParser()
    chain = _prompt | _model | _output_parser
    result = chain.run()
    return result

def get_langchain_gemini_text(vInput: str) -> str:

    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
    result = llm.invoke("Write a meal plan for today")
    print(result.content)

    for chunk in llm.stream("Write a 6 days trip plan for Penang, Kuala Lumpur and Melacca"):
        print(chunk.content)
        print("---")
    
    prompt = ChatPromptTemplate.from_template(
        "tell me about {topic}"
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    print(chain.invoke({"topic": "Artificial Intelligence"}))

def get_langchain_gemini_vision(vInput: str) -> str:

    llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", temperature=0.7)
    image_url = "https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/static/img/agents_vs_chains.png"
    content = requests.get(image_url).content

    message = HumanMessage(content=[{"type": "text", "text": "What's in this image and who lives there?"}, 
                                    {"type": "image_url", "image_url": image_url}])
    print(llm.invoke([message]).content)

# Example usage:
#vResult = get_langchain_gemini(vInput="Write a poem about a starry night", temperature=0.95)
#print(vResult)
    
get_langchain_gemini_text("")