import pytest
from .eg4 import EG4Test

class TestEG4ClientWrite(EG4Test):

    @pytest.mark.skip(reason="User skipped this test")
    def test_set_all_to_ac(self):
        client = self.get_client()

        # Make the actual request to set all to AC.
        assert client.prioritize_battery_ac_charging(), "Failed to set all to AC"

    @pytest.mark.skip(reason="User skipped this test")    
    def test_set_all_to_pv(self):
        client = self.get_client()

        # Make the actual request to set all to PV.
        assert client.prioritize_battery_pv_charging(), "Failed to set all to PV"

    def test_set_default_config(self):
        client = self.get_client()

        # Make the actual request to set default config.
        assert client.set_default_config(), "Failed to set default config"

