#!/usr/bin/env bash
# build and push the infos service image
docker build -t info-service-v1 ./info/

# build and push the infos service image
docker build -t image-service-v1 ./image/
