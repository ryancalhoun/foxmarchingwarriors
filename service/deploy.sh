#!/bin/bash
set -e

cd $(dirname $0)

. ../env

docker build . -t $REPO/service:$TIME
docker push $REPO/service:$TIME

background_service_url=$(
  gcloud run services describe $JOB_NAME \
    --project=$PROJECT \
    --region=$REGION \
    --format=json | jq -r .status.url
)

env=$(cat <<EOF
PROJECT: $PROJECT
REGION: $REGION
BUCKET: $BUCKET
QUEUE: $QUEUE_NAME
SEND_URL: $background_service_url/send
INDEX: |
  $(cat ../ui/dist/index.html)
EOF
)

gcloud run deploy $APP_NAME \
  --no-invoker-iam-check \
  --project=$PROJECT \
  --region=$REGION \
  --image=$REPO/service:$TIME \
  --port=5000 \
  --timeout=10 \
  --allow-unauthenticated \
  --min-instances=1 \
  --startup-probe=timeoutSeconds=1,periodSeconds=10,httpGet.port=5000,httpGet.path=/api/started \
  --liveness-probe=timeoutSeconds=1,periodSeconds=300,httpGet.port=5000,httpGet.path=/api/alive \
  --env-vars-file=<(echo "$env") \
  --set-secrets=JWT_KEY=jwt-secret:latest
