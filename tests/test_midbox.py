from .eg4 import EG4Test

class TestEG4ClientRead(EG4Test):
    def test_get_inverter_energy_info_integration(self):

        client = self.get_client()

        # Make the actual request to fetch inverter energy info.
        data = client.get_inverter_energy_info()

        # Assert that the data was returned successfully.
        assert data is not None, (
            "Expected non-null data from the inverter energy info endpoint"
        )

    def test_get_month_summary_integration(self):

        client = self.get_client()

        # Make the actual request to fetch month summary.
        data = client.get_month_summary(year="2025", month="02")

        # Assert that the data was returned successfully.
        assert data is not None, (
            "Expected non-null data from the month summary endpoint"
        )

        # Assert that dayMax == 28
        assert data["dayMax"] == 28, "Expected dayMax to be 28"

