#!/bin/bash
set -e

APPS=("app-about" "app-research" "app-api")
NAMESPACE="id-039"

echo "=== [1/3] Building Container Images (No Docker Hub Required) ==="
for app in "${APPS[@]}"; do
    echo ">>> Building $app:1.0 ..."
    if command -v minikube &> /dev/null && minikube status &> /dev/null; then
        eval $(minikube docker-env)
        docker build -t "$app:1.0" "./apps/$app"
    elif command -v k3s &> /dev/null; then
        docker build -t "$app:1.0" "./apps/$app"
        docker save "$app:1.0" | sudo k3s ctr images import -
    elif command -v kind &> /dev/null && [ -n "$(kind get clusters 2>/dev/null)" ]; then
        docker build -t "$app:1.0" "./apps/$app"
        kind load docker-image "$app:1.0"
    else
        docker build -t "$app:1.0" "./apps/$app"
    fi
done

echo "=== [2/3] Deploying Kubernetes Manifests ==="
kubectl apply -f k8s/

echo "=== [3/3] Waiting for Pods to be Ready ==="
kubectl rollout status deployment/app-about -n $NAMESPACE --timeout=120s
kubectl rollout status deployment/app-research -n $NAMESPACE --timeout=120s
kubectl rollout status deployment/app-api -n $NAMESPACE --timeout=120s

echo ""
echo "Deployment Completed Successfully!"
kubectl get all,ingress,pvc -n $NAMESPACE