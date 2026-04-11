#!/bin/bash
set -e

PROJECT=foxmarchingwarriors
REGION=us-central1
BUCKET=$PROJECT-static
SERVICE_IMAGE=$REGION-docker.pkg.dev/$PROJECT/docker/service
JOB_IMAGE=$REGION-docker.pkg.dev/$PROJECT/docker/job
TIME=$(date +%Y%m%d-%H%M%S)
SERVICE_ACCOUNT=377984045382-compute@developer.gserviceaccount.com

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

gcloud run deploy background-jobs \
  --project=$PROJECT \
  --region=$REGION \
  --image=$JOB_IMAGE:$TIME \
  --port=5000 \
  --timeout=30 \
  --no-allow-unauthenticated \
  --set-env-vars=PROJECT=$PROJECT \
  --set-secrets=RESEND_API_KEY=resend-api-key:latest

background_service_url=$(
  gcloud run services describe background-jobs \
    --project=$PROJECT \
    --region=$REGION \
    --format=json | jq -r .status.url
)

gcloud tasks queues update queue \
  --project=$PROJECT \
  --location=$REGION \
  --max-attempts=5 \
  --max-retry-duration=5s \
  --max-doublings=4 \
  --min-backoff=1s \
  --max-backoff=10s \
  --max-dispatches-per-second=5 \
  --max-concurrent-dispatches=1 \
  --http-oidc-service-account-email-override=$SERVICE_ACCOUNT

env=$(cat <<EOF
PROJECT: $PROJECT
REGION: $REGION
BUCKET: $BUCKET
QUEUE: queue
SEND_URL: $background_service_url/send
INDEX: |
  $(cat ./ui/dist/index.html)
EOF
)

gcloud run deploy foxmarchingwarriors \
  --no-invoker-iam-check \
  --project=$PROJECT \
  --region=$REGION \
  --image=$SERVICE_IMAGE:$TIME \
  --port=5000 \
  --timeout=10 \
  --allow-unauthenticated \
  --min-instances=1 \
  --startup-probe=timeoutSeconds=1,periodSeconds=10,httpGet.port=5000,httpGet.path=/api/started \
  --liveness-probe=timeoutSeconds=1,periodSeconds=300,httpGet.port=5000,httpGet.path=/api/alive \
  --env-vars-file=<(echo "$env") \
  --set-secrets=JWT_KEY=jwt-secret:latest
