from amcp_pylib.core import Command, command_syntax


@command_syntax('THUMBNAIL LIST {[sub_directory:string]}')
def THUMBNAIL_LIST(command: Command) -> Command:
    """
    Lists thumbnails.
    If the optional sub_directory is specified only the thumbnails in that sub directory will be returned.
    """
    return command


@command_syntax('THUMBNAIL RETRIEVE [filename:string]')
def THUMBNAIL_RETRIEVE(command: Command) -> Command:
    """
    Retrieves a thumbnail as a base64 encoded PNG-image.
    """
    return command


@command_syntax('THUMBNAIL GENERATE [filename:string]')
def THUMBNAIL_GENERATE(command: Command) -> Command:
    """
    Regenerates a thumbnail.
    """
    return command


@command_syntax('THUMBNAIL GENERATE_ALL')
def THUMBNAIL_GENERATE_ALL(command: Command) -> Command:
    """
    Regenerates all thumbnails.
    """
    return command
