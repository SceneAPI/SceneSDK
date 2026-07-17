from enum import Enum


class PluginDataTypeManifestKind(str, Enum):
    ARTIFACT = "artifact"
    SCENE_INPUT = "scene_input"

    def __str__(self) -> str:
        return str(self.value)
