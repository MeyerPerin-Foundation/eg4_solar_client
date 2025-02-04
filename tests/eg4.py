import os
import pytest
from eg4_solar_client import EG4Client  # Adjust the import as needed

class EG4Test:

    def get_client(self):
        account = os.getenv("EG4_ACCOUNT")
        password = os.getenv("EG4_PASSWORD")
        gridboss_sn = os.getenv("EG4_GRIDBOSS_SN")
        main_inverter_sn = os.getenv("EG4_MAIN_INVERTER_SN")

        # skip the test if the credentials are not present.
        if (
            account is None
            or password is None
            or gridboss_sn is None
            or main_inverter_sn is None
        ):
            pytest.skip(
                "EG4_ACCOUNT, EG4_PASSWORD, and EG4_GRIDBOSS_SN and EG4_MAIN_INVERTER_SN must be set in the environment to run this test"
            )

        # Instantiate the client.
        client = EG4Client(
            account=account,
            password=password,
            gridboss_sn=gridboss_sn,
            main_inverter_sn=main_inverter_sn,
        )

        return client
