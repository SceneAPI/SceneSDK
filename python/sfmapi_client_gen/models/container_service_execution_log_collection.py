from enum import Enum


class ContainerServiceExecutionLogCollection(str, Enum):
    BOTH = "both"
    FILE = "file"
    STDOUT = "stdout"

    def __str__(self) -> str:
        return str(self.value)
