from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.problem_error_ctx_type_0 import ProblemErrorCtxType0


T = TypeVar("T", bound="ProblemError")


@_attrs_define
class ProblemError:
    """One structured validation/detail error inside a ProblemResponse.

    Attributes:
        msg (str):
        type_ (str):
        loc (list[int | str] | None | Unset):
        input_ (Any | None | Unset):
        ctx (None | ProblemErrorCtxType0 | Unset):
    """

    msg: str
    type_: str
    loc: list[int | str] | None | Unset = UNSET
    input_: Any | None | Unset = UNSET
    ctx: None | ProblemErrorCtxType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_error_ctx_type_0 import ProblemErrorCtxType0

        msg = self.msg

        type_ = self.type_

        loc: list[int | str] | None | Unset
        if isinstance(self.loc, Unset):
            loc = UNSET
        elif isinstance(self.loc, list):
            loc = []
            for loc_type_0_item_data in self.loc:
                loc_type_0_item: int | str
                loc_type_0_item = loc_type_0_item_data
                loc.append(loc_type_0_item)

        else:
            loc = self.loc

        input_: Any | None | Unset
        if isinstance(self.input_, Unset):
            input_ = UNSET
        else:
            input_ = self.input_

        ctx: dict[str, Any] | None | Unset
        if isinstance(self.ctx, Unset):
            ctx = UNSET
        elif isinstance(self.ctx, ProblemErrorCtxType0):
            ctx = self.ctx.to_dict()
        else:
            ctx = self.ctx

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "msg": msg,
                "type": type_,
            }
        )
        if loc is not UNSET:
            field_dict["loc"] = loc
        if input_ is not UNSET:
            field_dict["input"] = input_
        if ctx is not UNSET:
            field_dict["ctx"] = ctx

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_error_ctx_type_0 import ProblemErrorCtxType0

        d = dict(src_dict)
        msg = d.pop("msg")

        type_ = d.pop("type")

        def _parse_loc(data: object) -> list[int | str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                loc_type_0 = []
                _loc_type_0 = data
                for loc_type_0_item_data in _loc_type_0:

                    def _parse_loc_type_0_item(data: object) -> int | str:
                        return cast(int | str, data)

                    loc_type_0_item = _parse_loc_type_0_item(loc_type_0_item_data)

                    loc_type_0.append(loc_type_0_item)

                return loc_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[int | str] | None | Unset, data)

        loc = _parse_loc(d.pop("loc", UNSET))

        def _parse_input_(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        input_ = _parse_input_(d.pop("input", UNSET))

        def _parse_ctx(data: object) -> None | ProblemErrorCtxType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ctx_type_0 = ProblemErrorCtxType0.from_dict(data)

                return ctx_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProblemErrorCtxType0 | Unset, data)

        ctx = _parse_ctx(d.pop("ctx", UNSET))

        problem_error = cls(
            msg=msg,
            type_=type_,
            loc=loc,
            input_=input_,
            ctx=ctx,
        )

        problem_error.additional_properties = d
        return problem_error

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
