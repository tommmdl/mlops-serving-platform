from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry
from app.schemas import PredictRequest, PredictResponse
from app.model import get_model

app = FastAPI(title="MLOps Serving Platform", version="1.0.0")

METRICS_REGISTRY = CollectorRegistry(auto_describe=True)

PREDICT_COUNTER = Counter(
    "predict_requests_total",
    "Total prediction requests",
    registry=METRICS_REGISTRY,
)
ANOMALY_COUNTER = Counter(
    "anomaly_detected_total",
    "Total anomalies detected",
    registry=METRICS_REGISTRY,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    PREDICT_COUNTER.inc()
    model = get_model()
    score, is_anomaly = model.predict(request.features)
    if is_anomaly:
        ANOMALY_COUNTER.inc()
    return PredictResponse(score=score, is_anomaly=is_anomaly)


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest(METRICS_REGISTRY).decode("utf-8")
