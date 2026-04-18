from typing import Optional

from amcp_pylib.core import Command, command_syntax


@command_syntax('THUMBNAIL LIST {[sub_directory:string]}')
def THUMBNAIL_LIST(
    *,
    sub_directory: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Lists thumbnails in the thumbnail folder.
    If the optional sub_directory is specified only the thumbnails in that sub directory will be returned.

    Args:
        sub_directory: Sub-directory path to restrict the listing to.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('THUMBNAIL RETRIEVE [filename:string]')
def THUMBNAIL_RETRIEVE(
    *,
    filename: str,
    request_id: Optional[str] = None,
) -> Command:
    """
    Retrieves a thumbnail as a base64 encoded PNG-image.

    Args:
        filename: Media file name whose thumbnail to retrieve (relative to the media folder).
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('THUMBNAIL GENERATE [filename:string]')
def THUMBNAIL_GENERATE(
    *,
    filename: str,
    request_id: Optional[str] = None,
) -> Command:
    """
    Regenerates the thumbnail for a specific media file.

    Args:
        filename: Media file name whose thumbnail to regenerate (relative to the media folder).
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('THUMBNAIL GENERATE_ALL')
def THUMBNAIL_GENERATE_ALL(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Regenerates all thumbnails in the thumbnail folder.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...
