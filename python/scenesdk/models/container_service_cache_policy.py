from enum import Enum


class ContainerServiceCachePolicy(str, Enum):
    NONE = "none"
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"

    def __str__(self) -> str:
        return str(self.value)
