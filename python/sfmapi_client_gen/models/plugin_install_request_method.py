from enum import Enum


class PluginInstallRequestMethod(str, Enum):
    DOCKER = "docker"
    EXTERNAL_TOOL = "external_tool"
    UV = "uv"

    def __str__(self) -> str:
        return str(self.value)
