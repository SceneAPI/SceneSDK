from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

from ..models.plugin_manifest_trust_tier import PluginManifestTrustTier
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compatibility import Compatibility
    from ..models.conformance import Conformance
    from ..models.license_info import LicenseInfo
    from ..models.plugin_data_type_manifest import PluginDataTypeManifest
    from ..models.plugin_dependency_manifest import PluginDependencyManifest
    from ..models.plugin_pipeline_manifest import PluginPipelineManifest
    from ..models.plugin_processor_extension_manifest import (
        PluginProcessorExtensionManifest,
    )
    from ..models.plugin_processor_manifest import PluginProcessorManifest
    from ..models.provider_manifest import ProviderManifest
    from ..models.runtime_modes import RuntimeModes
    from ..models.upstream_project import UpstreamProject


T = TypeVar("T", bound="PluginManifest")


@_attrs_define
class PluginManifest:
    """
    Attributes:
        plugin_id (str):
        display_name (str):
        description (str):
        package_name (str):
        github_url (str):
        entry_points (list[str]):
        providers (list[ProviderManifest]):
        runtime_modes (RuntimeModes):
        schema_version (Literal[1] | Unset):  Default: 1.
        capabilities (list[str] | Unset):
        backend_actions (list[str] | Unset):
        config_schemas (list[str] | Unset):
        artifact_contracts (list[str] | Unset):
        datatypes (list[PluginDataTypeManifest] | Unset):
        processors (list[PluginProcessorManifest] | Unset):
        pipelines (list[PluginPipelineManifest] | Unset):
        processor_extensions (list[PluginProcessorExtensionManifest] | Unset):
        plugin_dependencies (list[PluginDependencyManifest] | Unset):
        licenses (list[LicenseInfo] | Unset):
        upstream_projects (list[UpstreamProject] | Unset):
        compatibility (Compatibility | Unset):
        conformance (Conformance | Unset):
        trust_tier (PluginManifestTrustTier | Unset):  Default: PluginManifestTrustTier.COMMUNITY.
    """

    plugin_id: str
    display_name: str
    description: str
    package_name: str
    github_url: str
    entry_points: list[str]
    providers: list[ProviderManifest]
    runtime_modes: RuntimeModes
    schema_version: Literal[1] | Unset = 1
    capabilities: list[str] | Unset = UNSET
    backend_actions: list[str] | Unset = UNSET
    config_schemas: list[str] | Unset = UNSET
    artifact_contracts: list[str] | Unset = UNSET
    datatypes: list[PluginDataTypeManifest] | Unset = UNSET
    processors: list[PluginProcessorManifest] | Unset = UNSET
    pipelines: list[PluginPipelineManifest] | Unset = UNSET
    processor_extensions: list[PluginProcessorExtensionManifest] | Unset = UNSET
    plugin_dependencies: list[PluginDependencyManifest] | Unset = UNSET
    licenses: list[LicenseInfo] | Unset = UNSET
    upstream_projects: list[UpstreamProject] | Unset = UNSET
    compatibility: Compatibility | Unset = UNSET
    conformance: Conformance | Unset = UNSET
    trust_tier: PluginManifestTrustTier | Unset = PluginManifestTrustTier.COMMUNITY

    def to_dict(self) -> dict[str, Any]:
        plugin_id = self.plugin_id

        display_name = self.display_name

        description = self.description

        package_name = self.package_name

        github_url = self.github_url

        entry_points = self.entry_points

        providers = []
        for providers_item_data in self.providers:
            providers_item = providers_item_data.to_dict()
            providers.append(providers_item)

        runtime_modes = self.runtime_modes.to_dict()

        schema_version = self.schema_version

        capabilities: list[str] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities

        backend_actions: list[str] | Unset = UNSET
        if not isinstance(self.backend_actions, Unset):
            backend_actions = self.backend_actions

        config_schemas: list[str] | Unset = UNSET
        if not isinstance(self.config_schemas, Unset):
            config_schemas = self.config_schemas

        artifact_contracts: list[str] | Unset = UNSET
        if not isinstance(self.artifact_contracts, Unset):
            artifact_contracts = self.artifact_contracts

        datatypes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.datatypes, Unset):
            datatypes = []
            for datatypes_item_data in self.datatypes:
                datatypes_item = datatypes_item_data.to_dict()
                datatypes.append(datatypes_item)

        processors: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.processors, Unset):
            processors = []
            for processors_item_data in self.processors:
                processors_item = processors_item_data.to_dict()
                processors.append(processors_item)

        pipelines: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.pipelines, Unset):
            pipelines = []
            for pipelines_item_data in self.pipelines:
                pipelines_item = pipelines_item_data.to_dict()
                pipelines.append(pipelines_item)

        processor_extensions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.processor_extensions, Unset):
            processor_extensions = []
            for processor_extensions_item_data in self.processor_extensions:
                processor_extensions_item = processor_extensions_item_data.to_dict()
                processor_extensions.append(processor_extensions_item)

        plugin_dependencies: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.plugin_dependencies, Unset):
            plugin_dependencies = []
            for plugin_dependencies_item_data in self.plugin_dependencies:
                plugin_dependencies_item = plugin_dependencies_item_data.to_dict()
                plugin_dependencies.append(plugin_dependencies_item)

        licenses: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.licenses, Unset):
            licenses = []
            for licenses_item_data in self.licenses:
                licenses_item = licenses_item_data.to_dict()
                licenses.append(licenses_item)

        upstream_projects: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.upstream_projects, Unset):
            upstream_projects = []
            for upstream_projects_item_data in self.upstream_projects:
                upstream_projects_item = upstream_projects_item_data.to_dict()
                upstream_projects.append(upstream_projects_item)

        compatibility: dict[str, Any] | Unset = UNSET
        if not isinstance(self.compatibility, Unset):
            compatibility = self.compatibility.to_dict()

        conformance: dict[str, Any] | Unset = UNSET
        if not isinstance(self.conformance, Unset):
            conformance = self.conformance.to_dict()

        trust_tier: str | Unset = UNSET
        if not isinstance(self.trust_tier, Unset):
            trust_tier = self.trust_tier.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "plugin_id": plugin_id,
                "display_name": display_name,
                "description": description,
                "package_name": package_name,
                "github_url": github_url,
                "entry_points": entry_points,
                "providers": providers,
                "runtime_modes": runtime_modes,
            }
        )
        if schema_version is not UNSET:
            field_dict["schema_version"] = schema_version
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if backend_actions is not UNSET:
            field_dict["backend_actions"] = backend_actions
        if config_schemas is not UNSET:
            field_dict["config_schemas"] = config_schemas
        if artifact_contracts is not UNSET:
            field_dict["artifact_contracts"] = artifact_contracts
        if datatypes is not UNSET:
            field_dict["datatypes"] = datatypes
        if processors is not UNSET:
            field_dict["processors"] = processors
        if pipelines is not UNSET:
            field_dict["pipelines"] = pipelines
        if processor_extensions is not UNSET:
            field_dict["processor_extensions"] = processor_extensions
        if plugin_dependencies is not UNSET:
            field_dict["plugin_dependencies"] = plugin_dependencies
        if licenses is not UNSET:
            field_dict["licenses"] = licenses
        if upstream_projects is not UNSET:
            field_dict["upstream_projects"] = upstream_projects
        if compatibility is not UNSET:
            field_dict["compatibility"] = compatibility
        if conformance is not UNSET:
            field_dict["conformance"] = conformance
        if trust_tier is not UNSET:
            field_dict["trust_tier"] = trust_tier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compatibility import Compatibility
        from ..models.conformance import Conformance
        from ..models.license_info import LicenseInfo
        from ..models.plugin_data_type_manifest import PluginDataTypeManifest
        from ..models.plugin_dependency_manifest import PluginDependencyManifest
        from ..models.plugin_pipeline_manifest import PluginPipelineManifest
        from ..models.plugin_processor_extension_manifest import (
            PluginProcessorExtensionManifest,
        )
        from ..models.plugin_processor_manifest import PluginProcessorManifest
        from ..models.provider_manifest import ProviderManifest
        from ..models.runtime_modes import RuntimeModes
        from ..models.upstream_project import UpstreamProject

        d = dict(src_dict)
        plugin_id = d.pop("plugin_id")

        display_name = d.pop("display_name")

        description = d.pop("description")

        package_name = d.pop("package_name")

        github_url = d.pop("github_url")

        entry_points = cast(list[str], d.pop("entry_points"))

        providers = []
        _providers = d.pop("providers")
        for providers_item_data in _providers:
            providers_item = ProviderManifest.from_dict(providers_item_data)

            providers.append(providers_item)

        runtime_modes = RuntimeModes.from_dict(d.pop("runtime_modes"))

        schema_version = cast(Literal[1] | Unset, d.pop("schema_version", UNSET))
        if schema_version != 1 and not isinstance(schema_version, Unset):
            raise ValueError(
                f"schema_version must match const 1, got '{schema_version}'"
            )

        capabilities = cast(list[str], d.pop("capabilities", UNSET))

        backend_actions = cast(list[str], d.pop("backend_actions", UNSET))

        config_schemas = cast(list[str], d.pop("config_schemas", UNSET))

        artifact_contracts = cast(list[str], d.pop("artifact_contracts", UNSET))

        _datatypes = d.pop("datatypes", UNSET)
        datatypes: list[PluginDataTypeManifest] | Unset = UNSET
        if _datatypes is not UNSET:
            datatypes = []
            for datatypes_item_data in _datatypes:
                datatypes_item = PluginDataTypeManifest.from_dict(datatypes_item_data)

                datatypes.append(datatypes_item)

        _processors = d.pop("processors", UNSET)
        processors: list[PluginProcessorManifest] | Unset = UNSET
        if _processors is not UNSET:
            processors = []
            for processors_item_data in _processors:
                processors_item = PluginProcessorManifest.from_dict(
                    processors_item_data
                )

                processors.append(processors_item)

        _pipelines = d.pop("pipelines", UNSET)
        pipelines: list[PluginPipelineManifest] | Unset = UNSET
        if _pipelines is not UNSET:
            pipelines = []
            for pipelines_item_data in _pipelines:
                pipelines_item = PluginPipelineManifest.from_dict(pipelines_item_data)

                pipelines.append(pipelines_item)

        _processor_extensions = d.pop("processor_extensions", UNSET)
        processor_extensions: list[PluginProcessorExtensionManifest] | Unset = UNSET
        if _processor_extensions is not UNSET:
            processor_extensions = []
            for processor_extensions_item_data in _processor_extensions:
                processor_extensions_item = PluginProcessorExtensionManifest.from_dict(
                    processor_extensions_item_data
                )

                processor_extensions.append(processor_extensions_item)

        _plugin_dependencies = d.pop("plugin_dependencies", UNSET)
        plugin_dependencies: list[PluginDependencyManifest] | Unset = UNSET
        if _plugin_dependencies is not UNSET:
            plugin_dependencies = []
            for plugin_dependencies_item_data in _plugin_dependencies:
                plugin_dependencies_item = PluginDependencyManifest.from_dict(
                    plugin_dependencies_item_data
                )

                plugin_dependencies.append(plugin_dependencies_item)

        _licenses = d.pop("licenses", UNSET)
        licenses: list[LicenseInfo] | Unset = UNSET
        if _licenses is not UNSET:
            licenses = []
            for licenses_item_data in _licenses:
                licenses_item = LicenseInfo.from_dict(licenses_item_data)

                licenses.append(licenses_item)

        _upstream_projects = d.pop("upstream_projects", UNSET)
        upstream_projects: list[UpstreamProject] | Unset = UNSET
        if _upstream_projects is not UNSET:
            upstream_projects = []
            for upstream_projects_item_data in _upstream_projects:
                upstream_projects_item = UpstreamProject.from_dict(
                    upstream_projects_item_data
                )

                upstream_projects.append(upstream_projects_item)

        _compatibility = d.pop("compatibility", UNSET)
        compatibility: Compatibility | Unset
        if isinstance(_compatibility, Unset):
            compatibility = UNSET
        else:
            compatibility = Compatibility.from_dict(_compatibility)

        _conformance = d.pop("conformance", UNSET)
        conformance: Conformance | Unset
        if isinstance(_conformance, Unset):
            conformance = UNSET
        else:
            conformance = Conformance.from_dict(_conformance)

        _trust_tier = d.pop("trust_tier", UNSET)
        trust_tier: PluginManifestTrustTier | Unset
        if isinstance(_trust_tier, Unset):
            trust_tier = UNSET
        else:
            trust_tier = PluginManifestTrustTier(_trust_tier)

        plugin_manifest = cls(
            plugin_id=plugin_id,
            display_name=display_name,
            description=description,
            package_name=package_name,
            github_url=github_url,
            entry_points=entry_points,
            providers=providers,
            runtime_modes=runtime_modes,
            schema_version=schema_version,
            capabilities=capabilities,
            backend_actions=backend_actions,
            config_schemas=config_schemas,
            artifact_contracts=artifact_contracts,
            datatypes=datatypes,
            processors=processors,
            pipelines=pipelines,
            processor_extensions=processor_extensions,
            plugin_dependencies=plugin_dependencies,
            licenses=licenses,
            upstream_projects=upstream_projects,
            compatibility=compatibility,
            conformance=conformance,
            trust_tier=trust_tier,
        )

        return plugin_manifest
