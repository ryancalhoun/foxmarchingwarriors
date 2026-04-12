#!/bin/bash
set -e

cd $(dirname $0)

. ../env

docker build . -t $REPO/job:$TIME
docker push $REPO/job:$TIME

env=$(cat <<EOF
PROJECT: $PROJECT
REGION: $REGION
CALENDAR: $CALENDAR
EOF
)

gcloud tasks queues update $QUEUE_NAME \
  --project=$PROJECT \
  --location=$REGION \
  --max-attempts=5 \
  --max-retry-duration=5s \
  --max-doublings=4 \
  --min-backoff=1s \
  --max-backoff=10s \
  --max-dispatches-per-second=5 \
  --max-concurrent-dispatches=1 \
  --http-oidc-service-account-email-override=$GCP_SERVICE_ACCOUNT

gcloud run deploy $JOB_NAME \
  --project=$PROJECT \
  --region=$REGION \
  --image=$REPO/job:$TIME \
  --port=5000 \
  --timeout=30 \
  --no-allow-unauthenticated \
  --env-vars-file=<(echo "$env") \
  --set-secrets=RESEND_API_KEY=resend-api-key:latest
