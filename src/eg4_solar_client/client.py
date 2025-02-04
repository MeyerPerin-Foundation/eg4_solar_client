import requests
import logging
from dotenv import load_dotenv
from pprint import pprint
import os

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more granular logs
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("eg4_solar_client")


class EG4Client:
    def __init__(self, account: str, password: str, device_serial_number: str):
        self.session = requests.Session()

        # Credentials
        payload = {
            "account": account,
            "password": password,
        }

        self.device_serial_number = device_serial_number

        response = self.session.post(
            "https://monitor.eg4electronics.com/WManage/web/login", data=payload
        )
        if response.status_code == 200:
            logger.info("Login to EG4 monitoring successful")
        else:
            logger.error("Login failed:", response.text)

    def get_inverter_energy_info(self):
        payload = {
            "serialNum": self.device_serial_number,
        }
        response = self.session.post(
            "https://monitor.eg4electronics.com/WManage/api/midbox/getMidboxRuntime",
            data=payload,
        )

        if response.status_code == 200:
            logger.info("Successfully got EG4 inverter energy info")
            return response.json()
        else:
            logger.error("Failed to get inverter energy info:", response.text)


def main():
    eg4_client = EG4Client(
        account=os.getenv("EG4_ACCOUNT"),
        password=os.getenv("EG4_PASSWORD"),
        device_serial_number=os.getenv("EG4_DEVICE_SN"),
    )

    data = eg4_client.get_inverter_energy_info()
    pprint(data)

if __name__ == "__main__":
    load_dotenv()
    main()
