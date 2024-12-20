#/bin/bash

poetry shell #--> Just do this if you already install and configure your Poetry

brew install python
brew link python@3.11
brew install pip

pip install --upgrade pip
pip install --upgrade poetry
rm pyproject.toml
rm poetry.lock

#Initialize the Poetry environment 
poetry new myapp #(optional)
poetry init

#Activate the environment in your directory
poetry config virtualenvs.in-project true
poetry install
poetry shell

#Add your Python Dependency Package (based on your needs)
poetry add streamlit
poetry add google-cloud-aiplatform
poetry add google-cloud-logging
poetry add google-cloud-documentai
poetry add langchain=0.0.235
poetry add sqlparse=0.4.4
poetry add SQLAlchemy=1.4.49
poetry add sqlalchemy-bigquery;python_version < '3.12'
#pip install google-generativeai google-ai-generativelanguage langchain_core langchain-google-genai langchain_experimental

#Create requirements.txt (optional)
poetry export -f requirements.txt --output requirements.txt

#Operational that you might need (optional)
poetry remove streamlit #removing package
poetry install --no-root #optional if you change toml manual
poetry lock #optional if you change toml manual
poetry env list
poetry env info
poetry show --tree
poetry show --latest
poetry exit
poetry update
deactivate #deactivate the environment