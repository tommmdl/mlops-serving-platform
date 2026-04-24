import pytest
from app.model import ModelLoader, get_model, reset_model

@pytest.fixture(autouse=True)
def clear_singleton():
    reset_model()
    yield
    reset_model()

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

def test_get_model_singleton_identity():
    m1 = get_model()
    m2 = get_model()
    assert m1 is m2
