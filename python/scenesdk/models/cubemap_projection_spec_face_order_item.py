from enum import Enum


class CubemapProjectionSpecFaceOrderItem(str, Enum):
    BACK = "back"
    DOWN = "down"
    FRONT = "front"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"

    def __str__(self) -> str:
        return str(self.value)
