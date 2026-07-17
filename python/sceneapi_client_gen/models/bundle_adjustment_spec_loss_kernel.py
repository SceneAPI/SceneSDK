from enum import Enum


class BundleAdjustmentSpecLossKernel(str, Enum):
    CAUCHY = "cauchy"
    HUBER = "huber"
    SOFT_L1 = "soft_l1"
    SQUARED = "squared"
    TUKEY = "tukey"

    def __str__(self) -> str:
        return str(self.value)
