export GCP_PROJECT='work-mylab-machinelearning'    
export GCP_REGION='us-central1'                    

pip install --upgrade pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip