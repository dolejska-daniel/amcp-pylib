from typing import Literal, Optional

from amcp_pylib.core import Command, command_syntax


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} ADD [cg_layer:int] '
                '[template:string] [play_on_load:0,1] {[data:string]}')
def CG_ADD(
    *,
    video_channel: int,
    cg_layer: int,
    template: str,
    play_on_load: Literal[0, 1],
    layer: Optional[int] = None,
    data: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Prepares a template for displaying. It won't show until you call CG PLAY
    (unless you supply play_on_load=1). Data is either inline XML or a reference to a saved dataset.

    Args:
        video_channel: Video channel index.
        cg_layer: CG layer index within the CG producer.
        template: Template file name (without extension) relative to the templates folder.
        play_on_load: 1 to start playing the template immediately after loading, 0 to pause on first frame.
        layer: Video layer index on the channel. Defaults to layer 9999 if omitted.
        data: Inline XML data or name of a saved dataset to pass to the template.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} PLAY [cg_layer:int]')
def CG_PLAY(
    *,
    video_channel: int,
    cg_layer: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Plays and displays the template in the specified layer.

    Args:
        video_channel: Video channel index.
        cg_layer: CG layer index within the CG producer.
        layer: Video layer index on the channel. Defaults to layer 9999 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} STOP [cg_layer:int]')
def CG_STOP(
    *,
    video_channel: int,
    cg_layer: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Stops and removes the template from the specified layer.
    This is different from CG REMOVE in that the template gets a chance to animate out when it is stopped.

    Args:
        video_channel: Video channel index.
        cg_layer: CG layer index within the CG producer.
        layer: Video layer index on the channel. Defaults to layer 9999 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} NEXT [cg_layer:int]')
def CG_NEXT(
    *,
    video_channel: int,
    cg_layer: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Triggers a "continue" in the template on the specified layer.
    This is used to control animations that have multiple discrete steps.

    Args:
        video_channel: Video channel index.
        cg_layer: CG layer index within the CG producer.
        layer: Video layer index on the channel. Defaults to layer 9999 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} REMOVE [cg_layer:int]')
def CG_REMOVE(
    *,
    video_channel: int,
    cg_layer: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Removes the template from the specified layer immediately without an outro animation.

    Args:
        video_channel: Video channel index.
        cg_layer: CG layer index within the CG producer.
        layer: Video layer index on the channel. Defaults to layer 9999 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} CLEAR')
def CG_CLEAR(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Removes all templates on a video layer. The entire CG producer will be removed.

    Args:
        video_channel: Video channel index.
        layer: Video layer index on the channel. Defaults to layer 9999 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} UPDATE [cg_layer:int] [data:string]')
def CG_UPDATE(
    *,
    video_channel: int,
    cg_layer: int,
    data: str,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Sends new data to the template on specified layer.
    Data is either inline XML or a reference to a saved dataset.

    Args:
        video_channel: Video channel index.
        cg_layer: CG layer index within the CG producer.
        data: Inline XML data or name of a saved dataset to send to the template.
        layer: Video layer index on the channel. Defaults to layer 9999 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} INVOKE [cg_layer:int] [method:string]')
def CG_INVOKE(
    *,
    video_channel: int,
    cg_layer: int,
    method: str,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Invokes the given method on the template on the specified layer.
    Can be used to jump the playhead to a specific label.

    Args:
        video_channel: Video channel index.
        cg_layer: CG layer index within the CG producer.
        method: Method or label name to invoke on the Flash/HTML template.
        layer: Video layer index on the channel. Defaults to layer 9999 if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} INFO {[cg_layer:int]}')
def CG_INFO(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    cg_layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Retrieves information about the template on the specified layer.
    If cg_layer is not given, information about the template host is given instead.

    Args:
        video_channel: Video channel index.
        layer: Video layer index on the channel. Defaults to layer 9999 if omitted.
        cg_layer: CG layer index to query. Returns host info if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).
    """
    ...
