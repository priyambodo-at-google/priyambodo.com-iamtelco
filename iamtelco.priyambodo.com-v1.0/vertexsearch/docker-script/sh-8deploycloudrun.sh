#/bin/bash
#-----------------------------------------------------------------------------------#
# gcloud auth configure-docker us-central1-docker.pkg.dev
docker push us-central1-docker.pkg.dev/work-mylab-machinelearning/app-containers-repo/vertexsearch-alphabetfinancialdocs-html-app:v2
#gcloud artifacts repositories list --location=us-central1
#gcloud artifacts repositories describe app-containers-repo --location=us-central1
#-----------------------------------------------------------------------------------#
gcloud run deploy \
  --image=us-central1-docker.pkg.dev/work-mylab-machinelearning/app-containers-repo/vertexsearch-alphabetfinancialdocs-html-app:v2 \
  --region us-central1 \
  --allow-unauthenticated \
  --platform managed \
  --port 80 
#-----------------------------------------------------------------------------------#

#This script is not used, since it needs Docker installed in MacOS