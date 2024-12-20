import ast
import pandas as pd
import sqlparse

def extract_columns(sql_query):
    stmt = sqlparse.parse(sql_query)[0]
    columns = []
    column_identifiers = []

    # get column_identifieres
    in_select = False
    for token in stmt.tokens:
        if isinstance(token, sqlparse.sql.Comment):
            continue
        if str(token).lower() == 'select':
            in_select = True
        elif in_select and token.ttype is None:
            for identifier in token.get_identifiers():
                column_identifiers.append(identifier)
            break

    # get column names
    for column_identifier in column_identifiers:
        columns.append(column_identifier.get_name())

    return columns

def convert_to_dataframe(SQLResult, columns):
    # Convert the string to a list of tuples
    data = ast.literal_eval(f"{SQLResult}")

    # Create a DataFrame from the list of tuples
    df = pd.DataFrame(data, columns=columns)

    # print(df)
    return df


