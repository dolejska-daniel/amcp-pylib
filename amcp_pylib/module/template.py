from amcp_pylib.core import Command, command_syntax


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} ADD [cg_layer:int] '
                '[template:string] [play_on_load:0,1] {[data:string]}')
def CG_ADD(command: Command) -> Command:
    """
    Prepares a template for displaying. It won't show until you call CG PLAY (unless you supply the play-on-load flag,
    1 for true). Data is either inline XML or a reference to a saved dataset.
    """
    return command


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} PLAY [cg_layer:int]')
def CG_PLAY(command: Command) -> Command:
    """
    Plays and displays the template in the specified layer.
    """
    return command


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} STOP [cg_layer:int]')
def CG_STOP(command: Command) -> Command:
    """
    Stops and removes the template from the specified layer.
    This is different from REMOVE in that the template gets a chance to animate out when it is stopped.
    """
    return command


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} NEXT [cg_layer:int]')
def CG_NEXT(command: Command) -> Command:
    """
    Triggers a "continue" in the template on the specified layer. This is used to control animations that has multiple discreet steps.
    """
    return command


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} REMOVE [cg_layer:int]')
def CG_REMOVE(command: Command) -> Command:
    """
    Removes the template from the specified layer.
    """
    return command


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} CLEAR')
def CG_CLEAR(command: Command) -> Command:
    """
    Removes all templates on a video layer. The entire cg producer will be removed.
    """
    return command


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} UPDATE [cg_layer:int] [data:string]')
def CG_UPDATE(command: Command) -> Command:
    """
    Sends new data to the template on specified layer. Data is either inline XML or a reference to a saved dataset.
    """
    return command


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} INVOKE [cg_layer:int] [method:string]')
def CG_INVOKE(command: Command) -> Command:
    """
    Invokes the given method on the template on the specified layer.
    Can be used to jump the playhead to a specific label.
    """
    return command


@command_syntax('CG [video_channel:int]{-[layer:int]|-9999} INFO {[cg_layer:int]}')
def CG_INFO(command: Command) -> Command:
    """
    Retrieves information about the template on the specified layer.
    If cg_layer is not given, information about the template host is given instead.
    """
    return command
