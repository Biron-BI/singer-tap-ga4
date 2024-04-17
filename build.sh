#!/bin/bash

set -o errexit
set -o pipefail

IMAGE='eu.gcr.io/docker-registry-242806/singer-tap-ga4'

TAGS_DEFAULT=$(git describe --tags --always --first-parent | sed 's/^v//')
echo -n "TAGS [$TAGS_DEFAULT]:"
read TAGS

for TAG in ${TAGS:-$TAGS_DEFAULT}; do
    docker build -t "$IMAGE:$TAG" -f docker/Dockerfile .
    docker push "$IMAGE:$TAG"
done
