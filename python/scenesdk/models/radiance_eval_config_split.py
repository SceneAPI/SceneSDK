from enum import Enum


class RadianceEvalConfigSplit(str, Enum):
    ALL = "all"
    TEST = "test"
    TRAIN = "train"
    VAL = "val"

    def __str__(self) -> str:
        return str(self.value)
