from enum import Enum


class ToolDetectionSource(str, Enum):
    ENV = "env"
    PATH = "path"

    def __str__(self) -> str:
        return str(self.value)
