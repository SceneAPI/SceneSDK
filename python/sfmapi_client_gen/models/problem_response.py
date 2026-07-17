from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.problem_error import ProblemError


T = TypeVar("T", bound="ProblemResponse")


@_attrs_define
class ProblemResponse:
    """RFC 7807 ``application/problem+json`` envelope.

    Carries every key the server may emit (AIP-193). Optional fields:

    - ``errors`` — per-field Pydantic errors on a 422 (see L19);
      each entry has ``loc``, ``msg``, ``type`` and an optional
      ``input``.
    - ``capability`` — canonical capability name on a 501; pair with
      ``GET /v1/capabilities`` to discover what the deployment exposes.
    - ``retry_after`` — seconds to wait before retrying on a 429 / 503.

        Attributes:
            type_ (str):
            title (str):
            status (int):
            detail (None | str | Unset):
            instance (None | str | Unset):
            errors (list[ProblemError] | None | Unset):
            capability (None | str | Unset):
            retry_after (int | None | Unset):
    """

    type_: str
    title: str
    status: int
    detail: None | str | Unset = UNSET
    instance: None | str | Unset = UNSET
    errors: list[ProblemError] | None | Unset = UNSET
    capability: None | str | Unset = UNSET
    retry_after: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        title = self.title

        status = self.status

        detail: None | str | Unset
        if isinstance(self.detail, Unset):
            detail = UNSET
        else:
            detail = self.detail

        instance: None | str | Unset
        if isinstance(self.instance, Unset):
            instance = UNSET
        else:
            instance = self.instance

        errors: list[dict[str, Any]] | None | Unset
        if isinstance(self.errors, Unset):
            errors = UNSET
        elif isinstance(self.errors, list):
            errors = []
            for errors_type_0_item_data in self.errors:
                errors_type_0_item = errors_type_0_item_data.to_dict()
                errors.append(errors_type_0_item)

        else:
            errors = self.errors

        capability: None | str | Unset
        if isinstance(self.capability, Unset):
            capability = UNSET
        else:
            capability = self.capability

        retry_after: int | None | Unset
        if isinstance(self.retry_after, Unset):
            retry_after = UNSET
        else:
            retry_after = self.retry_after

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "title": title,
                "status": status,
            }
        )
        if detail is not UNSET:
            field_dict["detail"] = detail
        if instance is not UNSET:
            field_dict["instance"] = instance
        if errors is not UNSET:
            field_dict["errors"] = errors
        if capability is not UNSET:
            field_dict["capability"] = capability
        if retry_after is not UNSET:
            field_dict["retry_after"] = retry_after

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_error import ProblemError

        d = dict(src_dict)
        type_ = d.pop("type")

        title = d.pop("title")

        status = d.pop("status")

        def _parse_detail(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        detail = _parse_detail(d.pop("detail", UNSET))

        def _parse_instance(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        instance = _parse_instance(d.pop("instance", UNSET))

        def _parse_errors(data: object) -> list[ProblemError] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                errors_type_0 = []
                _errors_type_0 = data
                for errors_type_0_item_data in _errors_type_0:
                    errors_type_0_item = ProblemError.from_dict(errors_type_0_item_data)

                    errors_type_0.append(errors_type_0_item)

                return errors_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ProblemError] | None | Unset, data)

        errors = _parse_errors(d.pop("errors", UNSET))

        def _parse_capability(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        capability = _parse_capability(d.pop("capability", UNSET))

        def _parse_retry_after(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        retry_after = _parse_retry_after(d.pop("retry_after", UNSET))

        problem_response = cls(
            type_=type_,
            title=title,
            status=status,
            detail=detail,
            instance=instance,
            errors=errors,
            capability=capability,
            retry_after=retry_after,
        )

        problem_response.additional_properties = d
        return problem_response

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
