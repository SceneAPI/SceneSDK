from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.tool_detection_out_tools import ToolDetectionOutTools


T = TypeVar("T", bound="ToolDetectionOut")


@_attrs_define
class ToolDetectionOut:
    """
    Attributes:
        tools (ToolDetectionOutTools):
    """

    tools: ToolDetectionOutTools

    def to_dict(self) -> dict[str, Any]:
        tools = self.tools.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "tools": tools,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_detection_out_tools import ToolDetectionOutTools

        d = dict(src_dict)
        tools = ToolDetectionOutTools.from_dict(d.pop("tools"))

        tool_detection_out = cls(
            tools=tools,
        )

        return tool_detection_out
