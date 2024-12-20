import logging

from google.cloud import aiplatform
from google.oauth2 import service_account
from langchain.llms import VertexAI

from utils.config import get_config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = get_config()

if config['gcp']['use_service_account']:
    logger.info("Using Service account JSON for Authentication")
    credentials = service_account.Credentials.from_service_account_file(config['gcp']['service_account_path'])
    aiplatform.init(project=config['gcp']['project_id'], location=config['llm']['model_region'],
                    credentials=credentials)
else:
    logger.info("Using Service account or User credentials for Authentication")
    aiplatform.init(project=config['gcp']['project_id'], location=config['llm']['model_region'])


def get_llm(top_p, top_k, max_tok, temp):
    llm = VertexAI(
        model_name=config['llm']['model_name'],
        max_output_tokens=max_tok,
        temperature=temp,
        top_p=top_p,
        top_k=top_k,
        verbose=True,
    )
    return llm