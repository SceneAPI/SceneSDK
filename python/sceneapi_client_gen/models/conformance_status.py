from enum import Enum


class ConformanceStatus(str, Enum):
    FAILING = "failing"
    NOT_RUN = "not_run"
    PARTIAL = "partial"
    PASSING = "passing"

    def __str__(self) -> str:
        return str(self.value)
