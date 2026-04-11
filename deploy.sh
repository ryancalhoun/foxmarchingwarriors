#!/bin/bash
set -e

./ui/deploy.sh
./jobs/deploy.sh
./service/deploy.sh

