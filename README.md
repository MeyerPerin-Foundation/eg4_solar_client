# EG4 Solar Client

This is a client for the EG4 solar monitoring API.

## Installation

```bash
pip install eg4-solar-client
```

## Usage

```python
from eg4_solar_client import EG4Client

    # Your EG4 account credentials.
    account = "your_account"
    password = "your_password"
    device_serial_number = "your_device_serial_number"

    # Instantiate the client.
    client = EG4Client(
        account=account,
        password=password,
        device_serial_number=device_serial_number
    )

    # Make the actual request to fetch inverter energy info.
    data = client.get_inverter_energy_info()
```

The `data` variable will contain a JSON object with the data returned by your device.
