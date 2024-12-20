import streamlit as st
import time
from utils.bq_utils import list_bq_datasets_in_project, list_bq_tables_in_dataset
from utils.llm import get_llm
from utils.prompt_template import get_prompt_template
from utils.sql import get_sql_engine, get_sql_db, get_db_chain
from utils.convert_df import extract_columns
from utils.convert_df import convert_to_dataframe

SQLALCHEMY_SILENCE_UBER_WARNING=1 # Silence Deprecated API features

from utils.config import get_config

config = get_config()

# Setup the Streamlit App
st.set_page_config(page_title=config['application']['name'], page_icon=None, layout=config['application']['layout'],
                   initial_sidebar_state="auto", menu_items=None)
col1, col2 = st.columns([0.1,0.9])
with col1:
    st.subheader("")
    st.image("image/bqicon.png")
with col2:
    st.title(f"{config['application']['name']} ")

st.markdown(
"""
You can ask any questions to your data in a table at specific dataset using human natural language powered by Google GenAI.
Please check some example questions to explore and visualize the data.
""",
unsafe_allow_html=True,
)

temp = float(config['llm']['temperature'])
top_k = int(config['llm']['top_k'])
top_p = float(config['llm']['top_p'])
max_tok = int(config['llm']['token_limit'])

source_dataset_selected = None
table_selected = None

# Allow users to select the Dataset and table via a sidebar
with st.sidebar:
    #source_gcp_project_id_selected = st.text_input("Source Project", config['gcp']['project_id'])
    source_gcp_project_id_selected = config['gcp']['project_id']
    source_dataset_list = ["Please Select"] + list_bq_datasets_in_project()
    source_dataset_selected = st.selectbox("Select a Dataset/Database:", source_dataset_list)
    table_list = []
    if source_dataset_selected != "Please Select":
        table_list = ["Please Select"] + list_bq_tables_in_dataset(source_dataset_selected)
        table_selected = st.selectbox("Select a Table to ask:", table_list)
    st.markdown("***")

    #Create Stateful button
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    def click_button():
        st.session_state.clicked = True

    if st.session_state.clicked:
        show_model_params = False if st.button('Hide Model Parameters') else True
        st.slider("Temperature", min_value=0.0, max_value=1.0, step=0.01, key="temp", value=temp)
        st.slider("TopK", min_value=1, max_value=40, step=1, key="topk", value=top_k)
        st.slider("TopP", min_value=0.0, max_value=1.0, step=0.01, key="topp", value=top_p)
        st.slider("Max Tokens", min_value=10, max_value=int(config['llm']['max_token_limit']), key="tok", step=16,
                value=max_tok)
        top_p = st.session_state.topp
        top_k = st.session_state.topk
        max_tok = st.session_state.tok
        temp = st.session_state.temp

# Retrieve and cache the model
llm = get_llm(top_p, top_k, max_tok, temp)
# retrieve and cache the prompt template
GOOGLESQL_PROMPT = get_prompt_template()

# Allow the user to view the text field to ask questions, only when a table has been selected
dataset_and_table_selected = False
if source_dataset_selected == "Please Select":
    st.info("Please select a Dataset from the side panel (please choose bicarait_financial_data dataset for demo purpose)")
else:
    if table_selected == "Please Select":
        st.info("Please select a Table from the side panel (please choose sales_data table for demo purpose)")
    else:
        dataset_and_table_selected = True

if 'question' not in st.session_state:
    st.session_state.question = ''

def clear_all():
    st.cache_data.clear()
    st.session_state.load_state = False

if dataset_and_table_selected:
    st.subheader("What question would you like to ask?")
    st.markdown(f"Please note this this question will use the data contained within table: "
                f"**{table_selected}** to answer the question.")
    st.text_area("Enter your Prompt:", key="question", height=100, value="", on_change=clear_all)
    st.text("example questions: ")
    st.markdown("- how much is the biggest sales until now and from which customer?")
    st.markdown("- what is the top 5 highest sales and from which customer?")

    prompt_question = st.session_state.question

    @st.cache_data(show_spinner=False)

    def submit_question(): #the main function
        engine = get_sql_engine(source_dataset_selected)
        db = get_sql_db(engine, [table_selected])
        db_chain = get_db_chain(llm, db)
  
        t0 = time.time()
        final_prompt = GOOGLESQL_PROMPT.format(input=prompt_question, table_info=table_selected, top_k=2000000)
        print(final_prompt)
        
        # result = db_chain.run(final_prompt)
        result = db_chain(final_prompt)
        st.markdown("**Using the following SQL Query:**")
        
        # Print the SQL Query
        sql_query = result["intermediate_steps"][1]
        st.success(sql_query)
        
        # Print the Answer
        st.markdown("**Answer:**")
        answer = result["result"]
        st.success(answer)
        return result

    if "load_state" not in st.session_state:
        st.session_state.load_state = False

    submit = True if st.button('Submit Question') else False

    if submit or st.session_state.load_state:
        st.session_state.load_state = True
        with st.spinner("Please wait.. Google GenAI is working now..."):
            try:
                result = submit_question()
                try:
                    sql_query = result["intermediate_steps"][1]
                    SQLResult = result["intermediate_steps"][3]
                    columns = extract_columns(sql_query)
                    df = convert_to_dataframe(SQLResult, columns)
                    
                    st.header("Visualize")
                    table = st.checkbox("Table")
                    bar_chart = st.checkbox("Bar Chart")
                    line_chart = st.checkbox("Line Chart")
                    if table:
                        st.subheader("Table")
                        st.dataframe(df,hide_index=True)
                    if bar_chart:
                        st.subheader("Bar Chart")
                        # Get the type of the column
                        for col in df.columns:
                            dtype = df[col].dtype
                            if dtype == 'object':
                                x_axis=col
                            elif dtype == 'int64' or dtype == 'float64':
                                y_axis=col
                            else:
                                x_axis = None
                                y_axis = None
                        st.bar_chart(data=df,x=x_axis, y=y_axis)
                    if line_chart:
                        st.subheader("Line Chart")
                        # Get the type of the column
                        for col in df.columns:
                            dtype = df[col].dtype
                            if dtype == 'object':
                                x_axis=col
                            elif dtype == 'int64' or dtype == 'float64':
                                y_axis=col
                            else:
                                x_axis = None
                                y_axis = None
                        st.line_chart(data=df,x=x_axis, y=y_axis)

                except Exception as e:
                    st.header("Visualize")
                    st.warning(f"Sorry there are no Vizualisations available for this result")

            except Exception as e:
                #st.error(f"An Error Occurred. Check you're using the correct table!")
                st.error()
                               
# with tab3:
#     st.subheader("LLM's and Langchain")
#     st.markdown('**The rise of Large Language Models (LLMs) LLMs have revolutionized the way developers build applications.**.'
#                 'LLMs are capable of understanding and responding to natural language, which opens up a whole new '
#                 'world of possibilities for database communication.')
#     st.markdown(
#         '**LangChain is an orchestration tool that leverages the power of LLMs to transform the way you interact with your database..**.'
#         'With LangChain, you can simply converse with your database in natural language, and LangChain will translate your '
#         'queries into SQL and return the results in real time.')
#     st.markdown(
#         '**This makes it possible to build applications that were once impossible, such as chatbots that can answer '
#         'your questions about your database, or applications that can automatically generate reports based on your data..**.'
#         'Generative AI is the future of database communication, and its available today.')

#     st.markdown("**Here are some specific examples of how LangChain can be used:**")
#     st.markdown("* A chatbot that can answer questions about your database in natural language.")
#     st.markdown("* An application that can automatically generate reports based on your data.")
#     st.markdown("* A tool that can help you debug your database queries.")
#     st.markdown("* A system that can track changes to your database and notify you of any errors.")

#     st.markdown("LangChain uses SQLAlchemy to connect to SQL databases, we can use any SQL dialect supported "
#                 "by SQLAlchemy, such as MS SQL, MySQL, MariaDB, PostgreSQL, Oracle SQL, BigQuery, or SQLite.")

#     st.title("")
#     st.subheader("Considerations")
#     st.markdown("**Here are a few consideration when using LLM for generating SQL queries:**")
#     st.markdown("* LLMs are trained on large datasets of text and code. This allows them to learn the patterns "
#                 "of human language and how to generate text that is similar to human-written text")
#     st.markdown("* However, LLMs are not perfect. They can sometimes struggle to understand natural "
#                 "language queries that are not well-formed or that do not contain all the necessary information.")
#     st.markdown("* This is especially true when the database is large. A large database can contain a lot of data, "
#                 "and it can be difficult for an LLM to identify the relevant information from a natural language query.")
#     st.markdown("**As a result, it is important to be aware of the limitations of LLMs when using them to interact with "
#                 "databases.** If you are using an LLM to query a database, it is important to make sure that your "
#                 "questions are as informative as possible. You should also be prepared to provide additional "
#                 "information if the LLM is unable to understand your query.")

# with tab2:
#     st.header("Example Questions")
#     st.markdown("**Here are some example questions** (Note, these will need to be changed based on your specific tables):")
#     st.markdown("**Table:** :blue[stg_client]")
#     st.markdown("* What is the average age of all females?")
#     st.markdown("* What are the top 5 occupations and the count of each? Provide the answer in point format.")
#     st.markdown("* Provide a breakdown of males vs females?")
#     st.markdown("**Table:** :blue[stg_card_transactions]")
#     st.markdown("* Whats the most popular merchant and how many transactions did they handle?")
#     st.markdown("* What date had the most transactions?")
#     st.markdown("* Whats the total number of fraudulent transactions?")
#     st.markdown("* What are the top 5 highest transactions and from which retailer? Provide the answer in point format.")