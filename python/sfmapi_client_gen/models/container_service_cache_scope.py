from enum import Enum


class ContainerServiceCacheScope(str, Enum):
    GLOBAL = "global"
    PLUGIN = "plugin"
    REQUEST = "request"

    def __str__(self) -> str:
        return str(self.value)
