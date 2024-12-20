#/bin/bash
#gcloud init
#gcloud auth login
#gcloud config set project work-mylab-machinelearning
#gcloud components update

export GCP_REGION='us-central1'
export GCP_PROJECT='work-mylab-machinelearning'
export AR_REPO='iamtelco-priyambodocom-artifactregistry'  
export SERVICE_NAME='iamtelco-priyambodo-com' 

#gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker
gcloud auth configure-docker "$GCP_REGION-docker.pkg.dev"
gcloud builds submit --tag "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME"

gcloud run deploy "$SERVICE_NAME" \
   --image="$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME" \
   --port=8080 \
   --allow-unauthenticated \
   --region=$GCP_REGION \
   --platform=managed  \
   --project=$GCP_PROJECT \
   --set-env-vars=GCP_PROJECT=$GCP_PROJECT,GCP_REGION=$GCP_REGION

#Result: 
#https://iamrich-priyambodo-com-rzmyhdhywa-uc.a.run.app/