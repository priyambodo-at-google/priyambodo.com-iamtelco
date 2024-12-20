#from functools import cache
from langchain.prompts.prompt import PromptTemplate


#@cache
def get_prompt_template():
    _googlesql_prompt = """You are a GoogleSQL expert. Given an input question, first create a syntactically correct GoogleSQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per GoogleSQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    For the final answer provide a summary of what was done and the answer.
    Use the following format:
    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here"
    Only use the following tables:
    {table_info}
    
    Question: {input}"""

    return PromptTemplate(
        input_variables=["input", "table_info", "top_k"],
        template=_googlesql_prompt,
    )