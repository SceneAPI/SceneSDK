from enum import Enum


class ExportSpecFormat(str, Enum):
    COLMAP_BIN = "colmap_bin"
    COLMAP_TEXT = "colmap_text"
    GAUSSIAN_SPLATTING = "gaussian_splatting"
    INSTANT_NGP = "instant_ngp"
    KAPTURE = "kapture"
    NERFSTUDIO = "nerfstudio"
    NVM = "nvm"
    PLY = "ply"

    def __str__(self) -> str:
        return str(self.value)
