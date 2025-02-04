import os
import pytest
from eg4_solar_client import EG4Client  # Adjust the import as needed
from dotenv import load_dotenv

class TestEG4Client:

    def test_get_inverter_energy_info_integration(self):
        account = os.getenv("EG4_ACCOUNT")
        password = os.getenv("EG4_PASSWORD")
        device_serial_number = os.getenv("EG4_DEVICE_SN")

        # skip the test if the credentials are not present.
        if account is None or password is None or device_serial_number is None:
            pytest.skip("EG4_ACCOUNT, EG4_PASSWORD, and EG4_DEVICE_SN must be set in the environment to run this test")

        # Instantiate the client.
        client = EG4Client(
            account=account,
            password=password,
            device_serial_number=device_serial_number
        )

        # Make the actual request to fetch inverter energy info.
        data = client.get_inverter_energy_info()

        # Assert that the data was returned successfully.
        assert data is not None, "Expected non-null data from the inverter energy info endpoint"

@pytest.fixture(scope="session", autouse=True)
def load_env_vars():
    load_dotenv()
    assert os.getenv("EG4_ACCOUNT") is not None, "EG4_ACCOUNT must be set in the environment"
    assert os.getenv("EG4_PASSWORD") is not None, "EG4_PASSWORD must be set in the environment"
    assert os.getenv("EG4_DEVICE_SN") is not None, "EG4_DEVICE_SN must be set in the environment"

