from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine
from langchain import SQLDatabase, SQLDatabaseChain

from utils.config import get_config

config = get_config()


def get_sql_engine(DATASET_ID):
    return create_engine(f"bigquery://{config['gcp']['project_id']}/{DATASET_ID}")


def get_sql_db(SQL_ENGINE, TABLES):
    return SQLDatabase(engine=SQL_ENGINE,metadata=MetaData(bind=SQL_ENGINE), include_tables=TABLES)


def get_db_chain(LLM, SQL_DB):
    return SQLDatabaseChain.from_llm(LLM, SQL_DB, return_intermediate_steps=True, verbose=True)