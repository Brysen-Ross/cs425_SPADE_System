# Mock printer implementation for testing purposes. Does not connect to Moonraker or any real printer
from dataclasses import dataclass

@dataclass
class PrinterStatus:
    connected: bool = False
    state: str = "Offline"
    progress: float = 0.0
    nozzle_temperature: float = 0.0
    bed_temperature: float = 0.0

class MockPrinter:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True
        return True
    
    def disconnect(self):
        self.connected = False
        return True

    def get_status(self):
        return PrinterStatus(
            connected=self.connected,
            state="Printing" if self.connected else "Offline",
            progress=0.32 if self.connected else 0.0,
            nozzle_temperature=200.0 if self.connected else 0.0,
            bed_temperature=60.0 if self.connected else 0.0)
    