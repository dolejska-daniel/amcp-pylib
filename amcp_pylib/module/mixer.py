from amcp_pylib.core import Command, command_syntax


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} KEYER {[keyer:0,1]|0}')
def MIXER_KEYER(command: Command) -> Command:
    """
    Replaces layer n+1's alpha with the R (red) channel of layer n, and hides the RGB channels of layer n.
    If keyer equals 1 then the specified layer will not be rendered,
    instead it will be used as the key for the layer above.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-keyer
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} CHROMA {[enable:0,1] {[target_hue:float] [hue_width:float] '
                '[min_saturation:float] [min_brightness:float] [softness:float] [spill_suppress:float] '
                '[spill_suppress_saturation:float] [show_mask:0,1]}} '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}')
def MIXER_CHROMA(command: Command) -> Command:
    """
    Enables or disables chroma keying on the specified video layer.
    Giving no parameters returns the current chroma settings.
    The chroma keying is done in the HSB/HSV color space.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-chroma
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} CHROMA {[enable:0,1] {[target_hue:float] [hue_width:float] '
                '[min_saturation:float] [min_brightness:float] [softness:float] [spill_suppress:float] '
                '[spill_suppress_saturation:float] [show_mask:0,1]}} {[duration:int] '
                '{[tween:string]|LINEAR}|0 LINEAR}')
def MIXER_BLEND(command: Command) -> Command:
    """
    Sets the blend mode to use when compositing this layer with the background.
    If no argument is given the current blend mode is returned.

    Every layer can be set to use a different blend mode than the default normal mode,
    similar to applications like Photoshop.
    Some common uses are to use screen to make all the black image data become transparent,
    or to use add to selectively lighten highlights.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-blend
    """
    return command


@command_syntax('MIXER [video_channel:int]-[layer:int] INVERT {invert:0,1|0}')
def MIXER_INVERT(command: Command) -> Command:
    """
    Invert color. Only works on layers.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-invert
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} OPACITY {[opacity:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_OPACITY(command: Command) -> Command:
    """
    Changes the opacity of the specified layer. The value is a float between 0 and 1.
    Retrieves the opacity of the specified layer if no argument is given.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-opacity
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} BRIGHTNESS {[brightness:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_BRIGHTNESS(command: Command) -> Command:
    """
    Changes the brightness of the specified layer. The value is a float between 0 and 1.
    Retrieves the brightness of the specified layer if no argument is given.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-brightness
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} SATURATION {[saturation:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_SATURATION(command: Command) -> Command:
    """
    Changes the saturation of the specified layer. The value is a float between 0 and 1.
    Retrieves the saturation of the specified layer if no argument is given.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-saturation
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} CONTRAST {[contrast:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_CONTRAST(command: Command) -> Command:
    """
    Changes the contrast of the specified layer. The value is a float between 0 and 1.
    Retrieves the contrast of the specified layer if no argument is given.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-contrast
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} LEVELS {[min_input:float] [max_input:float] '
                '[gamma:float] [min_output:float] [max_output:float]{[duration:int] '
                '{[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_LEVELS(command: Command) -> Command:
    """
    Adjusts the video levels of a layer. If no arguments are given the current levels are returned.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-levels
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} FILL {[x:float] [y:float] [x_scale:float] '
                '[y_scale:float] {[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_FILL(command: Command) -> Command:
    """
    Scales/positions the video stream on the specified layer. The concept is quite simple;
    it comes from the ancient DVE machines like ADO.
    Imagine that the screen has a size of 1x1 (not in pixel, but in an abstract measure).
    Then the coordinates of a full size picture is 0 0 1 1, which means left edge is at coordinate 0,
    top edge at coordinate 0, width full size = 1, heigh full size = 1.

    If you want to crop the picture on the left side (for wipe left to right) you set the left edge to full right
    => 1 and the width to 0. So this give you the start-coordinates of 1 0 0 1.

    End coordinates of any wipe are allways the full picture 0 0 1 1.

    With the FILL command it can make sense to have values between 1 and 0, if you want to do a smaller window.
    If, for instance you want to have a window of half the size of your screen, you set with and height to 0.5.
    If you want to center it you set left and top edge to 0.25 so you will get the arguments 0.25 0.25 0.5 0.5.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-fill
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} CLIP {[x:float] [y:float] [width:float] '
                '[height:float] {[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_CLIP(command: Command) -> Command:
    """
    Defines the rectangular viewport where a layer is rendered thru on the screen without being affected by MIXER FILL,
    MIXER ROTATION and MIXER PERSPECTIVE. See MIXER CROP if you want to crop the layer before transforming it.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-clip
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} ANCHOR {[x:float] [y:float] {[duration:int] '
                '{[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_ANCHOR(command: Command) -> Command:
    """
    Changes the anchor point of the specified layer, or returns the current values if no arguments are given.

    The anchor point is around which MIXER FILL and MIXER ROTATION will be done from.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-anchor
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} CROP {[left_edge:float] [top_edge:float] '
                '[right_edge:float] [bottom_edge:float] {[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_CROP(command: Command) -> Command:
    """
    Defines how a layer should be cropped before making other transforms via MIXER FILL, MIXER ROTATION
    and #MIXER PERSPECTIVE. See MIXER CLIP if you want to change the viewport relative to the screen instead.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-crop
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} ROTATION {[angle:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_ROTATION(command: Command) -> Command:
    """
    Returns or modifies the angle of which a layer is rotated by (clockwise degrees)
    around the point specified by MIXER ANCHOR.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-rotation
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} PERSPECTIVE {[top_left_x:float] [top_left_y:float] '
                '[top_right_x:float] [top_right_y:float] [bottom_right_x:float] [bottom_right_y:float] '
                '[bottom_left_x:float] [bottom_left_y:float] {[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_PERSPECTIVE(command: Command) -> Command:
    """
    Perspective transforms (corner pins or distorts if you will) a layer.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-perspective
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} MIPMAP {[mipmap:0,1]|0}')
def MIXER_MIPMAP(command: Command) -> Command:
    """
    Sets whether to use mipmapping (anisotropic filtering if supported) on a layer or not.
    If no argument is given the current state is returned.
    Mipmapping reduces aliasing when downscaling/perspective transforming.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-mipmap
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} VOLUME {[volume:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_VOLUME(command: Command) -> Command:
    """
    Changes the volume of the specified layer. The 1.0 is the original volume, which can be attenuated or amplified.
    Retrieves the volume of the specified layer if no argument is given.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-volume
    """
    return command


@command_syntax('MIXER [video_channel:int] MASTERVOLUME {[volume:float]}')
def MIXER_MASTERVOLUME(command: Command) -> Command:
    """
    Changes or retrieves (giving no argument) the volume of the entire channel.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-mastervolume
    """
    return command


@command_syntax('MIXER [video_channel:int] STRAIGHT_ALPHA_OUTPUT {[straight_alpha:0,1|0]}')
def MIXER_STRAIGHT_ALPHA_OUTPUT(command: Command) -> Command:
    """
    Turn straight alpha output on or off for the specified channel.
    The casparcg.config needs to be configured to enable the feature.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-straight_alpha_output
    """
    return command


@command_syntax('MIXER [video_channel:int] GRID [resolution:int] {[duration:int] {[tween:string]|LINEAR}|0 LINEAR}')
def MIXER_GRID(command: Command) -> Command:
    """
    Creates a grid of video layer in ascending order of the layer index,
    i.e. if resolution equals 2 then a 2x2 grid of layers will be created starting from layer 1.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-grid
    """
    return command


@command_syntax('MIXER [video_channel:int] COMMIT')
def MIXER_COMMIT(command: Command) -> Command:
    """
    Commits all deferred mixer transforms on the specified channel.
    This ensures that all animations start at the same exact frame.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-commit
    """
    return command


@command_syntax('MIXER [video_channel:int]{-[layer:int]} CLEAR')
def MIXER_CLEAR(command: Command) -> Command:
    """
    Clears all transformations on a channel or layer.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-clear
    """
    return command


@command_syntax('CHANNEL_GRID')
def CHANNEL_GRID(command: Command) -> Command:
    """
    Opens a new channel and displays a grid with the contents of all the existing channels.
    The element <channel-grid>true</channel-grid> must be present in casparcg.config for this to work correctly.

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#channel_grid
    """
    return command
