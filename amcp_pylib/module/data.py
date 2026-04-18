from typing import Optional

from amcp_pylib.core import Command, command_syntax


@command_syntax('DATA STORE [name:string] [data:string]')
def DATA_STORE(
    *,
    name: str,
    data: str,
    request_id: Optional[str] = None,
) -> Command:
    """
    Stores the dataset data under the name name.
    Directories will be created if they do not exist.

    Args:
        name: Dataset name (may include path separators to create sub-directories).
        data: Dataset content to store as an XML string in the CasparCG
            ``<templateData>`` format.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('DATA RETRIEVE [name:string]')
def DATA_RETRIEVE(
    *,
    name: str,
    request_id: Optional[str] = None,
) -> Command:
    """
    Returns the data saved under the name name.

    Args:
        name: Name of the dataset to retrieve.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('DATA LIST {[sub_directory:string]}')
def DATA_LIST(
    *,
    sub_directory: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Returns a list of stored datasets.
    If the optional sub_directory is specified only the datasets in that sub directory will be returned.

    Args:
        sub_directory: Sub-directory path to restrict the listing to.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('DATA REMOVE [name:string]')
def DATA_REMOVE(
    *,
    name: str,
    request_id: Optional[str] = None,
) -> Command:
    """
    Removes the dataset saved under the name name.

    Args:
        name: Name of the dataset to remove.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...
