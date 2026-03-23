#!/bin/bash

BUCKET=gs://foxmarchingwarriors-web

cd $(dirname $0)
(cd web && npm run build)

gcloud storage cp setup.sh $BUCKET/setup.sh
gcloud storage cp -R api $BUCKET/web/
gcloud storage cp -R web/dist $BUCKET/web/

gcloud compute \
  instance-groups managed \
  rolling-action replace web-group \
  --region us-central1 --project foxmarchingwarriors
