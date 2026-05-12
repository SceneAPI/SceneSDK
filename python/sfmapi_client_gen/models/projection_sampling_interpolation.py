from enum import Enum


class ProjectionSamplingInterpolation(str, Enum):
    CUBIC = "cubic"
    LANCZOS = "lanczos"
    LINEAR = "linear"
    NEAREST = "nearest"

    def __str__(self) -> str:
        return str(self.value)
