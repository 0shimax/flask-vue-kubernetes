#!/bin/bash

# set env
export PROJECT_ID="$(gcloud config get-value project -q)"
gcloud config set compute/zone us-central1-b

echo "Building and upload flask app image"
docker build -t gcr.io/${PROJECT_ID}/hello-flask-app:v2 ./services/server
gcloud docker -- push gcr.io/${PROJECT_ID}/hello-flask-app:v2

echo "Creating cluster"
gcloud container clusters create hello-flask-cluster --num-nodes=1 --zone us-central1-b

echo "Creating the flask deployment and service"
kubectl create -f ./kubernetes/flask-deployment.yml
kubectl create -f ./kubernetes/flask-service.yml

echo "Get external IP address"
kubectl describe service flask

# kubectl run hello-flask-web --image=gcr.io/${PROJECT_ID}/hello-flask-app:latest --port 8080
# kubectl expose deployment hello-flask-web --type=LoadBalancer --port 80 --target-port 8080
