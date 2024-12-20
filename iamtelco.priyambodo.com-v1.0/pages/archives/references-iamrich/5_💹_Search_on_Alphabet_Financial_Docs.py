#Import the required Libraries
import streamlit as st
import pandas as pd
from typing import Any

# Defining variables for the project
project_id = "work-mylab-machinelearning"
location = "global"                    # Values: "global"
search_engine_id = "search-alphabet-financialr_1689840102872"
serving_config_id = "default_config"          # Values: "default_config"
search_query = "Google"

def main():
    # Add a title and intro text
    st.title('Explore Alphabet Financial Reports')
    st.text('Ask any questions to these downloaded Alphabet Financial Reports.')

    # Use Alphabet Docs
    st.write('These are the list of the documents that has been downloaded from https://abc.xyz/investor/')
    #f_show_auto_list_of_alphabet_docs()
    f_show_manual_list_of_alphabet_docs()

    # Create a button to upload files
    # Create a button in Streamlit
    url = "https://enterprisesearch-app-rzmyhdhywa-uc.a.run.app/alphabet.html"
    text = "Search your questions about the document in here..."
    create_hyperlink_button(url, text)

def create_hyperlink_button(url, text):
  button_html = f'<a href="{url}" target="_blank">{text}</a>'
  return st.markdown(button_html, unsafe_allow_html=True)

def f_show_html():    # Read the content of the local HTML file
    with open("widget.html", "r") as file:
        html_content = file.read()
    # Render the HTML content using the html component
    # st.components.v1.html(html_content, height=500)
    st.markdown(html_content, unsafe_allow_html=True)
   
def remove_gs_prefix(input_string):
    prefix = "gs://genai-appbuilder-es-alphabetfinancialreport/"
    if prefix in input_string:
        return input_string.replace(prefix, "gs://googlecloudstorage_to_store_files/")
    else:
        return input_string
    
def uploadFilesToStorage(uploaded_files):
    if uploaded_files is not None:
        for f in uploaded_files:
            st.write(f)
        data_list = []
        for f in uploaded_files:
            data = pd.read_csv(f)
            data_list.append(data)
        df = pd.concat(data_list)

def list_documents_genai_es(project_id: str, location: str, search_engine_id: str) -> Any:
    # Create a client
    client = discoveryengine.DocumentServiceClient()
    # The full resource name of the search engine branch.
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=search_engine_id,
        branch="default_branch",
    )
    response = client.list_documents(parent=parent)
    print(f"Documents in {search_engine_id}:")
    for result in response:
        print(result)
    return response

def f_show_auto_list_of_alphabet_docs():
    vResult = list_documents_genai_es(project_id, location, search_engine_id)
    vResult = vResult  # Replace "YOUR_DATA_HERE" with the actual ListDocumentsPager object
    # Create a list of dictionaries for each document in the data
    documents_list = []
    for document in vResult.documents:
        document_data = {
            'File Name': remove_gs_prefix(document.content.uri),
        }
        documents_list.append(document_data)
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(documents_list)
    # Show the DataFrame as a table using Streamlit
    st.dataframe(df)

def f_show_manual_list_of_alphabet_docs():
    vdata = [
        "gs://googlecloudstorage_to_store_files/20210428-alphabet-10q.pdf",
        "gs://googlecloudstorage_to_store_files/2022q2-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/2020_Q4_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/20220202-alphabet-10k.pdf",
        "gs://googlecloudstorage_to_store_files/2022q4-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/2021_Q1_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/goog-10-k-q4-2022.pdf",
        "gs://googlecloudstorage_to_store_files/2021q1-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/2021q2-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/20200731-alphabet-10q.pdf",
        "gs://googlecloudstorage_to_store_files/2022_Q3_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/20220427-alphabet-10q.pdf",
        "gs://googlecloudstorage_to_store_files/20230426-alphabet-10q.pdf",
        "gs://googlecloudstorage_to_store_files/2022q1-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/2021_Q2_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/2022q3-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/goog-exhibit-99-1-q1-2023-19.pdf",
        "gs://googlecloudstorage_to_store_files/2020_Q3_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/20210203-alphabet-10k.pdf",
        "gs://googlecloudstorage_to_store_files/2020-alphabet-annual-report.pdf",
        "gs://googlecloudstorage_to_store_files/2022_Q2_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/2021_Q3_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/2020_Q1_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/2020q3-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/20221025-alphabet-10q.pdf",
        "gs://googlecloudstorage_to_store_files/2022-alphabet-annual-report.pdf",
        "gs://googlecloudstorage_to_store_files/2020q2-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/20201030-alphabet-10q.pdf",
        "gs://googlecloudstorage_to_store_files/20200429-alphabet-10q.pdf",
        "gs://googlecloudstorage_to_store_files/2021q3-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/20220726-alphabet-10q.pdf",
        "gs://googlecloudstorage_to_store_files/2020q4-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/2022_Q4_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/2021-q3-alphabet-10q.pdf",
        "gs://googlecloudstorage_to_store_files/20210728-alphabet-10q.pdf",
        "gs://googlecloudstorage_to_store_files/2023_Q1_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/2020q1-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/2021q4-alphabet-earnings-release.pdf",
        "gs://googlecloudstorage_to_store_files/2020_Q2_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/2021-alphabet-annual-report.pdf",
        "gs://googlecloudstorage_to_store_files/2021_Q4_Earnings_Transcript.pdf",
        "gs://googlecloudstorage_to_store_files/2022_Q1_Earnings_Transcript.pdf",
        ]
    # Create a DataFrame with the data
    df = pd.DataFrame(vdata, columns=["File Name"])
    # Add a new column for "No" starting from 1 to 42
    # df.insert(0, "No", range(1, 43))
    # Show the table in the Streamlit app
    st.dataframe(df)

if __name__ == "__main__":
    main()