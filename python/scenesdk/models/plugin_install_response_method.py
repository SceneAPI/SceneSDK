from enum import Enum


class PluginInstallResponseMethod(str, Enum):
    CONTAINER_SERVICE = "container_service"
    DOCKER = "docker"
    EXTERNAL_TOOL = "external_tool"
    UV = "uv"

    def __str__(self) -> str:
        return str(self.value)
