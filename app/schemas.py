from pydantic import BaseModel, field_validator
from typing import List


class PredictRequest(BaseModel):
    features: List[float]

    @field_validator("features")
    @classmethod
    def must_have_four_features(cls, v):
        if len(v) != 4:
            raise ValueError("features must have exactly 4 elements")
        return v


class PredictResponse(BaseModel):
    score: float
    is_anomaly: bool
