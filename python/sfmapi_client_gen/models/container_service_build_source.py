from enum import Enum


class ContainerServiceBuildSource(str, Enum):
    GIT = "git"
    LOCAL = "local"
    RELEASE = "release"

    def __str__(self) -> str:
        return str(self.value)
