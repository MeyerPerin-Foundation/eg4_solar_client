import requests
from dotenv import load_dotenv
import os

def main():
    LOGIN_URL = "https://monitor.eg4electronics.com/WManage/web/login"
    # DATA_URL =  "https://monitor.eg4electronics.com/WManage/api/inverter/getInverterEnergyInfoParallel"
    DATA_URL =  "https://monitor.eg4electronics.com/WManage/api/midbox/getMidboxRuntime"


    session = requests.Session()

    # Credentials
    payload = {
        "account": os.getenv("ACCOUNT"),
        "password": os.getenv("PASSWORD"),
    }

    response = session.post(LOGIN_URL, data=payload)
    if response.status_code == 200:
        print("Login successful")
                
        data_payload={
            "serialNum" : "4354850208"
        }

        protected_data = session.post(DATA_URL, data=data_payload)
        print(protected_data.text)
    else:
        print("Login failed:", response.text)


if __name__ == "__main__":
    load_dotenv()
    main()
