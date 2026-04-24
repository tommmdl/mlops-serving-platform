from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from app.schemas import PredictRequest, PredictResponse
from app.model import get_model

app = FastAPI(title="MLOps Serving Platform", version="1.0.0")


def _get_or_create_counter(name: str, description: str) -> Counter:
    """Get existing counter or create new one (avoids duplicate registration errors)."""
    try:
        return Counter(name, description)
    except ValueError:
        # Already registered — retrieve from registry
        return REGISTRY._names_to_collectors.get(name) or REGISTRY._names_to_collectors.get(name + "_total")


PREDICT_COUNTER = _get_or_create_counter("predict_requests_total", "Total prediction requests")
ANOMALY_COUNTER = _get_or_create_counter("anomaly_detected_total", "Total anomalies detected")


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
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
