# mlops-serving-platform

![CI/CD](https://github.com/tommmdl/mlops-serving-platform/actions/workflows/ci-cd.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Docker](https://img.shields.io/badge/docker-multi--stage-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Plataforma de serving de modelo ML (Isolation Forest) via FastAPI, containerizada com Docker e deployada em Kubernetes. Portfólio de MLOps end-to-end.

## Stack

| Camada | Tecnologia |
|---|---|
| API | FastAPI + uvicorn |
| Modelo | scikit-learn Isolation Forest |
| Containerização | Docker multi-stage |
| Dev | Docker Compose |
| Produção | Kubernetes (EKS) |
| CI/CD | GitHub Actions + AWS ECR |
| Observabilidade | Prometheus |

## Rodar localmente

### Pré-requisitos
- Docker + Docker Compose
- Python 3.11

### 1. Treinar o modelo

```bash
pip install -r app/requirements.txt
python scripts/train_model.py
```

### 2. Subir a stack

```bash
cd compose
docker-compose up --build
```

Acesse:
- API: http://localhost/health
- Prometheus: http://localhost:9090

### 3. Testar o endpoint /predict

```bash
curl -X POST http://localhost/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.1, -0.2, 0.3, 0.0]}'
```

Response:
```json
{"score": -0.142, "is_anomaly": false}
```

## Deploy em produção (EKS)

### Pré-requisitos
- Cluster EKS configurado
- ECR repository criado
- Secrets no GitHub: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `EKS_CLUSTER_NAME`, `ECR_REGISTRY`

### Deploy automático
Push para `main` dispara o pipeline completo: testes → build → push ECR → deploy EKS.

### Deploy manual

```bash
export ECR_REGISTRY=<sua-conta>.dkr.ecr.us-east-1.amazonaws.com
export IMAGE_TAG=latest

python scripts/train_model.py
docker build -f docker/Dockerfile -t $ECR_REGISTRY/mlops-serving:$IMAGE_TAG .
docker push $ECR_REGISTRY/mlops-serving:$IMAGE_TAG

sed -i "s|\${ECR_REGISTRY}|$ECR_REGISTRY|g" k8s/deployment.yaml
sed -i "s|\${IMAGE_TAG}|$IMAGE_TAG|g" k8s/deployment.yaml
kubectl apply -f k8s/
```

## Testes

```bash
python scripts/train_model.py
pytest tests/ -v
```

## Arquitetura

Ver [ARCHITECTURE.md](ARCHITECTURE.md)
