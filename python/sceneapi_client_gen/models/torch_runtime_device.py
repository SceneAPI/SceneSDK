from enum import Enum


class TorchRuntimeDevice(str, Enum):
    CPU = "cpu"
    CUDA = "cuda"

    def __str__(self) -> str:
        return str(self.value)
