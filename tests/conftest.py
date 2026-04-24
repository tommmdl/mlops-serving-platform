import pytest
from app.model import reset_model


@pytest.fixture(autouse=True)
def reset_singletons():
    reset_model()
    yield
    reset_model()
