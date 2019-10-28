from amcp_pylib.core import Command, command_syntax


@command_syntax('CINF [filename:string]')
def CINF(command: Command) -> Command:
    """
    Returns information about a media file.
        - Filename
        - Type [STILL/MOVIE/AUDIO]
        - Filesize (Bytes)
        - Last Modified
        - Frame count
        - Frame rate/duration

    If a file with the same name exist in multiple directories, all of them are returned.
    """
    return command


@command_syntax('CLS {[sub_directory:string]}')
def CLS(command: Command) -> Command:
    """
    Lists media files in the media folder. Use the command INFO PATHS to get the path to the media folder.
    If the optional sub_directory is specified only the media files in that sub directory will be returned.
    """
    return command


@command_syntax('FLS')
def FLS(command: Command) -> Command:
    """
    Lists all font files in the fonts folder. Use the command INFO PATHS to get the path to the fonts folder.
    Columns in order from left to right are: Font name and font path.
    """
    return command


@command_syntax('TLS {[sub_directory:string]}')
def TLS(command: Command) -> Command:
    """
    Lists template files in the templates folder. Use the command INFO PATHS to get the path to the templates folder.
    If the optional sub_directory is specified only the template files in that sub directory will be returned.
    """
    return command


@command_syntax('VERSION {[component:string]}')
def VERSION(command: Command) -> Command:
    """
    Returns the version of specified component.
    """
    return command


@command_syntax('INFO [video_channel:int]{-[layer:int]}')
def INFO(command: Command) -> Command:
    """
    Get information about a channel or a specific layer on a channel.
    If layer is ommitted information about the whole channel is returned.
    """
    return command


@command_syntax('INFO')
def INFO_CHANNELS(command: Command) -> Command:
    """
    Retrieves a list of the available channels.
    """
    return command


@command_syntax('INFO TEMPLATE [template:string]')
def INFO_TEMPLATE(command: Command) -> Command:
    """
    Gets information about the specified template.
    """
    return command


@command_syntax('INFO CONFIG')
def INFO_CONFIG(command: Command) -> Command:
    """
    Gets the contents of the configuration used.
    """
    return command


@command_syntax('INFO PATHS')
def INFO_PATHS(command: Command) -> Command:
    """
    Gets information about the paths used.
    """
    return command


@command_syntax('INFO SYSTEM')
def INFO_SYSTEM(command: Command) -> Command:
    """
    Gets system information like OS, CPU and library version numbers.
    """
    return command


@command_syntax('INFO SERVER')
def INFO_SERVER(command: Command) -> Command:
    """
    Gets detailed information about all channels.
    """
    return command


@command_syntax('INFO QUEUES')
def INFO_QUEUES(command: Command) -> Command:
    """
    Gets detailed information about all AMCP Command Queues.
    """
    return command


@command_syntax('INFO THREADS')
def INFO_THREADS(command: Command) -> Command:
    """
    Lists all known threads in the server.
    """
    return command


@command_syntax('INFO [video_channel:int]{-[layer:int]} DELAY')
def INFO_DELAY(command: Command) -> Command:
    """
    Gets the current delay on the specified channel or layer.
    """
    return command


@command_syntax('DIAG')
def DIAG(command: Command) -> Command:
    """
    Opens the Diagnostics Window.
    """
    return command


@command_syntax('GL INFO')
def GL_INFO(command: Command) -> Command:
    """
    Retrieves information about the allocated and pooled OpenGL resources.
    """
    return command


@command_syntax('GL GC')
def GL_GC(command: Command) -> Command:
    """
    Releases all the pooled OpenGL resources. May cause a pause on all video channels.
    """
    return command


@command_syntax('BYE')
def BYE(command: Command) -> Command:
    """
    Disconnects from the server if connected remotely,
    if interacting directly with the console on the machine Caspar is running on
    then this will achieve the same as the KILL command.
    """
    return command


@command_syntax('KILL')
def KILL(command: Command) -> Command:
    """
    Shuts the server down.
    """
    return command


@command_syntax('RESTART')
def RESTART(command: Command) -> Command:
    """
    Shuts the server down, but exits with return code 5 instead of 0.
    Intended for use in combination with casparcg_auto_restart.bat.
    """
    return command


@command_syntax('HELP {[command:string]}')
def HELP(command: Command) -> Command:
    """
    Shows online help for a specific command or a list of all commands.
    """
    return command


@command_syntax('HELP PRODUCER {[producer:string]}')
def HELP_PRODUCER(command: Command) -> Command:
    """
    Shows online help for a specific producer or a list of all producers.
    """
    return command


@command_syntax('HELP CONSUMER {[consumer:string]}')
def HELP_CONSUMER(command: Command) -> Command:
    """
    Shows online help for a specific consumer or a list of all consumers.
    """
    return command
