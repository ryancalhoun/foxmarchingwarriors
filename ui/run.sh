#!/bin/bash
set -e

cd $(dirname $0)
. ../env

npm run serve
