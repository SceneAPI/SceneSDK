from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_file_ref import ArtifactFileRef
    from ..models.artifact_import_request_metadata import ArtifactImportRequestMetadata
    from ..models.artifact_import_request_producer_type_0 import (
        ArtifactImportRequestProducerType0,
    )
    from ..models.artifact_import_request_summary_type_0 import (
        ArtifactImportRequestSummaryType0,
    )


T = TypeVar("T", bound="ArtifactImportRequest")


@_attrs_define
class ArtifactImportRequest:
    """Register an existing artifact URI as a typed sfmapi artifact.

    Imports do not copy bytes. They create a completed import job/task
    that owns the artifact descriptor so the artifact can be validated,
    converted, and used as a downstream stage input.

        Attributes:
            project_id (str):
            kind (str):
            recon_id (None | str | Unset):
            dataset_id (None | str | Unset):
            name (None | str | Unset):
            uri (None | str | Unset):
            media_type (None | str | Unset):
            artifact_format (None | str | Unset):
            datatype (None | str | Unset):
            schema_version (int | None | Unset):
            files (list[ArtifactFileRef] | Unset):
            sha256 (None | str | Unset):
            byte_size (int | None | Unset):
            coordinate_frame (None | str | Unset):
            producer (ArtifactImportRequestProducerType0 | None | Unset):
            summary (ArtifactImportRequestSummaryType0 | None | Unset):
            metadata (ArtifactImportRequestMetadata | Unset):
    """

    project_id: str
    kind: str
    recon_id: None | str | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    uri: None | str | Unset = UNSET
    media_type: None | str | Unset = UNSET
    artifact_format: None | str | Unset = UNSET
    datatype: None | str | Unset = UNSET
    schema_version: int | None | Unset = UNSET
    files: list[ArtifactFileRef] | Unset = UNSET
    sha256: None | str | Unset = UNSET
    byte_size: int | None | Unset = UNSET
    coordinate_frame: None | str | Unset = UNSET
    producer: ArtifactImportRequestProducerType0 | None | Unset = UNSET
    summary: ArtifactImportRequestSummaryType0 | None | Unset = UNSET
    metadata: ArtifactImportRequestMetadata | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.artifact_import_request_producer_type_0 import (
            ArtifactImportRequestProducerType0,
        )
        from ..models.artifact_import_request_summary_type_0 import (
            ArtifactImportRequestSummaryType0,
        )

        project_id = self.project_id

        kind = self.kind

        recon_id: None | str | Unset
        if isinstance(self.recon_id, Unset):
            recon_id = UNSET
        else:
            recon_id = self.recon_id

        dataset_id: None | str | Unset
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        uri: None | str | Unset
        if isinstance(self.uri, Unset):
            uri = UNSET
        else:
            uri = self.uri

        media_type: None | str | Unset
        if isinstance(self.media_type, Unset):
            media_type = UNSET
        else:
            media_type = self.media_type

        artifact_format: None | str | Unset
        if isinstance(self.artifact_format, Unset):
            artifact_format = UNSET
        else:
            artifact_format = self.artifact_format

        datatype: None | str | Unset
        if isinstance(self.datatype, Unset):
            datatype = UNSET
        else:
            datatype = self.datatype

        schema_version: int | None | Unset
        if isinstance(self.schema_version, Unset):
            schema_version = UNSET
        else:
            schema_version = self.schema_version

        files: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        sha256: None | str | Unset
        if isinstance(self.sha256, Unset):
            sha256 = UNSET
        else:
            sha256 = self.sha256

        byte_size: int | None | Unset
        if isinstance(self.byte_size, Unset):
            byte_size = UNSET
        else:
            byte_size = self.byte_size

        coordinate_frame: None | str | Unset
        if isinstance(self.coordinate_frame, Unset):
            coordinate_frame = UNSET
        else:
            coordinate_frame = self.coordinate_frame

        producer: dict[str, Any] | None | Unset
        if isinstance(self.producer, Unset):
            producer = UNSET
        elif isinstance(self.producer, ArtifactImportRequestProducerType0):
            producer = self.producer.to_dict()
        else:
            producer = self.producer

        summary: dict[str, Any] | None | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        elif isinstance(self.summary, ArtifactImportRequestSummaryType0):
            summary = self.summary.to_dict()
        else:
            summary = self.summary

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "project_id": project_id,
                "kind": kind,
            }
        )
        if recon_id is not UNSET:
            field_dict["recon_id"] = recon_id
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if name is not UNSET:
            field_dict["name"] = name
        if uri is not UNSET:
            field_dict["uri"] = uri
        if media_type is not UNSET:
            field_dict["media_type"] = media_type
        if artifact_format is not UNSET:
            field_dict["artifact_format"] = artifact_format
        if datatype is not UNSET:
            field_dict["datatype"] = datatype
        if schema_version is not UNSET:
            field_dict["schema_version"] = schema_version
        if files is not UNSET:
            field_dict["files"] = files
        if sha256 is not UNSET:
            field_dict["sha256"] = sha256
        if byte_size is not UNSET:
            field_dict["byte_size"] = byte_size
        if coordinate_frame is not UNSET:
            field_dict["coordinate_frame"] = coordinate_frame
        if producer is not UNSET:
            field_dict["producer"] = producer
        if summary is not UNSET:
            field_dict["summary"] = summary
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.artifact_file_ref import ArtifactFileRef
        from ..models.artifact_import_request_metadata import (
            ArtifactImportRequestMetadata,
        )
        from ..models.artifact_import_request_producer_type_0 import (
            ArtifactImportRequestProducerType0,
        )
        from ..models.artifact_import_request_summary_type_0 import (
            ArtifactImportRequestSummaryType0,
        )

        d = dict(src_dict)
        project_id = d.pop("project_id")

        kind = d.pop("kind")

        def _parse_recon_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recon_id = _parse_recon_id(d.pop("recon_id", UNSET))

        def _parse_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_uri(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        uri = _parse_uri(d.pop("uri", UNSET))

        def _parse_media_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        media_type = _parse_media_type(d.pop("media_type", UNSET))

        def _parse_artifact_format(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        artifact_format = _parse_artifact_format(d.pop("artifact_format", UNSET))

        def _parse_datatype(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        datatype = _parse_datatype(d.pop("datatype", UNSET))

        def _parse_schema_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        schema_version = _parse_schema_version(d.pop("schema_version", UNSET))

        _files = d.pop("files", UNSET)
        files: list[ArtifactFileRef] | Unset = UNSET
        if _files is not UNSET:
            files = []
            for files_item_data in _files:
                files_item = ArtifactFileRef.from_dict(files_item_data)

                files.append(files_item)

        def _parse_sha256(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sha256 = _parse_sha256(d.pop("sha256", UNSET))

        def _parse_byte_size(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        byte_size = _parse_byte_size(d.pop("byte_size", UNSET))

        def _parse_coordinate_frame(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        coordinate_frame = _parse_coordinate_frame(d.pop("coordinate_frame", UNSET))

        def _parse_producer(
            data: object,
        ) -> ArtifactImportRequestProducerType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                producer_type_0 = ArtifactImportRequestProducerType0.from_dict(data)

                return producer_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ArtifactImportRequestProducerType0 | None | Unset, data)

        producer = _parse_producer(d.pop("producer", UNSET))

        def _parse_summary(
            data: object,
        ) -> ArtifactImportRequestSummaryType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_0 = ArtifactImportRequestSummaryType0.from_dict(data)

                return summary_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ArtifactImportRequestSummaryType0 | None | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: ArtifactImportRequestMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ArtifactImportRequestMetadata.from_dict(_metadata)

        artifact_import_request = cls(
            project_id=project_id,
            kind=kind,
            recon_id=recon_id,
            dataset_id=dataset_id,
            name=name,
            uri=uri,
            media_type=media_type,
            artifact_format=artifact_format,
            datatype=datatype,
            schema_version=schema_version,
            files=files,
            sha256=sha256,
            byte_size=byte_size,
            coordinate_frame=coordinate_frame,
            producer=producer,
            summary=summary,
            metadata=metadata,
        )

        return artifact_import_request
