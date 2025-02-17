import requests
import logging

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more granular logs
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("eg4_solar_client")


class EG4Client:
    def __init__(
        self, account: str, password: str, gridboss_sn: str, main_inverter_sn: str
    ):
        self.session = requests.Session()

        # Credentials
        payload = {
            "account": account,
            "password": password,
        }

        self.gridboss_sn = gridboss_sn
        self.main_inverter_sn = main_inverter_sn

        response = self.session.post(
            "https://monitor.eg4electronics.com/WManage/web/login", data=payload
        )
        if response.status_code == 200:
            logger.info("Login to EG4 monitoring successful")
        else:
            logger.error("Login failed:", response.text)

    def get_inverter_energy_info(self):
        payload = {
            "serialNum": self.gridboss_sn,
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

    def get_month_summary(self, year: str, month: str):
        payload = {
            "serialNum": self.gridboss_sn,
            "year": year,
            "month": month,
        }
        response = self.session.post(
            "https://monitor.eg4electronics.com/WManage/api/inverterChart/monthColumnParallel",
            data=payload,
        )

        if response.status_code == 200:
            logger.info("Successfully got EG4 monthly summary")
            return response.json()
        else:
            logger.error("Failed to get monthly summary:", response.text)

    def set_working_mode(self, working_mode: str, enable: bool):
        endpoint = "https://monitor.eg4electronics.com/WManage/web/maintain/remoteSet/functionControl"

        # Make sure the working mode is valid
        if working_mode not in ["PV_CHARGE_PRIORITY", "AC_CHARGE_PRIORITY"]:
            raise ValueError(
                "working_mode must be 'PV_CHARGE_PRIORITY' or 'AC_CHARGE_PRIORITY'"
            )

        # convert working mode to the internal EG4 name
        if working_mode == "PV_CHARGE_PRIORITY":
            working_mode_name = "HOLD_FORCED_CHG_EN"

        elif working_mode == "AC_CHARGE_PRIORITY":
            working_mode_name = "FUNC_AC_CHARGE"

        # Make sure the enable value is a boolean
        if not isinstance(enable, bool):
            raise ValueError("enable must be a boolean")

        # convert from boolean to string
        enable_str = "true" if enable else "false"

        payload = {
            "inverterSn": self.main_inverter_sn,
            "functionParam": working_mode_name,
            "enable": enable_str,
            "clientType": "WEB",
            "remoteSetType": "NORMAL",
        }

        response = self.session.post(endpoint, data=payload)

        if response.status_code == 200:
            logger.info("Successfully set working mode")
            return True

    def set_interval(self, working_mode: str, start_time: str, end_time: str):
        # Make sure the working mode is valid
        if working_mode not in ["PV_CHARGE_PRIORITY", "AC_CHARGE_PRIORITY"]:
            raise ValueError(
                "working_mode must be 'PV_CHARGE_PRIORITY' or 'AC_CHARGE_PRIORITY'"
            )

        # Make sure the start and end time are in the correct format
        if len(start_time.split(":")) != 2:
            raise ValueError("start_time must be in the format HH:MM")

        if len(end_time.split(":")) != 2:
            raise ValueError("end_time must be in the format HH:MM")

        # parse the start and end time into start_hour, start_min, end_hour, end_min
        start_hour, start_min = start_time.split(":")
        end_hour, end_min = end_time.split(":")

        # Make sure the start and end time are valid
        if int(start_hour) < 0 or int(start_hour) > 23:
            raise ValueError("start_hour must be between 0 and 23")

        if int(start_min) < 0 or int(start_min) > 59:
            raise ValueError("start_min must be between 0 and 59")

        if int(end_hour) < 0 or int(end_hour) > 23:
            raise ValueError("end_hour must be between 0 and 23")

        if int(end_min) < 0 or int(end_min) > 59:
            raise ValueError("end_min must be between 0 and 59")

        # Now that the data is validated, we need to create two payloads, one to set the start and another one to set the end
        # convert working mode to the internal EG4 name
        if working_mode == "PV_CHARGE_PRIORITY":
            working_mode_name = "HOLD_FORCED_CHARGE"
        elif working_mode == "AC_CHARGE_PRIORITY":
            working_mode_name = "HOLD_AC_CHARGE"

        # if the start time is different from the end time, ensure the function is enabled
        if start_time != end_time:
            self.set_working_mode(working_mode=working_mode, enable=True)

        endpoint = "https://monitor.eg4electronics.com/WManage/web/maintain/remoteSet/writeTime"

        payload_start = {
            "inverterSn": self.main_inverter_sn,
            "timeParam": f"{working_mode_name}_START_TIME",
            "hour": start_hour,
            "minute": start_min,
            "clientType": "WEB",
            "remoteSetType": "NORMAL",
        }

        payload_end = {
            "inverterSn": self.main_inverter_sn,
            "timeParam": f"{working_mode_name}_END_TIME",
            "hour": end_hour,
            "minute": end_min,
            "clientType": "WEB",
            "remoteSetType": "NORMAL",
        }

        response_start = self.session.post(endpoint, data=payload_start)
        response_end = self.session.post(endpoint, data=payload_end)

        if response_start.status_code == 200 and response_end.status_code == 200:
            logger.info("Successfully set PV charge priority interval")
            return True

    def prioritize_battery_pv_charging(
        self, start_time: str = None, end_time: str = None
    ):
        if start_time is not None and end_time is not None:
            self.set_interval(
                working_mode="PV_CHARGE_PRIORITY",
                start_time=start_time,
                end_time=end_time,
            )
        else:
            self.set_interval(
                working_mode="AC_CHARGE_PRIORITY", start_time="00:00", end_time="00:00"
            )
            self.set_interval(
                working_mode="PV_CHARGE_PRIORITY", start_time="00:00", end_time="23:59"
            )

        return True

    def prioritize_battery_ac_charging(
        self, start_time: str = None, end_time: str = None
    ):
        if start_time is not None and end_time is not None:
            self.set_interval(
                working_mode="AC_CHARGE_PRIORITY",
                start_time=start_time,
                end_time=end_time,
            )
        else:
            self.set_interval(
                working_mode="PV_CHARGE_PRIORITY", start_time="00:00", end_time="23:59"
            )

            self.set_interval(
                working_mode="AC_CHARGE_PRIORITY", start_time="00:00", end_time="23:59"
            )

        return True

    def set_default_config(self):
        self.prioritize_battery_ac_charging("16:00", "18:00")
        self.prioritize_battery_pv_charging("06:00", "18:00")

        return True
