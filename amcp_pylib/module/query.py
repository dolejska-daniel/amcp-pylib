from typing import Optional

from amcp_pylib.core import Command, command_syntax


@command_syntax('CINF [filename:string]')
def CINF(
    *,
    filename: str,
    request_id: Optional[str] = None,
) -> Command:
    """
    Returns information about a media file:
        - Filename
        - Type (STILL / MOVIE / AUDIO)
        - File size in bytes
        - Last modified timestamp
        - Frame count
        - Frame rate / duration

    If a file with the same name exists in multiple directories, all of them are returned.

    Args:
        filename: Media file name (relative to the media folder, without extension).
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CLS {[sub_directory:string]}')
def CLS(
    *,
    sub_directory: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Lists media files in the media folder. Use the command INFO PATHS to get the path to the media folder.
    If the optional sub_directory is specified only the media files in that sub directory will be returned.

    Args:
        sub_directory: Sub-directory path to restrict the listing to.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('FLS')
def FLS(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Lists all font files in the fonts folder. Use the command INFO PATHS to get the path to the fonts folder.
    Columns in order from left to right are: Font name and font path.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('TLS {[sub_directory:string]}')
def TLS(
    *,
    sub_directory: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Lists template files in the templates folder.
    Use the command INFO PATHS to get the path to the templates folder.
    If the optional sub_directory is specified only the template files in that sub directory will be returned.

    Args:
        sub_directory: Sub-directory path to restrict the listing to.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('VERSION {[component:string]}')
def VERSION(
    *,
    component: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Returns the version of the specified server component.
    Returns the server version if no component is specified.

    Args:
        component: Component name to query (e.g. SERVER, FLASH, TEMPLATEHOST, IMAGE).
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('INFO [video_channel:int]{-[layer:int]}')
def INFO(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Get information about a channel or a specific layer on a channel.
    If layer is omitted, information about the whole channel is returned.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Returns channel-level info if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('INFO')
def INFO_CHANNELS(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Retrieves a list of the available channels.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('INFO TEMPLATE [template:string]')
def INFO_TEMPLATE(
    *,
    template: str,
    request_id: Optional[str] = None,
) -> Command:
    """
    Gets information about the specified template.

    Args:
        template: Template file name (relative to the templates folder, without extension).
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('INFO CONFIG')
def INFO_CONFIG(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Gets the contents of the configuration used.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('INFO PATHS')
def INFO_PATHS(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Gets information about the paths used by the server (media, templates, data, log, etc.).

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('INFO SYSTEM')
def INFO_SYSTEM(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Gets system information like OS, CPU and library version numbers.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('INFO SERVER')
def INFO_SERVER(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Gets detailed information about all channels.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('INFO QUEUES')
def INFO_QUEUES(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Gets detailed information about all AMCP Command Queues.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('INFO THREADS')
def INFO_THREADS(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Lists all known threads in the server.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('INFO [video_channel:int]{-[layer:int]} DELAY')
def INFO_DELAY(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Gets the current delay on the specified channel or layer.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Returns channel-level delay if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('DIAG')
def DIAG(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Opens the Diagnostics Window on the server.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('GL INFO')
def GL_INFO(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Retrieves information about the allocated and pooled OpenGL resources.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('GL GC')
def GL_GC(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Releases all the pooled OpenGL resources. May cause a pause on all video channels.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('OSC SUBSCRIBE [port:int]')
def OSC_SUBSCRIBE(
    *,
    port: int,
    request_id: Optional[str] = None,
) -> Command:
    """
    Subscribes this AMCP client's IP address to OSC updates on the given UDP port.
    Introduced by CasparCG Server 2.4.

    Args:
        port: UDP port number to receive OSC messages on.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('OSC UNSUBSCRIBE [port:int]')
def OSC_UNSUBSCRIBE(
    *,
    port: int,
    request_id: Optional[str] = None,
) -> Command:
    """
    Removes this AMCP client's lifecycle-bound OSC subscription for the given UDP port.

    Args:
        port: UDP port number of the OSC subscription to remove.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('BYE')
def BYE(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Disconnects from the server if connected remotely.
    If interacting directly with the console on the machine CasparCG is running on,
    this will achieve the same as the KILL command.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('KILL')
def KILL(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Shuts the server down.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('RESTART')
def RESTART(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Shuts the server down, but exits with return code 5 instead of 0.
    Intended for use in combination with casparcg_auto_restart.bat.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('HELP {[command:string]}')
def HELP(
    *,
    command: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Shows online help for a specific command or a list of all commands.

    Args:
        command: Command name to show help for. Lists all commands if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('HELP PRODUCER {[producer:string]}')
def HELP_PRODUCER(
    *,
    producer: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Shows online help for a specific producer or a list of all producers.

    Args:
        producer: Producer name to show help for. Lists all producers if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('HELP CONSUMER {[consumer:string]}')
def HELP_CONSUMER(
    *,
    consumer: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Shows online help for a specific consumer or a list of all consumers.

    Args:
        consumer: Consumer name to show help for. Lists all consumers if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('BEGIN')
def BEGIN(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Starts a server-side AMCP command batch. Use COMMIT or DISCARD to finish it.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('COMMIT')
def COMMIT(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Executes the commands queued after BEGIN as a batch.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('DISCARD')
def DISCARD(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Discards the commands queued after BEGIN.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...
