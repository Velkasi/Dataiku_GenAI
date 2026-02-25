"""Package api - Accès à Dataiku DSS."""

from .client import get_client, get_project, get_config
from .projects import list_projects, get_project_summary, list_datasets
from .datasets import get_dataset_as_dataframe, push_dataframe_to_dataset, get_dataset_schema

__all__ = [
    "get_client",
    "get_project",
    "get_config",
    "list_projects",
    "get_project_summary",
    "list_datasets",
    "get_dataset_as_dataframe",
    "push_dataframe_to_dataset",
    "get_dataset_schema",
]
