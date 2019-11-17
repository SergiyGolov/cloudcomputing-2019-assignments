#!/usr/bin/env bash
# Push the infos service image on dockerhub
docker tag info-service-v1:latest ludovicherbelin/info-service-v1:latest
docker push ludovicherbelin/info-service-v1


# Push the infos service image
docker tag image-service-v1:latest ludovicherbelin/image-service-v1:latest
docker push ludovicherbelin/image-service-v1

# Deploy using the yaml file
kubectl create -f all.yaml