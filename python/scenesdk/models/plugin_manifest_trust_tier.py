from enum import Enum


class PluginManifestTrustTier(str, Enum):
    COMMUNITY = "community"
    LOCAL = "local"
    OFFICIAL = "official"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
