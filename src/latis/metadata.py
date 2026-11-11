import pydantic
import xarray as xr

class VariableMetadata(pydantic.BaseModel):
    """
    Class defining variable metadata fields
    """
    model_config = pydantic.ConfigDict(extra="ignore")
    # Required metadata items
    id: str
    type: str
    # Optional metadata items
    units: str | None = None
    missing_value: str | None = pydantic.Field(default=None, alias="missingValue")
    bin_width: str | None = pydantic.Field(default=None, alias="binWidth")
    title: str | None = None
    short_name: str | None = pydantic.Field(default=None, alias="shortName")
    description: str | None = None


class DatasetMetadata(pydantic.BaseModel):
    """
    Class defining dataset metadata fields
    """
    model_config = pydantic.ConfigDict(extra="ignore")
    # Required metadata items
    id: str
    # Optional metadata items
    temporal_coverage: str | None = pydantic.Field(default=None, alias="temporalCoverage")
    variable: list[VariableMetadata]


def apply_metadata(dataset: xr.Dataset, dataset_metadata: DatasetMetadata) -> xr.Dataset:
    # Check if any of the required metadata items are missing
    var_metadata = {var.id: var for var in dataset_metadata.variable}
    missing_metadata_items = set(dataset.data_vars) - set(var_metadata)
    if missing_metadata_items:
        raise pydantic.ValidationError(f"Missing metadata: {missing_metadata_items}")

    dataset = dataset.copy()
    dataset.attrs.update(dataset_metadata.model_dump(exclude={"variable"}, exclude_none=True))  # apply dataset-level metadata
    for variable_name, metadata_item in var_metadata.items():  # apply variable-level metadata
        if variable_name in dataset.variables:
            new_attrs = metadata_item.model_dump(exclude_none=True)
            if dataset[variable_name].dtype.kind in "mM":  # datetime64 and timedelta64 variable datatypes
                # If we add server-provided 'units' or 'calendar' attributes to the time variables (xarray takes them from .encoding), it may break to_netcdf
                new_attrs = {k: v for k, v in new_attrs.items() if k not in {"units", "calendar"}}
            dataset[variable_name].attrs.update(new_attrs)

    return dataset
