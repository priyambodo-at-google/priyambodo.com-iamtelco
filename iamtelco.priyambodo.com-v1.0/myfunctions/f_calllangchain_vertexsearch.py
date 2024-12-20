import os
import streamlit as st
from langchain.chat_models import ChatVertexAI
from langchain.prompts import ChatPromptTemplate
from langchain.retrievers import GoogleVertexAISearchRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

project_id = os.environ.get('GCP_PROJECT') 
vLOCATION = os.environ.get('GCP_REGION')
data_store_id = "iamtelcopriyambodocom-vert_1703844666663"
model_type = "gemini-pro"

def f_get_vertexsearch_chain(vContext, vQuestion) -> str :
    vContext = vContext.replace('"', '')    
    vQuestion = vQuestion.replace('"', '')
    if not data_store_id:
        raise ValueError(
            "No value provided in env variable 'DATA_STORE_ID'. "
            "A  data store is required to run this application."
        )
    model = ChatVertexAI(model_name="gemini-pro", temperature=0.0)
    retriever = GoogleVertexAISearchRetriever(
        project_id=project_id, search_engine_id=data_store_id
    )
    template = f"""Answer the question based only on the following context:
    {vContext}
    Question: {vQuestion}
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        | prompt
        | model
        | StrOutputParser()
    )
    chain = chain.with_types(input_type=Question)
    return chain