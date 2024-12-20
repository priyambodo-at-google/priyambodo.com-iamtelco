import streamlit as st
import base64
from myfunctions.f_callgemini_vertexai import f_callgemini_vertexai_text
from myfunctions.f_callutility_functions import f_upload_file_tocloudstorage, f_get_the_local_file_path, f_remove_the_local_file_path
from myfunctions.f_calldocumentai_summary import f_process_document_summarizer

st.header("💬 Talk to a :red[Telco] :blue[Document] for _Analysis_", divider="rainbow")
st.write("Analyzing your Telco Document with the power of _AI_")
#st.divider()

tab1, tab2, tab3  = st.tabs(["Document Summarization","Document Analysis/Q&A","Document Explorer"])

with tab1:

    st.subheader("Summarize your Document using Document AI.")  
    st.caption("You can find a sample file from here: https://www.google.com - _(Right Click and select 'Save Link As...')_")  

    vStatusFileUploadedSum = False
    vUploadedFileSum = st.file_uploader(
        'Choose a "PDF" file (max 10 MB and 15 pages only for this demo): \n\n', 
        accept_multiple_files=False, 
        type=["PDF"])

    if vUploadedFileSum is not None:  # Check if a file has been uploaded
        file_sizeSum = len(vUploadedFileSum.getvalue())  # Now it's safe to call getvalue()
        if file_sizeSum > 10 * 1024 * 1024:  # Check file size
            st.error("File size exceeds 10 MB limit. Please upload a smaller file.")
        else:
            if vUploadedFileSum.type == "application/pdf":
                vFileContentSum = base64.b64encode(vUploadedFileSum.read()).decode('utf-8')
                st.write("File Name of PDF file :", vUploadedFileSum.name)
                pdf_displaySum = f'<iframe src="data:application/pdf;base64,{vFileContentSum}" width="800" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_displaySum, unsafe_allow_html=True)
                vStatusFileUploadedSum = True
            else:
                st.error("Unsupported file type as of now. Please upload a PDF file.")
    else:
        st.info("if you don't have a file to upload, you can download a sample file that is given above.")
        vStatusFileUploadedSum = False

    vLengthSum = st.radio(
        "Select your Summarization Length preference: \n\n",
        ["Auto", "Brief", "Moderate", "Comprehensive"],
        key="vLengthSum",
        horizontal=True,
        index=0  
    )
    vFormatSum = st.radio(
        "Select your Summarization Format preference: \n\n",
        ["Auto", "Paragraph", "Bullets"],
        key="vFormatSum",
        horizontal=True,
        index=0  
    )

    vButtonUploadSum = st.button("Submit", type="primary", key="vButtonUploadSum")
    if vButtonUploadSum and vStatusFileUploadedSum:
        with st.spinner("Creating your summary, please wait..."):

            #Start to Call Document AI (still manual, need to be automated from variable later on)
            project_id = 'work-mylab-machinelearning'
            location = "us" # Format is "us" or "eu"
            processor_id = "dd5b50441d53f49d" # Create processor before running sample
            processor_version = "fddf2b010581ffe1" # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
            file_path = "/path/to/local/pdf"
            mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types

            file_path = f_get_the_local_file_path(vUploadedFileSum)
            response = f_process_document_summarizer(project_id,location,processor_id,processor_version,file_path,mime_type, vLengthSum, vFormatSum)

            st.write("Your Result is:")
            st.success(response)

            # st.markdown(response, unsafe_allow_html=True)
            # st.markdown("""
            # <style>
            # p {
            #     font-family: sans-serif;
            #     font-size: 16px;
            #     line-height: 1.5;
            #     margin: 10px 0;
            # }
            # </style>
            # """, unsafe_allow_html=True)            

            f_remove_the_local_file_path(file_path)
    else:
        st.warning("Please upload your document first before clicking on the Submit button.")


with tab2:

    st.subheader("Analyze/Q&A to your Document using Vertex Search.")  
    st.write("You can find the ready to use Q&A document in here: https://iamtelco-priyambodo-com-html-rzmyhdhywa-uc.a.run.app")

    st.write("---")
    st.write("This complete full cycle of application is :red[**still under development**]. Please wait for the next update.")

    vStatusFileUploaded = False
    vUploadedFile = st.file_uploader(
        "Choose a PDF, HTML or TXT file (max 10 MB): \n\n", 
        accept_multiple_files=False, 
        type=["pdf", "html", "txt"])

    if vUploadedFile is not None:  # Check if a file has been uploaded
        file_size = len(vUploadedFile.getvalue())  # Now it's safe to call getvalue()
        if file_size > 10 * 1024 * 1024:  # Check file size
            st.error("File size exceeds 10 MB limit. Please upload a smaller file.")
        else:
            if vUploadedFile.type == "text/plain":
                vFileContent = vUploadedFile.getvalue().decode("utf-8")
                st.write("File Name of TXT file :", vUploadedFile.name)
                st.write(vFileContent)
                vStatusFileUploaded = True
            elif vUploadedFile.type == 'text/html':
                vFileContent = vUploadedFile.read()  
                st.write("File Name of HTML file :", vUploadedFile.name)
                html_display = f'<iframe srcdoc="{vFileContent}" width="800" height="600"></iframe>'
                #st.markdown(html_display, unsafe_allow_html=True)
                st.write(html_display)
                vStatusFileUploaded = True
            elif vUploadedFile.type == "application/pdf":
                vFileContent = base64.b64encode(vUploadedFile.read()).decode('utf-8')
                st.write("File Name of PDF file :", vUploadedFile.name)
                pdf_display = f'<iframe src="data:application/pdf;base64,{vFileContent}" width="800" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
                vStatusFileUploaded = True
            else:
                st.error("Unsupported file type. Please upload a PDF, HTML or TXT file.")
    else:
        st.info("if you don't have a file to upload, you can download a sample file that is given above.")
        vStatusFileUploaded = False

    vButtonUpload = st.button("Submit", type="primary", key="vButtonUpload")
    if vButtonUpload and vStatusFileUploaded:
        with st.spinner("Upload the document and creating the index in Vertex AI..."):
            vFileLocation = f_upload_file_tocloudstorage(vUploadedFile)
            st.success(vFileLocation)
    else:
        st.warning("Please upload your document first before clicking on the Submit button.")

    vPromptContext = st.text_area(
    "Give the context before asking the question:... (example given below)): \n\n",
    key="vPromptContext",
    value="You are a Telco analysis, who would like to analyze the following document. Use chain of thought to answer the questions.\n\n",  
    height=100
    )

    vPromptQuestion = st.text_area(
    "Ask your specific question here:... (example given below)): \n\n",
    key="vPromptQuestion",
    value="Summarize the document in bullet points format.\n\n",  
    height=100
    )

    vButtonPrompt = st.button("Submit", type="primary", key="vButtonPrompt")
    vPrompt = vPromptContext + vPromptQuestion
    vPrompt = vPrompt.strip()
    if vButtonPrompt and vPrompt and vStatusFileUploaded:
        vTemperature = 0.0
        vTokens = 1024
        with st.spinner("Generating your Answer based on your Question about the Document..."):
            #response = f_get_vertexsearch_chain(vPromptContext, vPromptQuestion)
            response = "This module is still under development. Please check back soon."
            if response:
                st.write("Your Result is:")
                st.success(response)
                st.balloons()    
    else:
        st.warning("Please upload your document first before clicking on the Submit button.")

with tab3:
    st.subheader("Document Explorer")    
    url = "https://lookerstudio.google.com/c/reporting/f0337926-8d79-496d-a8d9-7f31f6f69d1c/page/kDmiD"
    st.markdown(f'<p style="font-size: 14px; color: #6c757d;">Please click on <a href="{url}" target="_blank" style="font-size: 14px; color: #357EBD;">this link</a> to open the application in a new tab.</p>', unsafe_allow_html=True)

    html = """
 **Document Explorer** is a powerful application designed to streamline document management and enhance data accessibility across your organization. It empowers you with three key features to optimize your workflow:

**1. Invoice Processing:**
- Effortlessly extract essential information from invoices.
- Automatically populate BigQuery with organized invoice data, enabling seamless integration with your business intelligence and analytics tools.

**2. Contract Management:**
- Maintain a comprehensive overview of all contracts within a centralized repository.
- Easily access and manage contract information, ensuring organized and efficient contract administration.

**3. Intelligent Content Search:**
- Leverage the advanced capabilities of Vertex AI Search to effortlessly locate specific content within your contract documents.
- Uncover relevant information quickly and efficiently, saving time and enhancing productivity.

**Document Explorer** effectively eliminates manual document handling challenges, allowing you to focus on strategic initiatives while driving data-driven decisions and optimizing contract management processes.
"""    
    st.write(html)