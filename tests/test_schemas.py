import pytest
from pydantic import ValidationError
from app.schemas import PredictRequest, PredictResponse

def test_predict_request_valid():
    req = PredictRequest(features=[1.0, -0.5, 2.1, 0.3])
    assert req.features == [1.0, -0.5, 2.1, 0.3]

def test_predict_request_wrong_length():
    with pytest.raises(ValidationError) as exc_info:
        PredictRequest(features=[1.0, 2.0])
    assert "exactly 4 elements" in str(exc_info.value)

def test_predict_request_too_many_features():
    with pytest.raises(ValidationError):
        PredictRequest(features=[1.0, 2.0, 3.0, 4.0, 5.0])

def test_predict_response():
    resp = PredictResponse(score=-0.15, is_anomaly=True)
    assert resp.is_anomaly is True
    assert resp.score == -0.15
