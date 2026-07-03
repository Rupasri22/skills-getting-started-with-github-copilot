import copy
import os
import sys
import pytest

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import app as app_module
from fastapi.testclient import TestClient

# Capture initial activities state
INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Reset in-memory activities before each test
    app_module.activities = copy.deepcopy(INITIAL_ACTIVITIES)
    yield
