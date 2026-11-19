@echo off
echo === [1/2] Building Container Images ===
docker build -t app-about:1.0 ./apps/app-about
docker build -t app-research:1.0 ./apps/app-research
docker build -t app-api:1.0 ./apps/app-api

echo === [2/2] Deploying Kubernetes Manifests ===
kubectl apply -f k8s/

echo === Checking Resources ===
kubectl get all,ingress,pvc -n id-039