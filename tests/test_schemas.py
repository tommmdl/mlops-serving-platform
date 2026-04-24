from app.schemas import PredictRequest, PredictResponse

def test_predict_request_valid():
    req = PredictRequest(features=[1.0, -0.5, 2.1, 0.3])
    assert req.features == [1.0, -0.5, 2.1, 0.3]

def test_predict_request_wrong_length():
    import pytest
    with pytest.raises(Exception):
        PredictRequest(features=[1.0, 2.0])  # precisa de 4 features

def test_predict_response():
    resp = PredictResponse(score=-0.15, is_anomaly=True)
    assert resp.is_anomaly is True
    assert resp.score == -0.15
