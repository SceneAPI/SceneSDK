from enum import Enum


class CameraModelOutProjection(str, Enum):
    FISHEYE = "fisheye"
    OMNIDIRECTIONAL = "omnidirectional"
    OTHER = "other"
    PINHOLE = "pinhole"
    SPHERICAL = "spherical"

    def __str__(self) -> str:
        return str(self.value)
