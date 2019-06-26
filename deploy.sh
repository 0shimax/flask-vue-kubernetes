#!/bin/bash

echo "Building and upload flask app image"
docker build -t gcr.io/${PROJECT_ID}/hello-flask-app:v2 ./services/server
gcloud docker -- push gcr.io/${PROJECT_ID}/hello-flask-app:v2

echo "Creating cluster"
gcloud container clusters create hello-flask-cluster --num-nodes=1 --zone us-central1-b

echo "Creating the flask deployment"
kubectl apply -f ./kubernetes/flask-deployment.yml

kubectl run hello-flask-web --image=gcr.io/${PROJECT_ID}/hello-flask-app:v1 --port 8080

kubectl expose deployment hello-flask-web --type=LoadBalancer --port 80 --target-port 8080
