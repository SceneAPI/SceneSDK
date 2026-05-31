from enum import Enum


class RadianceEvalConfigBackground(str, Enum):
    BLACK = "black"
    DATASET = "dataset"
    RANDOM = "random"
    WHITE = "white"

    def __str__(self) -> str:
        return str(self.value)
