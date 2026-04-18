from typing import Any, Literal, Optional

from amcp_pylib.core import Command, command_syntax


@command_syntax('LOADBG [channel:int]{-[layer:int]} [clip:string] {[loop:LOOP]} '
                '{[transition:CUT,MIX,PUSH,WIPE,SLIDE,STING] [duration:int] {[tween:string]} '
                '{[direction:LEFT,RIGHT]}} {SEEK [frame:int]} {LENGTH [frames:int]} '
                '{FILTER [filter:string]} {[auto:AUTO]} {[clear_on_404:CLEAR_ON_404]} {[parameters:raw]}')
def LOADBG(
    *,
    channel: int,
    clip: str,
    layer: Optional[int] = None,
    loop: Optional[Literal["LOOP"]] = None,
    transition: Optional[Literal["CUT", "MIX", "PUSH", "WIPE", "SLIDE", "STING"]] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    direction: Optional[Literal["LEFT", "RIGHT"]] = None,
    frame: Optional[int] = None,
    frames: Optional[int] = None,
    filter: Optional[str] = None,
    auto: Optional[Literal["AUTO"]] = None,
    clear_on_404: Optional[Literal["CLEAR_ON_404"]] = None,
    parameters: Any = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Loads a producer in the background and prepares it for playout.
    If no layer is specified the default layer index will be used.

    Args:
        channel: Video channel index.
        clip: Path to the media clip to load.
        layer: Layer index. Uses default layer if omitted.
        loop: Pass "LOOP" to loop the clip indefinitely.
        transition: Transition type to use when switching to foreground
            (CUT, MIX, PUSH, WIPE, SLIDE, or STING).
        duration: Transition duration in frames.
        tween: Tween/easing function name for the transition animation.
        direction: Transition direction ("LEFT" or "RIGHT").
        frame: Frame position to seek to before playback begins.
        frames: Maximum number of frames to play (clip length limit).
        filter: FFmpeg filter graph string to apply to the clip.
        auto: Pass "AUTO" to automatically transition the clip to foreground when it is ready.
        clear_on_404: Pass "CLEAR_ON_404" to clear the layer if the clip file is not found.
        parameters: Additional producer-specific parameters passed verbatim.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('LOAD [video_channel:int]{-[layer:int]|-0} {[clip:string]} {[loop:LOOP]} '
                '{[transition:CUT,MIX,PUSH,WIPE,SLIDE,STING] [duration:int] {[tween:string]} '
                '{[direction:LEFT,RIGHT]}} {SEEK [frame:int]} {LENGTH [frames:int]} '
                '{FILTER [filter:string]} {[auto:AUTO]} {[clear_on_404:CLEAR_ON_404]} {[parameters:raw]}')
def LOAD(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    clip: Optional[str] = None,
    loop: Optional[Literal["LOOP"]] = None,
    transition: Optional[Literal["CUT", "MIX", "PUSH", "WIPE", "SLIDE", "STING"]] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    direction: Optional[Literal["LEFT", "RIGHT"]] = None,
    frame: Optional[int] = None,
    frames: Optional[int] = None,
    filter: Optional[str] = None,
    auto: Optional[Literal["AUTO"]] = None,
    clear_on_404: Optional[Literal["CLEAR_ON_404"]] = None,
    parameters: Any = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Loads a clip to the foreground and plays the first frame before pausing.
    If any clip is playing on the target foreground then this clip will be replaced.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        clip: Path to the media clip to load.
        loop: Pass "LOOP" to loop the clip indefinitely.
        transition: Transition type (CUT, MIX, PUSH, WIPE, SLIDE, or STING).
        duration: Transition duration in frames.
        tween: Tween/easing function name for the transition animation.
        direction: Transition direction ("LEFT" or "RIGHT").
        frame: Frame position to seek to before playback begins.
        frames: Maximum number of frames to play (clip length limit).
        filter: FFmpeg filter graph string to apply to the clip.
        auto: Pass "AUTO" to automatically transition the clip to foreground when it is ready.
        clear_on_404: Pass "CLEAR_ON_404" to clear the layer if the clip file is not found.
        parameters: Additional producer-specific parameters passed verbatim.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('PLAY [video_channel:int]{-[layer:int]|-0} {[clip:string]} {[loop:LOOP]} '
                '{[transition:CUT,MIX,PUSH,WIPE,SLIDE,STING] [duration:int] {[tween:string]} '
                '{[direction:LEFT,RIGHT]}} {SEEK [frame:int]} {LENGTH [frames:int]} '
                '{FILTER [filter:string]} {[auto:AUTO]} {[clear_on_404:CLEAR_ON_404]} {[parameters:raw]}')
def PLAY(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    clip: Optional[str] = None,
    loop: Optional[Literal["LOOP"]] = None,
    transition: Optional[Literal["CUT", "MIX", "PUSH", "WIPE", "SLIDE", "STING"]] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    direction: Optional[Literal["LEFT", "RIGHT"]] = None,
    frame: Optional[int] = None,
    frames: Optional[int] = None,
    filter: Optional[str] = None,
    auto: Optional[Literal["AUTO"]] = None,
    clear_on_404: Optional[Literal["CLEAR_ON_404"]] = None,
    parameters: Any = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Moves clip from background to foreground and starts playing it.
    If a transition (see LOADBG) is prepared, it will be executed.
    When a clip argument is supplied this command is equivalent to LOADBG followed by PLAY.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        clip: Path to the media clip to load and play directly.
        loop: Pass "LOOP" to loop the clip indefinitely.
        transition: Transition type (CUT, MIX, PUSH, WIPE, SLIDE, or STING).
        duration: Transition duration in frames.
        tween: Tween/easing function name for the transition animation.
        direction: Transition direction ("LEFT" or "RIGHT").
        frame: Frame position to seek to before playback begins.
        frames: Maximum number of frames to play (clip length limit).
        filter: FFmpeg filter graph string to apply to the clip.
        auto: Pass "AUTO" to automatically transition the clip to foreground when it is ready.
        clear_on_404: Pass "CLEAR_ON_404" to clear the layer if the clip file is not found.
        parameters: Additional producer-specific parameters passed verbatim.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('PAUSE [video_channel:int]{-[layer:int]|-0}')
def PAUSE(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Pauses playback of the foreground clip on the specified layer.
    The RESUME command can be used to resume playback again.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('RESUME [video_channel:int]{-[layer:int]|-0}')
def RESUME(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Resumes playback of a foreground clip previously paused with the PAUSE command.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('STOP [video_channel:int]{-[layer:int]|-0}')
def STOP(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Removes the foreground clip of the specified layer.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CLEAR [video_channel:int]{-[layer:int]}')
def CLEAR(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Removes all clips (both foreground and background) of the specified layer.
    If no layer is specified then all layers in the specified video_channel are cleared.

    Args:
        video_channel: Video channel index.
        layer: Layer index. If omitted, all layers in the channel are cleared.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CLEAR ALL')
def CLEAR_ALL(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Clears foreground and background producers from all channels.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CALL [video_channel:int]{-[layer:int]|-0} [param:raw]')
def CALL(
    *,
    video_channel: int,
    param: Any,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Calls method on the specified producer with the provided param string.

    Args:
        video_channel: Video channel index.
        param: Method call string forwarded verbatim to the foreground producer.
        layer: Layer index. Defaults to layer 0 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CALLBG [video_channel:int]{-[layer:int]|-0} [param:raw]')
def CALLBG(
    *,
    video_channel: int,
    param: Any,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Calls a method on the background producer for the specified layer.

    Args:
        video_channel: Video channel index.
        param: Method call string forwarded verbatim to the background producer.
        layer: Layer index. Defaults to layer 0 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('SWAP [channel1:int]{-[layer1:int]} [channel2:int]{-[layer2:int]} {[transforms:TRANSFORMS]}')
def SWAP(
    *,
    channel1: int,
    channel2: int,
    layer1: Optional[int] = None,
    layer2: Optional[int] = None,
    transforms: Optional[Literal["TRANSFORMS"]] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Swaps layers between channels (both foreground and background will be swapped).

    Args:
        channel1: First video channel index.
        channel2: Second video channel index.
        layer1: Layer index on the first channel. Uses default layer if omitted.
        layer2: Layer index on the second channel. Uses default layer if omitted.
        transforms: Pass "TRANSFORMS" to also swap mixer transforms (fill, clip, etc.).
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('ADD [video_channel:int]{-[consumer_index:int]} [consumer:string] {[parameters:raw]}')
def ADD(
    *,
    video_channel: int,
    consumer: str,
    consumer_index: Optional[int] = None,
    parameters: Any = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Adds a consumer to the specified video channel.
    The string consumer will be parsed by the available consumer factories.
    If a successful match is found a consumer will be created and added to the video_channel.

    Args:
        video_channel: Video channel index.
        consumer: Consumer type name (e.g. DECKLINK, FILE, SCREEN).
        consumer_index: Optional numeric index to assign to this consumer instance.
        parameters: Additional consumer-specific parameters passed verbatim.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('REMOVE [video_channel:int]{-[consumer_index:int]} {[parameters:raw]}')
def REMOVE(
    *,
    video_channel: int,
    consumer_index: Optional[int] = None,
    parameters: Any = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Removes an existing consumer from video_channel.
    If consumer_index is given, the consumer will be removed via its id.
    If parameters are given instead, the consumer matching those parameters will be removed.

    Args:
        video_channel: Video channel index.
        consumer_index: Numeric ID of the consumer to remove.
        parameters: Consumer parameters to identify the consumer to remove.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('APPLY [video_channel:int]{-[layer:int]|-0} [param:raw]')
def APPLY(
    *,
    video_channel: int,
    param: Any,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Applies a method to a consumer/output where supported by the server.

    Args:
        video_channel: Video channel index.
        param: Method call string forwarded verbatim to the consumer.
        layer: Layer index. Defaults to layer 0 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('PRINT [video_channel:int]')
def PRINT(
    *,
    video_channel: int,
    request_id: Optional[str] = None,
) -> Command:
    """
    Saves an RGBA PNG bitmap still image of the contents of the specified channel in the media folder.

    Args:
        video_channel: Video channel index to capture.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('LOG LEVEL [level:TRACE,DEBUG,INFO,WARNING,ERROR,FATAL]')
def LOG_LEVEL(
    *,
    level: Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "FATAL"],
    request_id: Optional[str] = None,
) -> Command:
    """
    Changes the log level of the server.

    Args:
        level: New log level. One of TRACE, DEBUG, INFO, WARNING, ERROR, or FATAL.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('LOG CATEGORY [category:CALLTRACE,COMMUNICATION] [enable:0,1]')
def LOG_CATEGORY(
    *,
    category: Literal["CALLTRACE", "COMMUNICATION"],
    enable: Literal[0, 1],
    request_id: Optional[str] = None,
) -> Command:
    """
    Enables or disables the specified logging category.

    Args:
        category: Logging category to configure (CALLTRACE or COMMUNICATION).
        enable: 1 to enable the category, 0 to disable it.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('SET [video_channel:int] [variable:string] [value:string]')
def SET(
    *,
    video_channel: int,
    variable: str,
    value: str,
    request_id: Optional[str] = None,
) -> Command:
    """
    Changes the value of a channel variable. Available variables to set:
        - MODE: Changes the video format of the channel.
        - CHANNEL_LAYOUT: Changes the audio channel layout of the video channel.

    Args:
        video_channel: Video channel index.
        variable: Name of the channel variable to change (e.g. MODE, CHANNEL_LAYOUT).
        value: New value to assign to the variable.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('LOCK [video_channel:int] [action:ACQUIRE,RELEASE,CLEAR] {[lock_phrase:string]}')
def LOCK(
    *,
    video_channel: int,
    action: Literal["ACQUIRE", "RELEASE", "CLEAR"],
    lock_phrase: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Allows for exclusive access to a channel.

    Args:
        video_channel: Video channel index.
        action: Lock action to perform (ACQUIRE, RELEASE, or CLEAR).
        lock_phrase: Secret phrase required to acquire or release the lock.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('PING {[token:raw]}')
def PING(
    *,
    token: Any = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Checks that the AMCP parser is alive. The server replies with PONG and the optional token.

    Args:
        token: Optional token echoed back by the server in the PONG response.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...
