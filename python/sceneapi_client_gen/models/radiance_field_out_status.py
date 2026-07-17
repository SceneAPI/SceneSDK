from enum import Enum


class RadianceFieldOutStatus(str, Enum):
    CANCELLED = "cancelled"
    CANCELLED_DIRTY = "cancelled_dirty"
    FAILED = "failed"
    RUNNING = "running"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
