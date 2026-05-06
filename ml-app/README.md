# ML App — MLOps Pipeline on Ubuntu

A complete MLOps project: iris classifier served via Flask, containerized with Docker, deployed to Kubernetes via ArgoCD GitOps, with CI/CD through GitHub Actions.

## Stack
- **Model**: scikit-learn RandomForest (iris dataset)
- **Serving**: Flask REST API
- **Container**: Docker → GHCR
- **Orchestration**: Kubernetes (kind for local)
- **GitOps**: ArgoCD
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

## Quick Start

### 1. Prerequisites
```bash
# Install Docker, kubectl, kind, helm, python3
# See full guide for commands
```

### 2. Train & build locally
```bash
cd model
pip install scikit-learn joblib
python train.py
docker build -t ghcr.io/YOUR_GITHUB_USERNAME/ml-app:latest .
```

### 3. Push to GHCR
```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
docker push ghcr.io/YOUR_GITHUB_USERNAME/ml-app:latest
```
Make the package **public** in GitHub → Packages settings.

### 4. Create local cluster & install ArgoCD
```bash
kind create cluster --name ml-cluster
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### 5. Deploy via ArgoCD
```bash
# Update argocd/application.yaml with your repo URL first
kubectl apply -f argocd/application.yaml
```

### 6. Test the API
```bash
kubectl port-forward svc/ml-app 5000:5000
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### 7. Monitoring (optional)
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
```

## CI/CD Flow
`git push` → GitHub Actions trains model + builds image + pushes to GHCR → updates `values.yaml` image tag → ArgoCD detects change → redeploys to Kubernetes automatically.

## Remember to replace
- `YOUR_GITHUB_USERNAME` in `helm/ml-app/values.yaml`
- `YOUR_GITHUB_USERNAME` and repo URL in `argocd/application.yaml`
