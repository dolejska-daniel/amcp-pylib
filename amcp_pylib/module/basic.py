from amcp_pylib.core import Command, command_syntax


@command_syntax('LOADBG [channel:int]{-[layer:int]} [clip:string] {[loop:LOOP]} '
                '{[transition:CUT,MIX,PUSH,WIPE,SLIDE] [duration:int] {[tween:string]|LINEAR} '
                '{[direction:LEFT,RIGHT]|RIGHT}|CUT 0} {SEEK [frame:int]} {LENGTH [frames:int]} '
                '{FILTER [filter:string]} {[auto:AUTO]}')
def LOADBG(command: Command) -> Command:
    """
    Loads a producer in the background and prepares it for playout.
    If no layer is specified the default layer index will be used.
    """
    return command


@command_syntax('LOAD [video_channel:int]{-[layer:int]|-0} [clip:string] {[loop:LOOP]} '
                '{[transition:CUT,MIX,PUSH,WIPE,SLIDE] [duration:int] {[tween:string]|LINEAR} '
                '{[direction:LEFT,RIGHT]|RIGHT}|CUT 0} {SEEK [frame:int]} {LENGTH [frames:int]} '
                '{FILTER [filter:string]} {[auto:AUTO]}')
def LOAD(command: Command) -> Command:
    """
    Loads a clip to the foreground and plays the first frame before pausing.
    If any clip is playing on the target foreground then this clip will be replaced.
    """
    return command


@command_syntax('PLAY [video_channel:int]{-[layer:int]|-0} [clip:string] {[loop:LOOP]} '
                '{[transition:CUT,MIX,PUSH,WIPE,SLIDE] [duration:int] {[tween:string]|LINEAR} '
                '{[direction:LEFT,RIGHT]|RIGHT}|CUT 0} {SEEK [frame:int]} {LENGTH [frames:int]} '
                '{FILTER [filter:string]} {[auto:AUTO]}')
def PLAY(command: Command) -> Command:
    """
    Moves clip from background to foreground and starts playing it.
    If a transition (see LOADBG) is prepared, it will be executed.
    """
    return command


@command_syntax('PLAY [video_channel:int]{-[layer:int]|-0}')
def PAUSE(command: Command) -> Command:
    """
    Pauses playback of the foreground clip on the specified layer.
    The RESUME command can be used to resume playback again.
    """
    return command


@command_syntax('RESUME [video_channel:int]{-[layer:int]|-0}')
def RESUME(command: Command) -> Command:
    """
    Resumes playback of a foreground clip previously paused with the PAUSE command.
    """
    return command


@command_syntax('STOP [video_channel:int]{-[layer:int]|-0}')
def STOP(command: Command) -> Command:
    """
    Removes the foreground clip of the specified layer.
    """
    return command


@command_syntax('CLEAR [video_channel:int]{-[layer:int]}')
def CLEAR(command: Command) -> Command:
    """
    Removes all clips (both foreground and background) of the specified layer.
    If no layer is specified then all layers in the specified video_channel are cleared.
    """
    return command


@command_syntax('CALL [video_channel:int]{-[layer:int]|-0} [param:string]')
def CALL(command: Command) -> Command:
    """
    Calls method on the specified producer with the provided param string.
    """
    return command


@command_syntax('SWAP [channel1:int]{-[layer1:int]} [channel2:int]{-[layer2:int]} {[transforms:TRANSFORMS]}')
def SWAP(command: Command) -> Command:
    """
    Swaps layers between channels (both foreground and background will be swapped).
    """
    return command


@command_syntax('ADD [video_channel:int]{-[consumer_index:int]} [consumer:string] [parameters:string]')
def ADD(command: Command) -> Command:
    """
    Adds a consumer to the specified video channel.
    The string consumer will be parsed by the available consumer factories.
    If a successful match is found a consumer will be created and added to the video_channel.
    """
    return command


@command_syntax('REMOVE [video_channel:int]{-[consumer_index:int]} {[parameters:string]}')
def REMOVE(command: Command) -> Command:
    """
    Removes an existing consumer from video_channel.
    If consumer_index is given, the consumer will be removed via its id.
    If parameters are given instead, the consumer matching those parameters will be removed.
    """
    return command


@command_syntax('PRINT [video_channel:int]')
def PRINT(command: Command) -> Command:
    """
    Saves an RGBA PNG bitmap still image of the contents of the specified channel in the media folder.
    """
    return command


@command_syntax('LOG LEVEL [level:TRACE,DEBUG,INFO,WARNING,ERROR,FATAL]')
def LOG_LEVEL(command: Command) -> Command:
    """
    Changes the log level of the server.
    """
    return command


@command_syntax('LOG CATEGORY [category:CALLTRACE,COMMUNICATION] [enable:0,1]')
def LOG_CATEGORY(command: Command) -> Command:
    """
    Enables or disables the specified logging category.
    """
    return command


@command_syntax('SET [video_channel:int] [variable:string] [value:string]')
def SET(command: Command) -> Command:
    """
    Changes the value of a channel variable. Available variables to set:
        - MODE Changes the video format of the channel.
        - CHANNEL_LAYOUT Changes the audio channel layout of the video channel channel.
    """
    return command


@command_syntax('LOCK [video_channel:int] [action:ACQUIRE,RELEASE,CLEAR] {[lock_phrase:string]}')
def LOCK(command: Command) -> Command:
    """
    Allows for exclusive access to a channel.
    """
    return command
