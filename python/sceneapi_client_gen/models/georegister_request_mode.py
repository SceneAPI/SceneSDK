from enum import Enum


class GeoregisterRequestMode(str, Enum):
    GPS = "gps"
    SIM3 = "sim3"

    def __str__(self) -> str:
        return str(self.value)
