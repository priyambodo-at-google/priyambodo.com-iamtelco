import streamlit as st
import base64
from myfunctions.f_callgemini_vertexai import f_callgemini_vertexai_text, f_callgemini_vertexai_vision
from myfunctions.f_callutility_functions import f_upload_image_tocloudstorage

st.header("💬 Talk to a :red[Telco] :blue[Image] for _Analysis_", divider="rainbow")
st.write("Analyzing your Telco Document with the power of _AI_")
#st.divider()

tab1, tab2, tab3  = st.tabs(["Create Description of an Image", "Ask Questions about the Image", "Find a Similar Image using RAG"])

with tab1:

    st.subheader("Create Description of an Image.")  
    st.write("""
Upload a JPG, JPEG, or PNG image and receive a comprehensive, text-based account of its contents, tailored to capture key elements and nuances relevant to Telco domains. Uncover hidden insights and enhance your understanding of visual data with the power of AI.             """)
    st.caption("You can find a sample file from here: https://www.google.com - _(Right Click and select 'Save Link As...')_")  

    vFileExplainChosen = False
    vUploadedFile = st.file_uploader(
        "Choose a JPG, JPEG, PNG file (max 10 MB): \n\n", 
        accept_multiple_files=False, 
        key="vUploadedFile",
        type=["jpg", "jpeg", "png"])

    if vUploadedFile is not None:  # Check if a file has been uploaded
        file_size = len(vUploadedFile.getvalue())  # Now it's safe to call getvalue()
        if file_size > 10 * 1024 * 1024:  # Check file size
            st.error("File size exceeds 10 MB limit. Please upload a smaller file.")
        else:
            if vUploadedFile.type in ['image/png', 'image/jpeg']:
                vFileContent = base64.b64encode(vUploadedFile.read()).decode('utf-8')
                image_display = f'<img src="data:{vUploadedFile.type};base64,{vFileContent}" width="600">'
                st.markdown(image_display, unsafe_allow_html=True)
                st.write("File name of image file :", vUploadedFile.name  )
                vFileExplainChosen = True
            else:
                st.error("Unsupported file type. Please upload a JPG, JPEG, PNG file.")
    else:
        st.info("if you don't have a file to upload, you can download a sample file that is given above.")

    #Explain the Image
    vButtonPrompt = st.button("Explain the Image", type="primary", key="vButtonPrompt")
    vPrompt = """Composition: Describe the overall layout of the image, including the arrangement of objects, use of space, and any dominant lines or shapes.
Objects and Characters: Identify and describe the key objects and characters in the image, their appearance, relationships, and any symbolism they might represent.
Colors and Lighting: Analyze the use of color and lighting in the image, how they contribute to the mood and atmosphere, and any symbolic meaning they might hold.
Emotions and Themes: Discuss the emotions and themes evoked by the image, drawing connections to historical or cultural context, personal experiences, or broader philosophical ideas.
Style and Technique: If relevant, analyze the artist's style and techniques, how they contribute to the overall effect of the image, and any art historical references or movements it might evoke.
"""
    vPrompt += """
Please provide a comprehensive, text-based account of its contents, tailored to capture key elements and nuances relevant in Telco domains. 
Uncover hidden insights and enhance your understanding of visual data with the power of AI.
    """

    if vButtonPrompt and vPrompt and vFileExplainChosen:
        with st.spinner("Generating your Answer based on your Question about the Document..."):
            vFileLocation = f_upload_image_tocloudstorage(vUploadedFile)
            response = f_callgemini_vertexai_vision(vPrompt, vFileLocation)
            if response:
                st.write("Your Result is:")
                st.success(response)
                st.balloons()
    else:
        st.warning("Please upload your document first before clicking on the Submit button.")

with tab2:
    #Ask Questions about the Image
    st.subheader("Ask Follow Up Telco topic Questions to the Image.")  
    st.write("""
Get insights from Telco images with AI-powered follow-up questions. Simply upload a JPG, JPEG, or PNG image and ask your question about it. Our AI will analyze the image and generate follow-up questions specific to Telco topics, helping you uncover hidden information and gain a deeper understanding of the image/visual data that you've uploaded.
             """)
    st.caption("You can find a sample file from here: https://www.google.com - _(Right Click and select 'Save Link As...')_")  

    vFileAskChosen = False
    vAskUploadedFile = st.file_uploader(
        "Choose a JPG, JPEG, PNG file (max 10 MB): \n\n", 
        accept_multiple_files=False, 
        key="vAskUploadedFile",
        type=["jpg", "jpeg", "png"])

    if vAskUploadedFile is not None:  # Check if a file has been uploaded
        file_size = len(vAskUploadedFile.getvalue())  # Now it's safe to call getvalue()
        if file_size > 10 * 1024 * 1024:  # Check file size
            st.error("File size exceeds 10 MB limit. Please upload a smaller file.")
        else:
            if vAskUploadedFile.type in ['image/png', 'image/jpeg']:
                vFileContent = base64.b64encode(vAskUploadedFile.read()).decode('utf-8')
                image_display = f'<img src="data:{vAskUploadedFile.type};base64,{vFileContent}" width="600">'
                st.markdown(image_display, unsafe_allow_html=True)
                st.write("File name of image file :", vAskUploadedFile.name )
                vFileAskChosen = True
            else:
                st.error("Unsupported file type. Please upload a JPG, JPEG, PNG file.")
    else:
        st.info("if you don't have a file to upload, you can download a sample file that is given above.")

    vSampleQuestion = "You are a Telecommunication and Infrastructure Technology Expert, please answer the question about the image based on your persona. Here is the question: What are the relevant insights that I can get from this image for my business?"
    vPromptAsk = st.text_area("Enter your Question about the Image, ensure you ask a question that is relevant to the image.", value=vSampleQuestion, key="vPromptAsk", height=200)
    vButtonAskQuestion = st.button("Ask your Question", type="primary", key="vButtonAskQuestion")
    if vButtonAskQuestion and vPromptAsk and vFileAskChosen:
        with st.spinner("Generating your Answer based on your Question about the Document..."):
            vAskFileLocation = f_upload_image_tocloudstorage(vAskUploadedFile)
            response = f_callgemini_vertexai_vision(vPromptAsk, vAskFileLocation)
            if response:
                st.write("Your Result is:")
                st.success(response)
                st.balloons()    
    else:
        st.warning("Please ensure you already uploaded your document and entered your question before clicking on the Submit button.")
        vStatusFileUploaded = False
    
with tab3:
    st.subheader("Find similar images to the one you uploaded. _(using RAG)_")   
    st.caption("Similarity search will use Retrieval Augmented Generation (RAG) from Vertex Search.")

    url = "https://ai-demos.dev/demos/matching-engine"
    st.markdown(f'<p style="font-size: 16px; color: #6c757d;">Please click on <a href="{url}" target="_blank" style="font-size: 16px; color: #357EBD;">this link</a> to open the application in a new tab.</p>', unsafe_allow_html=True)

    html = """
Traditional image similarity search relies on comparing pixel values or extracting features to find visually similar images. However, with Retrieval Augmented Generation (RAG) and Google Vertex Search (formerly Google Matching Engine), you can achieve a more nuanced and contextually relevant understanding of image similarity.

Here's how it works:

1. **Image Input:** You provide an image as the query.
2. **RAG Embeddings:** Vertex Search extracts high-dimensional representations of the query image and relevant images from its database using a combination of image recognition models and transformers. These embeddings capture not only visual features but also semantic information about the content and context of the image.
3. **Textual Augmentation:** RAG then generates textual descriptions of both the query image and the database images. These descriptions go beyond simply listing objects or colors and attempt to capture the overall meaning and context of the image.
4. **Similarity Search with Text Embeddings:** Vertex Search then uses these textual descriptions to create text embeddings. These embeddings are compared using advanced ranking algorithms to identify images with the most semantically similar descriptions to the query image.

This approach offers several advantages over traditional image similarity search:

* **Improved Accuracy:** RAG goes beyond visual similarity to consider the semantic meaning and context of the image, leading to more accurate and relevant results.
* **Flexibility:** Textual descriptions are more flexible than pixel-based comparisons, allowing for a wider range of queries and image matches. For example, you could find images of "a birthday party with friends" even if the specific objects or colors differ.
* **Uncovering Hidden Connections:** RAG can identify semantically similar images that may not be visually similar, helping you discover unexpected relationships and insights from your image data.

Overall, image similarity search with RAG and Vertex Search provides a powerful tool for exploring and understanding your image collection, enabling you to uncover deeper connections and unlock new possibilities for image-based tasks.
"""
    st.write(html)    
