import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

def train():
    rng = np.random.RandomState(42)
    normal = rng.randn(1000, 4)
    anomalies = rng.uniform(low=-6, high=6, size=(50, 4))
    X = np.concatenate([normal, anomalies])

    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)

    os.makedirs("app", exist_ok=True)
    joblib.dump(model, "app/model.joblib")
    print("Model trained and saved to app/model.joblib")

if __name__ == "__main__":
    train()
