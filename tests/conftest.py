import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True)
def load_env_vars():
    load_dotenv()
    assert os.getenv("EG4_ACCOUNT") is not None, (
        "EG4_ACCOUNT must be set in the environment"
    )
    assert os.getenv("EG4_PASSWORD") is not None, (
        "EG4_PASSWORD must be set in the environment"
    )
    assert os.getenv("EG4_GRIDBOSS_SN") is not None, (
        "EG4_GRIDBOSS_SN must be set in the environment"
    )
    assert os.getenv("EG4_MAIN_INVERTER_SN") is not None, (
        "EG4_MAIN_INVERTER_SN must be set in the environment"
    )
