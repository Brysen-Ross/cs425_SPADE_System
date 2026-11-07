import urllib.request
import json
from spade.mock_printer import PrinterStatus

class Moonraker:
    def __init__(self, base_url="http://127.0.0.1:7125"):
        self.base_url = base_url

    def connect(self):
        try:
            url = f"{self.base_url}/printer/info"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.load(response)
            return data["result"]["state"] == "ready"
        except (OSError, ValueError, KeyError, TypeError):
            return False

    def is_connected(self):
        try:
            url = f"{self.base_url}/server/info"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.load(response)
            return "result" in data
        except (OSError, ValueError, KeyError, TypeError):
            return False

    def get_status(self):
        url = f"{self.base_url}/printer/objects/query?print_stats&extruder&heater_bed&virtual_sdcard"

        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.load(response)
            status = data["result"]["status"]

            printer_state = status["print_stats"]["state"]
            nozzle_temp = status["extruder"]["temperature"]
            bed_temp = status["heater_bed"]["temperature"]
            progress = status["virtual_sdcard"]["progress"]

            return PrinterStatus(
                connected=True,
                state=printer_state.capitalize(),
                progress=progress,
                nozzle_temperature=nozzle_temp,
                bed_temperature=bed_temp
            )

        except (OSError, ValueError, KeyError, TypeError):
            return PrinterStatus(
                connected=False,
                state="Offline",
                nozzle_temperature=0.0,
                bed_temperature=0.0,
                progress=0.0
            )
            