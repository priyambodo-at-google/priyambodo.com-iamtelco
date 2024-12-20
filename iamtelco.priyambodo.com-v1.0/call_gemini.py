# Utils
import os
import streamlit as st
import time
from typing import List
import urllib
import warnings
from pathlib import Path as p
from pprint import pprint
import pandas as pd
#from pydantic import BaseModel

# Langchain
import langchain
from langchain.prompts import PromptTemplate
from langchain.llms import VertexAI
from langchain.embeddings import VertexAIEmbeddings
from langchain.chat_models import ChatVertexAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
# LangChain
print(f"LangChain version: {langchain.__version__}")

# Set Environment in your Shell
#export GCP_PROJECT='work-mylab-machinelearning'     # Change this
#export GCP_REGION='us-central1'                     # If you change this, make sure the region is supported.

# Vertex AI
from google.cloud import aiplatform
import vertexai
PROJECT_ID = os.environ.get('GCP_PROJECT') #Your Google Cloud Project ID
LOCATION = os.environ.get('GCP_REGION')   #Your Google Cloud Project Region
vertexai.init(project=PROJECT_ID, location=LOCATION)
# Vertex AI
print(f"Vertex AI SDK version: {aiplatform.__version__}")

## LLM model using LangChain
# llm = VertexAI(
#     model_name="text-bison@001",
#     max_output_tokens=256,
#     temperature=0.1,
#     top_p=0.8,
#     top_k=40,
#     verbose=True,
# )

## Chat
# chat = ChatVertexAI()

# Not using LangChain
from vertexai.preview.generative_models import (Content,
                                                GenerationConfig,
                                                GenerativeModel,
                                                GenerationResponse,
                                                Image, 
                                                HarmCategory, 
                                                HarmBlockThreshold, 
                                                Part)

@st.cache_resource
def load_models():
    text_model_pro = GenerativeModel("gemini-pro")
    multimodal_model_pro = GenerativeModel("gemini-pro-vision")
    return text_model_pro, multimodal_model_pro

def get_gemini_pro_text_response( model: GenerativeModel,
                                  contents: str, 
                                  generation_config: GenerationConfig,
                                  stream=True):
    
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    
    responses = model.generate_content(contents,
                                       generation_config = generation_config,
                                       safety_settings=safety_settings,
                                       stream=True)

    final_response = []
    for response in responses:
        try:
            # st.write(response.text)
            print(f"Response: {response.text}")
            final_response.append(response.text)
        except IndexError:
            # st.write(response)
            print(f"Response: {response}")
            final_response.append("")
            continue
    return " ".join(final_response)

def get_gemini_pro_vision_response(model, prompt_list, generation_config={},  stream=True):
    generation_config = {'temperature': 0.1,
                         'max_output_tokens': 2048
                         }
    responses = model.generate_content(prompt_list,
                                       generation_config = generation_config,stream=True)
    final_response = []
    for response in responses:
        try:
            final_response.append(response.text)
        except IndexError: 
            pass
    return("".join(final_response))

# Create function to call Generative AI from Vertex AI
def genai_gemini_text_nolongchain(prompt: str="",vtemperature=0.5,vmax_output_tokens=1024,vtop_p=0.8,vtop_k=40):
    text_model_pro, multimodal_model_pro = load_models()
    prompt = prompt.strip().replace('"',"")
    config = {
        "temperature": vtemperature, # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": vmax_output_tokens, # Token limit determines the maximum amount of text output (2048 is the max).
        "top_p": vtop_p, 
        "top_k": vtop_k  
        }
    if prompt:
        response = get_gemini_pro_text_response(
            text_model_pro,
            prompt,
            generation_config=config,
        )
        if response:
            #print(response)
            return(response)