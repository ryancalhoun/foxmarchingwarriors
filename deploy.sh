#!/bin/bash

PROJECT=foxmarchingwarriors
BUCKET=gs://$PROJECT-static
IMAGE=us-central1-docker.pkg.dev/$PROJECT/docker/www-api
TIME=$(date +%Y%m%d-%H%M%S)

cd $(dirname $0)
(
  cd web
  NODE_ENV=production npm run build
  cd dist
  gcloud storage cp -R . $BUCKET
)

(
  cd api
  docker build . -t $IMAGE:$TIME
  docker push $IMAGE:$TIME
)

env=$(cat <<EOF
PROJECT: $PROJECT
BUCKET: $BUCKET
INDEX: |
  $(cat ./web/dist/index.html)
EOF
)

gcloud run deploy foxmarchingwarriors \
  --no-invoker-iam-check \
  --project=$PROJECT \
  --region=us-central1 \
  --image=$IMAGE:$TIME \
  --port=5000 \
  --timeout=10 \
  --allow-unauthenticated \
  --min-instances=1 \
  --liveness-probe=timeoutSeconds=1,httpGet.port=5000,httpGet.path=/api/health \
  --env-vars-file=<(echo "$env") \
  --set-secrets=JWT_KEY=jwt-secret:latest
