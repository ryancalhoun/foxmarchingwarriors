#!/bin/bash

PROJECT=foxmarchingwarriors
BUCKET=$PROJECT-static
SERVICE_IMAGE=us-central1-docker.pkg.dev/$PROJECT/docker/service
JOB_IMAGE=us-central1-docker.pkg.dev/$PROJECT/docker/job
TIME=$(date +%Y%m%d-%H%M%S)

cd $(dirname $0)
(
  cd ui
  NODE_ENV=production npm run build
  cd dist
  gcloud storage cp -R . gs://$BUCKET
)

(
  cd service
  docker build . -t $SERVICE_IMAGE:$TIME
  docker push $SERVICE_IMAGE:$TIME
)

(
  cd jobs
  docker build . -t $JOB_IMAGE:$TIME
  docker push $JOB_IMAGE:$TIME
)

env=$(cat <<EOF
PROJECT: $PROJECT
BUCKET: $BUCKET
INDEX: |
  $(cat ./ui/dist/index.html)
EOF
)

gcloud run deploy foxmarchingwarriors \
  --no-invoker-iam-check \
  --project=$PROJECT \
  --region=us-central1 \
  --image=$SERVICE_IMAGE:$TIME \
  --port=5000 \
  --timeout=10 \
  --allow-unauthenticated \
  --min-instances=1 \
  --startup-probe=timeoutSeconds=1,periodSeconds=10,httpGet.port=5000,httpGet.path=/api/started \
  --liveness-probe=timeoutSeconds=1,periodSeconds=300,httpGet.port=5000,httpGet.path=/api/alive \
  --env-vars-file=<(echo "$env") \
  --set-secrets=JWT_KEY=jwt-secret:latest

gcloud run jobs deploy background-job \
  --project=$PROJECT \
  --region=us-central1 \
  --image=$JOB_IMAGE:$TIME \
  --set-env-vars=PROJECT=$PROJECT \
  --set-secrets=RESEND_API_KEY=resend-api-key:latest
