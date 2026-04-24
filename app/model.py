import threading
import joblib
import numpy as np
from typing import Tuple

_lock = threading.Lock()


class ModelLoader:
    def __init__(self, model_path: str):
        self._model = joblib.load(model_path)

    def predict(self, features: list[float]) -> Tuple[float, bool]:
        X = np.array(features).reshape(1, -1)
        score = float(self._model.score_samples(X)[0])
        is_anomaly = bool(self._model.predict(X)[0] == -1)
        return score, is_anomaly


_instance: ModelLoader | None = None


def get_model(model_path: str = "app/model.joblib") -> ModelLoader:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = ModelLoader(model_path)
    return _instance


def reset_model() -> None:
    global _instance
    _instance = None
