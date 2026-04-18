from typing import Literal, Optional

from amcp_pylib.core import Command, command_syntax


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} KEYER {[keyer:0,1]|0}')
def MIXER_KEYER(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    keyer: Optional[Literal[0, 1]] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Replaces layer n+1's alpha with the R (red) channel of layer n, and hides the RGB channels of layer n.
    If keyer equals 1 then the specified layer will not be rendered,
    instead it will be used as the key for the layer above.
    Returns the current keyer state when no argument is given.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        keyer: 1 to enable keyer mode, 0 to disable. Returns current state if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-keyer
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} CHROMA {[enable:0,1] {[target_hue:float] [hue_width:float] '
                '[min_saturation:float] [min_brightness:float] [softness:float] [spill_suppress:float] '
                '[spill_suppress_saturation:float] [show_mask:0,1]}} '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}')
def MIXER_CHROMA(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    enable: Optional[Literal[0, 1]] = None,
    target_hue: Optional[float] = None,
    hue_width: Optional[float] = None,
    min_saturation: Optional[float] = None,
    min_brightness: Optional[float] = None,
    softness: Optional[float] = None,
    spill_suppress: Optional[float] = None,
    spill_suppress_saturation: Optional[float] = None,
    show_mask: Optional[Literal[0, 1]] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Enables or disables chroma keying on the specified video layer.
    Giving no parameters returns the current chroma settings.
    The chroma keying is done in the HSB/HSV color space.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        enable: 1 to enable chroma keying, 0 to disable. Returns current state if omitted.
        target_hue: Hue angle (0–360) of the color to key out.
        hue_width: Width of the hue range to key out (0.0–1.0).
        min_saturation: Minimum saturation required for keying (0.0–1.0).
        min_brightness: Minimum brightness required for keying (0.0–1.0).
        softness: Edge softness of the chroma key mask (0.0–1.0).
        spill_suppress: Amount of spill suppression to apply (0.0–1.0).
        spill_suppress_saturation: Saturation applied during spill suppression (0.0–1.0).
        show_mask: 1 to display the computed key mask instead of the keyed image.
        duration: Animation duration in frames for the transition.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-chroma
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} BLEND {[blend:string]}')
def MIXER_BLEND(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    blend: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Sets the blend mode to use when compositing this layer with the background.
    If no argument is given the current blend mode is returned.

    Every layer can be set to use a different blend mode than the default normal mode,
    similar to applications like Photoshop.
    Some common uses are to use screen to make all the black image data become transparent,
    or to use add to selectively lighten highlights.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        blend: Blend mode name (e.g. normal, screen, add, overlay). Returns current if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-blend
    """
    ...


@command_syntax('MIXER [video_channel:int]-[layer:int] INVERT {invert:0,1|0}')
def MIXER_INVERT(
    *,
    video_channel: int,
    layer: int,
    invert: Optional[Literal[0, 1]] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Invert color. Only works on layers (layer index is required).
    Returns the current invert state when no argument is given.

    Args:
        video_channel: Video channel index.
        layer: Layer index (required for this command).
        invert: 1 to invert colors, 0 to disable. Returns current state if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-invert
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} OPACITY {[opacity:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_OPACITY(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    opacity: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Changes the opacity of the specified layer. The value is a float between 0 and 1.
    Retrieves the opacity of the specified layer if no argument is given.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        opacity: Opacity value from 0.0 (fully transparent) to 1.0 (fully opaque).
            Returns current opacity if omitted.
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-opacity
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} BRIGHTNESS {[brightness:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_BRIGHTNESS(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    brightness: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Changes the brightness of the specified layer. The value is a float between 0 and 1.
    Retrieves the brightness of the specified layer if no argument is given.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        brightness: Brightness multiplier from 0.0 (black) to 1.0 (original).
            Returns current brightness if omitted.
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-brightness
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} SATURATION {[saturation:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_SATURATION(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    saturation: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Changes the saturation of the specified layer. The value is a float between 0 and 1.
    Retrieves the saturation of the specified layer if no argument is given.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        saturation: Saturation multiplier from 0.0 (greyscale) to 1.0 (original).
            Returns current saturation if omitted.
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-saturation
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} CONTRAST {[contrast:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_CONTRAST(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    contrast: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Changes the contrast of the specified layer. The value is a float between 0 and 1.
    Retrieves the contrast of the specified layer if no argument is given.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        contrast: Contrast multiplier from 0.0 (flat grey) to 1.0 (original).
            Returns current contrast if omitted.
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-contrast
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} LEVELS {[min_input:float] [max_input:float] '
                '[gamma:float] [min_output:float] [max_output:float] {[duration:int] '
                '{[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_LEVELS(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    min_input: Optional[float] = None,
    max_input: Optional[float] = None,
    gamma: Optional[float] = None,
    min_output: Optional[float] = None,
    max_output: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Adjusts the video levels of a layer. If no arguments are given the current levels are returned.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        min_input: Black point of the input range (0.0–1.0).
        max_input: White point of the input range (0.0–1.0).
        gamma: Gamma correction value (> 0.0; 1.0 = no correction).
        min_output: Black point of the output range (0.0–1.0).
        max_output: White point of the output range (0.0–1.0).
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-levels
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} FILL {[x:float] [y:float] [x_scale:float] '
                '[y_scale:float] {[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_FILL(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    x: Optional[float] = None,
    y: Optional[float] = None,
    x_scale: Optional[float] = None,
    y_scale: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Scales/positions the video stream on the specified layer.
    The coordinate space is 0.0–1.0 where the full screen is 0 0 1 1
    (left-edge x, top-edge y, width, height).
    Returns the current fill transform if no arguments are given.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        x: Horizontal position of the left edge (0.0 = screen left).
        y: Vertical position of the top edge (0.0 = screen top).
        x_scale: Width of the layer as a fraction of the screen (1.0 = full width).
        y_scale: Height of the layer as a fraction of the screen (1.0 = full height).
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-fill
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} CLIP {[x:float] [y:float] [width:float] '
                '[height:float] {[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_CLIP(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    x: Optional[float] = None,
    y: Optional[float] = None,
    width: Optional[float] = None,
    height: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Defines the rectangular viewport where a layer is rendered on the screen.
    The clip is not affected by MIXER FILL, MIXER ROTATION or MIXER PERSPECTIVE.
    See MIXER CROP if you want to crop the layer before transforming it.
    Returns the current clip rectangle if no arguments are given.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        x: Horizontal position of the clip left edge (0.0–1.0).
        y: Vertical position of the clip top edge (0.0–1.0).
        width: Clip width as a fraction of the screen (0.0–1.0).
        height: Clip height as a fraction of the screen (0.0–1.0).
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-clip
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} ANCHOR {[x:float] [y:float] {[duration:int] '
                '{[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_ANCHOR(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    x: Optional[float] = None,
    y: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Changes the anchor point of the specified layer, or returns the current values if no arguments are given.
    The anchor point is around which MIXER FILL and MIXER ROTATION will be done from.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        x: Horizontal anchor position in normalized coordinates (0.5 = center).
        y: Vertical anchor position in normalized coordinates (0.5 = center).
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-anchor
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} CROP {[left_edge:float] [top_edge:float] '
                '[right_edge:float] [bottom_edge:float] {[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_CROP(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    left_edge: Optional[float] = None,
    top_edge: Optional[float] = None,
    right_edge: Optional[float] = None,
    bottom_edge: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Defines how a layer should be cropped before making other transforms via MIXER FILL,
    MIXER ROTATION and MIXER PERSPECTIVE.
    See MIXER CLIP if you want to change the viewport relative to the screen instead.
    Returns the current crop values if no arguments are given.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        left_edge: Fraction of the image to crop from the left side (0.0–1.0).
        top_edge: Fraction of the image to crop from the top (0.0–1.0).
        right_edge: Fraction of the image to crop from the right side (0.0–1.0).
        bottom_edge: Fraction of the image to crop from the bottom (0.0–1.0).
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-crop
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} ROTATION {[angle:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_ROTATION(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    angle: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Returns or modifies the angle of which a layer is rotated by (clockwise degrees)
    around the point specified by MIXER ANCHOR.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        angle: Clockwise rotation angle in degrees. Returns current angle if omitted.
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-rotation
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} PERSPECTIVE {[top_left_x:float] [top_left_y:float] '
                '[top_right_x:float] [top_right_y:float] [bottom_right_x:float] [bottom_right_y:float] '
                '[bottom_left_x:float] [bottom_left_y:float] {[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_PERSPECTIVE(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    top_left_x: Optional[float] = None,
    top_left_y: Optional[float] = None,
    top_right_x: Optional[float] = None,
    top_right_y: Optional[float] = None,
    bottom_right_x: Optional[float] = None,
    bottom_right_y: Optional[float] = None,
    bottom_left_x: Optional[float] = None,
    bottom_left_y: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Perspective transforms (corner pins) a layer.
    All coordinates are in normalized screen space (0.0–1.0).
    Returns the current perspective transform if no arguments are given.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        top_left_x: X coordinate of the top-left corner pin.
        top_left_y: Y coordinate of the top-left corner pin.
        top_right_x: X coordinate of the top-right corner pin.
        top_right_y: Y coordinate of the top-right corner pin.
        bottom_right_x: X coordinate of the bottom-right corner pin.
        bottom_right_y: Y coordinate of the bottom-right corner pin.
        bottom_left_x: X coordinate of the bottom-left corner pin.
        bottom_left_y: Y coordinate of the bottom-left corner pin.
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-perspective
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} MIPMAP {[mipmap:0,1]|0}')
def MIXER_MIPMAP(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    mipmap: Optional[Literal[0, 1]] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Sets whether to use mipmapping (anisotropic filtering if supported) on a layer or not.
    If no argument is given the current state is returned.
    Mipmapping reduces aliasing when downscaling/perspective transforming.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        mipmap: 1 to enable mipmapping, 0 to disable. Returns current state if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-mipmap
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]|-0} VOLUME {[volume:float] '
                '{[duration:int] {[tween:string]|LINEAR}|0 LINEAR}}')
def MIXER_VOLUME(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    volume: Optional[float] = None,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Changes the volume of the specified layer.
    1.0 is the original volume, which can be attenuated (< 1.0) or amplified (> 1.0).
    Retrieves the volume of the specified layer if no argument is given.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Defaults to layer 0 if omitted.
        volume: Volume multiplier (1.0 = original; 0.0 = mute). Returns current if omitted.
        duration: Animation duration in frames.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-volume
    """
    ...


@command_syntax('MIXER [video_channel:int] MASTERVOLUME {[volume:float]}')
def MIXER_MASTERVOLUME(
    *,
    video_channel: int,
    volume: Optional[float] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Changes or retrieves (when no argument is given) the volume of the entire channel.

    Args:
        video_channel: Video channel index.
        volume: Master volume multiplier (1.0 = original; 0.0 = mute). Returns current if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-mastervolume
    """
    ...


@command_syntax('MIXER [video_channel:int] STRAIGHT_ALPHA_OUTPUT {[straight_alpha:0,1|0]}')
def MIXER_STRAIGHT_ALPHA_OUTPUT(
    *,
    video_channel: int,
    straight_alpha: Optional[Literal[0, 1]] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Turn straight alpha output on or off for the specified channel.
    The casparcg.config needs to be configured to enable the feature.

    Args:
        video_channel: Video channel index.
        straight_alpha: 1 to output straight (un-premultiplied) alpha, 0 to disable.
            Returns current state if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-straight_alpha_output
    """
    ...


@command_syntax('MIXER [video_channel:int] GRID [resolution:int] {[duration:int] {[tween:string]|LINEAR}|0 LINEAR}')
def MIXER_GRID(
    *,
    video_channel: int,
    resolution: int,
    duration: Optional[int] = None,
    tween: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Creates a grid of video layers in ascending order of the layer index.
    For example, if resolution equals 2 then a 2x2 grid of layers will be created starting from layer 1.

    Args:
        video_channel: Video channel index.
        resolution: Grid side length (e.g. 2 creates a 2×2 grid from layers 1–4).
        duration: Animation duration in frames for the transition into the grid.
        tween: Tween/easing function name. Defaults to LINEAR.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-grid
    """
    ...


@command_syntax('MIXER [video_channel:int] COMMIT')
def MIXER_COMMIT(
    *,
    video_channel: int,
    request_id: Optional[str] = None,
) -> Command:
    """
    Commits all deferred mixer transforms on the specified channel.
    This ensures that all animations start at the same exact frame.

    Args:
        video_channel: Video channel index.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-commit
    """
    ...


@command_syntax('MIXER [video_channel:int]{-[layer:int]} CLEAR')
def MIXER_CLEAR(
    *,
    video_channel: int,
    layer: Optional[int] = None,
    request_id: Optional[str] = None,
) -> Command:
    """
    Clears all mixer transformations on a channel or layer.
    If no layer is specified, all transforms on the channel are cleared.

    Args:
        video_channel: Video channel index.
        layer: Layer index. Clears the entire channel if omitted.
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#mixer-clear
    """
    ...


@command_syntax('CHANNEL_GRID')
def CHANNEL_GRID(
    *,
    request_id: Optional[str] = None,
) -> Command:
    """
    Opens a new channel and displays a grid with the contents of all the existing channels.
    The element <channel-grid>true</channel-grid> must be present in casparcg.config for this to work correctly.

    Args:
        request_id: Optional AMCP request ID for command batching (REQ prefix).

    :link https://github.com/CasparCG/help/wiki/AMCP-Protocol#channel_grid
    """
    ...
