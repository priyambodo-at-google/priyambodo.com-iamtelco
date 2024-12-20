import streamlit as st
import os
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.preview.language_models import TextGenerationModel
import vertexai 
from google.cloud import aiplatform

@st.cache_resource
def f_init_vertexai():
    #export GCP_PROJECT='work-mylab-machinelearning'    # Change this
    #export GCP_REGION='us-central1'                    # If you change this, make sure the region is supported.
    vPROJECT_ID = os.environ.get('GCP_PROJECT')          #Your Google Cloud Project ID
    vLOCATION = os.environ.get('GCP_REGION')             #Your Google Cloud Project Region
    vertexai.init(project=vPROJECT_ID, location=vLOCATION)
    print(f"Vertex AI SDK version: {aiplatform.__version__}")

def f_callgemini_vertexai_text(vPrompt: str, vTemperature=0.9,vMax_output_tokens=1024,vTop_p=0.9,vTop_k=40) -> str:
    llm = GenerativeModel("gemini-pro")
    vPrompt = vPrompt.strip().replace('"',"").replace("\n", " ").replace("\r", " ")
    # vPrompt = """
    # You are an expert at solving word problems. Solve the following problem:
    # I have three houses, each with three cats. 
    # Each cat owns 4 mittens, and a hat. 
    # Each mitten was knit from 7m of yarn, each hat from 4m.
    # How much yarn was needed to make all the items? 
    # Think about it step by step, and show your work.
    #"""
    try :
        responses = llm.generate_content(
            vPrompt,
            generation_config={
                "temperature": vTemperature,
                "max_output_tokens": vMax_output_tokens,
                "top_p": vTop_p,
                "top_k": vTop_k,
            },
            stream=False
            )
        return responses.text
        # for response in responses:
        #     print(response.text)
        #     return response.text
    except Exception as e:
        return e

def f_callgemini_vertexai_chat(vPrompt: str) -> str:
    try :
        llm = GenerativeModel("gemini-pro")
        chat = llm.start_chat()
        responses = chat.send_message(vPrompt)
        return responses.text
    except Exception as e:
        return e

def f_callgemini_vertexai_vision(vPrompt: str, vFileLocation) -> str:
    multimodal_model = GenerativeModel("gemini-pro-vision")
    response = multimodal_model.generate_content(
        [
            Part.from_uri(
                vFileLocation, mime_type="image/jpeg"
            ),
            vPrompt,
        ]
    )
    print(response)
    return response.text

def f_callmedlm_vertexai_text(vPrompt: str) -> str:
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 256,
        "temperature": 0.0,
        "top_k": 40,
        "top_p": 0.80,
    }
    model_instance = TextGenerationModel.from_pretrained("medlm-medium")
    response = model_instance.predict(
        "Question: What causes you to get ringworm?",
        **parameters
    )
    print(f"Response from Model: {response.text}")
    return response.text

if __name__ == "__main__":
    f_init_vertexai()

#Test the Functions
#f_callgemini_vertexai_text("")
#f_callgemini_vertexai_chat("")
#f_callgemini_vertexai_vision("")
#f_callmedlm_vertexai_text("")