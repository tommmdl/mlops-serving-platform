# Architecture

## Overview

```
Internet
   │
   ▼
[Nginx :80]
   │  reverse proxy
   ▼
[FastAPI :8000]
   │              │
   ▼              ▼
[IsolationForest] [Prometheus metrics]
  (model.joblib)       │
                       ▼
                 [Prometheus :9090]
```

## Dev Stack (Docker Compose)

- `nginx` — entry point, reverse proxy para `api`
- `api` — FastAPI + Isolation Forest, expõe `/health`, `/predict`, `/metrics`
- `prometheus` — scrape das métricas a cada 15s

## Production Stack (Kubernetes)

- `Deployment` — 2 replicas mínimas, liveness/readiness em `/health`
- `Service` (ClusterIP) — balanceia tráfego entre pods
- `HPA` — escala de 2 a 5 pods quando CPU > 70%

## CI/CD (GitHub Actions)

1. `test` job — instala deps, treina modelo, roda pytest
2. `build-and-push` job — build Docker, push ECR (só em `main`)
3. `deploy` job — atualiza kubeconfig EKS, aplica manifests K8s
