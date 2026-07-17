from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.rotation import Rotation


T = TypeVar("T", bound="Sim3")


@_attrs_define
class Sim3:
    """Similarity Sim(3) transform: ``y = s * R @ x + t``.

    Attributes:
        rotation (Rotation): Hamilton quaternion stored ``(w, x, y, z)``.
        translation (list[float]):
        scale (float):
    """

    rotation: Rotation
    translation: list[float]
    scale: float

    def to_dict(self) -> dict[str, Any]:
        rotation = self.rotation.to_dict()

        translation = []
        for translation_item_data in self.translation:
            translation_item: float
            translation_item = translation_item_data
            translation.append(translation_item)

        scale = self.scale

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "rotation": rotation,
                "translation": translation,
                "scale": scale,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rotation import Rotation

        d = dict(src_dict)
        rotation = Rotation.from_dict(d.pop("rotation"))

        translation = []
        _translation = d.pop("translation")
        for translation_item_data in _translation:

            def _parse_translation_item(data: object) -> float:
                return cast(float, data)

            translation_item = _parse_translation_item(translation_item_data)

            translation.append(translation_item)

        scale = d.pop("scale")

        sim_3 = cls(
            rotation=rotation,
            translation=translation,
            scale=scale,
        )

        return sim_3
