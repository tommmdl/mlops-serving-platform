import numpy as np
from app.model import ModelLoader

def test_predict_returns_score_and_flag():
    loader = ModelLoader("app/model.joblib")
    score, is_anomaly = loader.predict([0.1, -0.2, 0.3, 0.0])
    assert isinstance(score, float)
    assert isinstance(is_anomaly, bool)

def test_anomaly_detected_for_extreme_values():
    loader = ModelLoader("app/model.joblib")
    score, is_anomaly = loader.predict([10.0, -10.0, 10.0, -10.0])
    assert is_anomaly is True

def test_normal_not_flagged():
    loader = ModelLoader("app/model.joblib")
    score, is_anomaly = loader.predict([0.1, 0.2, -0.1, 0.0])
    assert is_anomaly is False
