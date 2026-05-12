from enum import Enum


class CameraModelOutDistortion(str, Enum):
    NONE = "none"
    OPENCV_BROWN = "opencv_brown"
    OPENCV_FISHEYE = "opencv_fisheye"
    OTHER = "other"
    RADIAL = "radial"

    def __str__(self) -> str:
        return str(self.value)
