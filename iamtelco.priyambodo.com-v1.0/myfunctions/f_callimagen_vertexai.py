import streamlit as st
import os
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai 
from google.cloud import aiplatform
from vertexai.preview.vision_models import Image, ImageGenerationModel
from vertexai.vision_models import ImageTextModel, Image

@st.cache_resource
def f_init_vertexai():
    #export GCP_PROJECT='work-mylab-machinelearning'    #Change this
    #export GCP_REGION='us-central1'                    #If you change this, make sure the region is supported.
    vPROJECT_ID = os.environ.get('GCP_PROJECT')         #Your Google Cloud Project ID
    vLOCATION = os.environ.get('GCP_REGION')            #Your Google Cloud Project Region
    vertexai.init(project=vPROJECT_ID, location=vLOCATION)
    print(f"Vertex AI SDK version: {aiplatform.__version__}")

def f_callimagen_createimage(vPrompt: str) -> str:
    model = ImageGenerationModel.from_pretrained("imagegeneration@005")
    images = model.generate_images(prompt="A dog reading the newspaper",
    # Optional:
    number_of_images=2,
    seed=1
    )
    images[0].save(location="./gen-img1.png", include_generation_parameters=True)
    images[1].save(location="./gen-img2.png", include_generation_parameters=True)
    # Optional. View the generated images in a notebook.
    # images[0].show()
    # images[1].show()

def f_callimagen_editimage(vPrompt: str) -> str:
    model = ImageGenerationModel.from_pretrained("imagegeneration")
    base_img=Image.load_from_file(location='./gen-img1.png')
    images = model.edit_image(base_image=base_img, prompt="pop art style",
    # Optional:
    seed=1,
    guidance_scale=20,
    number_of_images=2
    )
    images[0].save(location="./edit-img1.png")
    images[1].save(location="./edit-img2.png")
    # Optional. View the edited images in a notebook.
    # images[0].show()
    # images[1].show()

def f_callimagen_decribeimage(vPrompt: str) -> str: #I think it is better use gemini rather than this
    model = ImageTextModel.from_pretrained("imagetext@001")
    source_image = Image.load_from_file(location='./gen-img1.png')
    captions = model.get_captions(
        image=source_image,
        # Optional:
        number_of_results=2,
        language="en",
    )
    print(captions)
    return(captions)

def f_callimagen_askimage(vPrompt:str) -> str: #I think it is better use gemini rather than this
    model = ImageTextModel.from_pretrained("imagetext@001")
    source_image = Image.load_from_file(location='./gen-img1.png')
    answers = model.ask_question(
        image=source_image,
        question="What breed of dog is this a picture of?",
        # Optional:
        number_of_results=2,
    )
    print(answers)
    return(answers)

if __name__ == "__main__":
    f_init_vertexai()

#Test the Functions
#f_callgemini_vertexai_vision("")