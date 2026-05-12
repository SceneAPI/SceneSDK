from enum import Enum


class ProjectionJobRequestOperation(str, Enum):
    CUBEMAP_TO_EQUIRECTANGULAR = "cubemap_to_equirectangular"
    EQUIRECTANGULAR_TO_CUBEMAP = "equirectangular_to_cubemap"
    EQUIRECTANGULAR_TO_PERSPECTIVE = "equirectangular_to_perspective"

    def __str__(self) -> str:
        return str(self.value)
