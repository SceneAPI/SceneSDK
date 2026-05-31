from enum import Enum


class TorchRuntimePolicy(str, Enum):
    OPTIONAL = "optional"
    RECOMMENDED = "recommended"
    REQUIRED = "required"

    def __str__(self) -> str:
        return str(self.value)
