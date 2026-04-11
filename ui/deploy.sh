#!/bin/bash
set -e

cd $(dirname $0)
. ../env

NODE_ENV=production npm run build

cd dist
gcloud storage cp -R . gs://$BUCKET
