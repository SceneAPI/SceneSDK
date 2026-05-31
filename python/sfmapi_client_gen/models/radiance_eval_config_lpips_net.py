from enum import Enum


class RadianceEvalConfigLpipsNet(str, Enum):
    ALEX = "alex"
    SQUEEZE = "squeeze"
    VGG = "vgg"

    def __str__(self) -> str:
        return str(self.value)
