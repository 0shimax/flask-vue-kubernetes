#!/bin/bash

echo "Creating the database credentials..."
kubectl apply -f ./kubernetes/secret.yml


echo "Creating the flask deployment and service..."
kubectl create -f ./kubernetes/flask-deployment.yml
kubectl create -f ./kubernetes/flask-service.yml


echo "Adding the ingress..."
kubectl apply -f ./kubernetes/ingress.yml
