from pydantic import BaseModel, field_validator


class PredictRequest(BaseModel):
    features: list[float]

    @field_validator("features")
    @classmethod
    def must_have_four_features(cls, v):
        if len(v) != 4:
            raise ValueError(f"features must have exactly 4 elements, got {len(v)}")
        return v


class PredictResponse(BaseModel):
    score: float
    is_anomaly: bool
