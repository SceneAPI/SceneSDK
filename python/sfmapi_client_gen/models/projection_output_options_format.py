from enum import Enum


class ProjectionOutputOptionsFormat(str, Enum):
    JPG = "jpg"
    PNG = "png"
    SOURCE = "source"
    WEBP = "webp"

    def __str__(self) -> str:
        return str(self.value)
