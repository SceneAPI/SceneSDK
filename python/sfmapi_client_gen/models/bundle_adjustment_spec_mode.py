from enum import Enum


class BundleAdjustmentSpecMode(str, Enum):
    FEATUREMETRIC = "featuremetric"
    RIG = "rig"
    STANDARD = "standard"
    TWO_STAGE = "two_stage"

    def __str__(self) -> str:
        return str(self.value)
