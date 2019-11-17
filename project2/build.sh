#!/usr/bin/env bash
# build and push the infos service image
docker build -t info-service-v1 ./infos/python_server/

# build and push the infos service image
# docker build -t image-service-v1 ./images/python_server/
