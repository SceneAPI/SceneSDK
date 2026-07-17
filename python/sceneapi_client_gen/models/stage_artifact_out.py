from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_file_ref import ArtifactFileRef
    from ..models.stage_artifact_out_links_type_0 import StageArtifactOutLinksType0
    from ..models.stage_artifact_out_metadata_type_0 import (
        StageArtifactOutMetadataType0,
    )
    from ..models.stage_artifact_out_producer_type_0 import (
        StageArtifactOutProducerType0,
    )
    from ..models.stage_artifact_out_summary_type_0 import StageArtifactOutSummaryType0


T = TypeVar("T", bound="StageArtifactOut")


@_attrs_define
class StageArtifactOut:
    """A typed worker output persisted independently of task logs.

    Unknown backends can emit multiple artifacts per stage. The API
    stores them here so clients can list and select exact outputs
    instead of guessing from the latest task dictionary.

        Attributes:
            artifact_id (str):
            job_id (str):
            task_id (str):
            kind (str):
            created_at (datetime.datetime):
            field_links (None | StageArtifactOutLinksType0 | Unset):
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
            producer (None | StageArtifactOutProducerType0 | Unset):
            summary (None | StageArtifactOutSummaryType0 | Unset):
            metadata (None | StageArtifactOutMetadataType0 | Unset):
    """

    artifact_id: str
    job_id: str
    task_id: str
    kind: str
    created_at: datetime.datetime
    field_links: None | StageArtifactOutLinksType0 | Unset = UNSET
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
    producer: None | StageArtifactOutProducerType0 | Unset = UNSET
    summary: None | StageArtifactOutSummaryType0 | Unset = UNSET
    metadata: None | StageArtifactOutMetadataType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.stage_artifact_out_links_type_0 import StageArtifactOutLinksType0
        from ..models.stage_artifact_out_metadata_type_0 import (
            StageArtifactOutMetadataType0,
        )
        from ..models.stage_artifact_out_producer_type_0 import (
            StageArtifactOutProducerType0,
        )
        from ..models.stage_artifact_out_summary_type_0 import (
            StageArtifactOutSummaryType0,
        )

        artifact_id = self.artifact_id

        job_id = self.job_id

        task_id = self.task_id

        kind = self.kind

        created_at = self.created_at.isoformat()

        field_links: dict[str, Any] | None | Unset
        if isinstance(self.field_links, Unset):
            field_links = UNSET
        elif isinstance(self.field_links, StageArtifactOutLinksType0):
            field_links = self.field_links.to_dict()
        else:
            field_links = self.field_links

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
        elif isinstance(self.producer, StageArtifactOutProducerType0):
            producer = self.producer.to_dict()
        else:
            producer = self.producer

        summary: dict[str, Any] | None | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        elif isinstance(self.summary, StageArtifactOutSummaryType0):
            summary = self.summary.to_dict()
        else:
            summary = self.summary

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, StageArtifactOutMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "artifact_id": artifact_id,
                "job_id": job_id,
                "task_id": task_id,
                "kind": kind,
                "created_at": created_at,
            }
        )
        if field_links is not UNSET:
            field_dict["_links"] = field_links
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
        from ..models.stage_artifact_out_links_type_0 import StageArtifactOutLinksType0
        from ..models.stage_artifact_out_metadata_type_0 import (
            StageArtifactOutMetadataType0,
        )
        from ..models.stage_artifact_out_producer_type_0 import (
            StageArtifactOutProducerType0,
        )
        from ..models.stage_artifact_out_summary_type_0 import (
            StageArtifactOutSummaryType0,
        )

        d = dict(src_dict)
        artifact_id = d.pop("artifact_id")

        job_id = d.pop("job_id")

        task_id = d.pop("task_id")

        kind = d.pop("kind")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_field_links(
            data: object,
        ) -> None | StageArtifactOutLinksType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                field_links_type_0 = StageArtifactOutLinksType0.from_dict(data)

                return field_links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StageArtifactOutLinksType0 | Unset, data)

        field_links = _parse_field_links(d.pop("_links", UNSET))

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
        ) -> None | StageArtifactOutProducerType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                producer_type_0 = StageArtifactOutProducerType0.from_dict(data)

                return producer_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StageArtifactOutProducerType0 | Unset, data)

        producer = _parse_producer(d.pop("producer", UNSET))

        def _parse_summary(data: object) -> None | StageArtifactOutSummaryType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_0 = StageArtifactOutSummaryType0.from_dict(data)

                return summary_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StageArtifactOutSummaryType0 | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        def _parse_metadata(
            data: object,
        ) -> None | StageArtifactOutMetadataType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = StageArtifactOutMetadataType0.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StageArtifactOutMetadataType0 | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        stage_artifact_out = cls(
            artifact_id=artifact_id,
            job_id=job_id,
            task_id=task_id,
            kind=kind,
            created_at=created_at,
            field_links=field_links,
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

        stage_artifact_out.additional_properties = d
        return stage_artifact_out

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
