from enum import Enum


class PluginSpecialAttributeManifestType(str, Enum):
    BOOL = "bool"
    DATATYPE_REF = "datatype-ref"
    ENUM = "enum"
    FLOAT = "float"
    INT = "int"
    OBJECT = "object"
    STR = "str"

    def __str__(self) -> str:
        return str(self.value)
