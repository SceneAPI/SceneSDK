from enum import Enum


class RadianceEvalConfigMetricsItem(str, Enum):
    LPIPS = "lpips"
    PSNR = "psnr"
    SSIM = "ssim"

    def __str__(self) -> str:
        return str(self.value)
