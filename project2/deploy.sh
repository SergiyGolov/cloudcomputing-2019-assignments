#!/usr/bin/env bash

# Connect to docker with ludovicherbelin
echo 896f6473-8a6c-4920-9f05-9be916a0c511 | docker login --username ludovicherbelin --password-stdin

# Push the infos service image on dockerhub
docker tag info-service-v1:latest ludovicherbelin/info-service-v1:latest
docker push ludovicherbelin/info-service-v1


# Push the infos service image
docker tag image-service-v1:latest ludovicherbelin/image-service-v1:latest
docker push ludovicherbelin/image-service-v1

# Logout from ludovicherbelin
docker logout

# Creates the service account secret for the cluster to access the cloudsql instance 
# using the given credentials file
kubectl create secret generic cloudsql-instance-credentials --from-file=cc-sql-acc.json

# Deploy using the yaml file
kubectl create -f all.yaml --dry-run=true -o yaml | kubectl apply -f -