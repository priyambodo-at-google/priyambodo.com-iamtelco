#from functools import cache
from google.cloud import bigquery
import logging
from google.oauth2 import service_account
from utils.config import get_config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = get_config()

if config['gcp']['use_service_account']:
    logger.info("Using Service account JSON for Authentication")
    print("Using Service account JSON for Authentication")
    credentials = service_account.Credentials.from_service_account_file(config['gcp']['service_account_path'])
    client_bq = bigquery.Client(project=config['gcp']['project_id'], credentials=credentials)
else:
    logger.info("Using Service account or User credentials for Authentication")
    print("Using Service account or User credentials for Authentication")
    client_bq = bigquery.Client(project=config['gcp']['project_id'])


#@cache
def list_bq_datasets_in_project():

    datasets = list(client_bq.list_datasets(project=config['gcp']['project_id']))  # Make an API request.
    dataset_list = []
    if datasets:
        logger.info("Datasets in project {}:".format(config['gcp']['project_id']))
        for dataset in datasets:
            dataset_list.append(dataset.dataset_id)
    else:
        logger.info("{} project does not contain any datasets.".format(config['gcp']['project_id']))
    logger.info(f"Found {len(dataset_list)} Datasets in {config['gcp']['project_id']}")
    return dataset_list

#@cache
def list_bq_tables_in_dataset(dataset):
    tables = list(client_bq.list_tables(dataset))  # Make an API request.
    tables_list = []
    if tables:
        logger.info("Tables in Dataset {}:".format(dataset))
        for table in tables:
            tables_list.append(table.table_id)
    else:
        logger.info(f"{dataset} dataset does not contain any Tables.")
    logger.info(f"Found {len(tables_list)} Datasets in {dataset}")
    return tables_list