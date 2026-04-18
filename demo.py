"""
amcp-pylib demonstration  -  staged scenarios from simple to complex.

Requires a running CasparCG server at 127.0.0.1:5250.
Each scenario is self-contained and gracefully skips on connection failure.
"""

import asyncio
import logging
import time

from amcp_pylib.core import Client, ClientAsync
from amcp_pylib.exceptions import AMCPResponseError
from amcp_pylib.module import *
from amcp_pylib.response import ResponseBase

logging.basicConfig(
    format="%(asctime)s %(levelname)s (%(name)s): %(message)s",
    level=logging.WARNING,
    datefmt="%H:%M:%S",
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SEPARATOR = "-" * 60


def section(title: str) -> None:
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def send(client: Client, command, label: str = "") -> ResponseBase | None:
    tag = f"[{label}]  " if label else ""
    print(f"  {tag}>> {str(command).strip()}")
    try:
        response = client.send(command)
        status = f"{response.code} {response.code_description}"
        data_preview = ""
        if response.data:
            preview = response.data[0][:80] if response.data[0] else ""
            data_preview = f"  <- {preview}" + ("..." if len(response.data[0]) > 80 else "")
        print(f"  {tag}<< {status}{data_preview}")
        return response
    except AMCPResponseError as exc:
        print(f"  {tag}!! ERROR {exc.response.code}: {exc.response.header_text.strip()}")
        return exc.response
    except Exception as exc:
        print(f"  {tag}!! {type(exc).__name__}: {exc}")
        return None


def wait(seconds: float, reason: str = "") -> None:
    print(f"  (waiting {seconds}s{': ' + reason if reason else ''})")
    time.sleep(seconds)


def discover_clip(client: Client) -> str:
    """
    Query CLS and return the first available media clip name.
    Falls back to a built-in hex color producer if no media is available
    or if the media server is offline (CasparCG 2.5 routes CLS through a
    separate REST service that may not be running).
    """
    resp = send(client, CLS(), "cls")
    if resp and resp.ok and resp.data:
        for line in resp.data:
            line = line.strip()
            if line.startswith('"'):
                end = line.find('"', 1)
                if end > 1:
                    clip = line[1:end]
                    print(f"  Discovered media: {clip!r}")
                    return clip
    print("  No media found  -  using built-in color producer (#ff6600).")
    print("  (Add video files to CasparCG's media folder for richer playback.)")
    return "#ff6600"


# ---------------------------------------------------------------------------
# Scenario 1  -  Server discovery
# ---------------------------------------------------------------------------

def scenario_server_discovery(client: Client) -> str:
    """
    Ping the server, inspect version and paths, discover available media.
    Returns the clip name (or color fallback) used in all later scenarios.
    """
    section("Scenario 1  -  Server Discovery")

    send(client, PING(token="hello"), "ping")
    send(client, VERSION(), "version")
    send(client, INFO_PATHS(), "paths")

    clip = discover_clip(client)

    resp = send(client, TLS(), "template list")
    if resp and resp.ok and resp.data:
        print(f"  Found {len(resp.data)} template(s).")

    return clip


# ---------------------------------------------------------------------------
# Scenario 2  -  Simple clip playback
# ---------------------------------------------------------------------------

def scenario_simple_playback(client: Client, clip: str) -> None:
    """Load a clip in the background, then cut to it, pause, resume, stop."""
    section("Scenario 2  -  Simple Clip Playback")

    # Pre-load into the background slot; server buffers it so the cut is instant.
    send(client, LOADBG(channel=1, clip=clip, loop="LOOP"), "load bg")
    send(client, PLAY(video_channel=1), "play (cut)")

    wait(1.5, "clip playing")

    send(client, PAUSE(video_channel=1), "pause")
    wait(0.5)
    send(client, RESUME(video_channel=1), "resume")
    wait(1.0)

    send(client, STOP(video_channel=1), "stop")
    send(client, CLEAR(video_channel=1), "clear channel")


# ---------------------------------------------------------------------------
# Scenario 3  -  Transitions
# ---------------------------------------------------------------------------

def scenario_transitions(client: Client, clip: str) -> None:
    """
    Demonstrate MIX, PUSH, and WIPE transitions with different tweens.
    Each step transitions to a visually distinct colour so the effect is obvious.
    """
    section("Scenario 3  -  Transitions & Tweens")

    # Each entry: (next_clip, transition_type, duration_frames, tween, label)
    steps = [
        (clip,      "MIX",  25, "easeinsine",  "dissolve"),
        ("#c0392b", "PUSH", 20, "easeinquint", "push right (crimson)"),
        ("#1a5276", "WIPE", 30, "linear",      "wipe (deep blue)"),
        ("#1e8449", "MIX",  25, "easeinoutcubic", "dissolve (forest green)"),
    ]

    # Start on the discovered clip (or orange fallback).
    send(client, PLAY(video_channel=1, clip=clip), "initial clip")
    wait(1.0)

    for dest_clip, transition, duration, tween, label in steps:
        send(
            client,
            LOADBG(channel=1, clip=dest_clip, transition=transition,
                   duration=duration, tween=tween),
            f"loadbg ({label})",
        )
        send(client, PLAY(video_channel=1), f"trigger {transition}")
        wait(1.5, "transition plays out")

    send(client, CLEAR(video_channel=1), "clear")


# ---------------------------------------------------------------------------
# Scenario 4  -  Mixer: colour grading & animated fades
# ---------------------------------------------------------------------------

def scenario_mixer_color(client: Client, clip: str) -> None:
    """
    Fade a muted steel-blue layer in from black, then dramatically shift its
    brightness and saturation so the grading effects are unmistakably visible.

    Steel blue (#4a7fa8) is chosen because it sits at medium saturation/brightness:
    halving the brightness makes it obviously darker, and doubling the saturation
    turns it into a vivid cobalt.  The same transforms on a nearly-white or
    fully-saturated colour would be imperceptible.
    """
    section("Scenario 4  -  Mixer: Colour Grading & Animated Fades")

    # Use a fixed colour that shows grading clearly.  If a real media clip was
    # discovered, it will be used as a background on layer 9 for context.
    GRADING_CLIP = "#4a7fa8"   # medium-saturation steel blue
    LAYER = 10

    if not clip.startswith("#"):
        send(client, PLAY(video_channel=1, layer=9, clip=clip, loop="LOOP"), "bg clip (layer 9)")

    send(client, PLAY(video_channel=1, layer=LAYER, clip=GRADING_CLIP), "grading layer (steel blue)")

    # Fade in from fully transparent over 50 frames (~1 s at 50 fps).
    send(client, MIXER_OPACITY(video_channel=1, layer=LAYER, opacity=0.0), "opacity -> 0 (hidden)")
    wait(0.1)
    send(
        client,
        MIXER_OPACITY(video_channel=1, layer=LAYER, opacity=1.0, duration=50, tween="easeinoutcubic"),
        "fade in",
    )
    wait(2.0, "fade completes")

    # Darken dramatically (0.4 = 40% brightness).
    send(
        client,
        MIXER_BRIGHTNESS(video_channel=1, layer=LAYER, brightness=0.4, duration=40, tween="linear"),
        "brightness -> 0.4 (darken)",
    )
    wait(1.5, "darkening")

    # Restore brightness, then boost saturation to vivid cobalt.
    send(
        client,
        MIXER_BRIGHTNESS(video_channel=1, layer=LAYER, brightness=1.0, duration=25, tween="linear"),
        "brightness -> 1.0 (restore)",
    )
    wait(1.0)
    send(
        client,
        MIXER_SATURATION(video_channel=1, layer=LAYER, saturation=3.0, duration=40, tween="easeinoutcubic"),
        "saturation -> 3.0 (vivid cobalt)",
    )
    wait(1.5, "saturation boost")

    send(client, MIXER_CLEAR(video_channel=1, layer=LAYER), "reset grading")
    send(client, CLEAR(video_channel=1), "clear channel")


# ---------------------------------------------------------------------------
# Scenario 5  -  Mixer: spatial transforms & picture-in-picture
# ---------------------------------------------------------------------------

def scenario_mixer_spatial(client: Client, clip: str) -> None:
    """
    Two layers: a full-screen background and a picture-in-picture insert.
    The PiP animates in from off-screen, rotates briefly, then gets a
    corner-pin perspective warp to simulate a tilted monitor.
    """
    section("Scenario 5  -  Mixer: Spatial Transforms & PiP")

    BG_LAYER  = 10
    PIP_LAYER = 20

    # Use contrasting colours so the PiP box is clearly visible against the background.
    bg_clip  = clip if not clip.startswith("#") else "#1a237e"   # dark navy
    pip_clip = "#e65100"                                          # deep orange

    send(client, PLAY(video_channel=1, layer=BG_LAYER, clip=bg_clip, loop="LOOP"), "bg layer")

    # PiP -- start off the right edge (x=1.0), then slide in to the top-right corner.
    send(client, PLAY(video_channel=1, layer=PIP_LAYER, clip=pip_clip), "pip layer")
    send(
        client,
        MIXER_FILL(video_channel=1, layer=PIP_LAYER, x=1.0, y=0.0, x_scale=0.35, y_scale=0.35),
        "pip off-screen",
    )
    send(
        client,
        MIXER_FILL(
            video_channel=1, layer=PIP_LAYER,
            x=0.63, y=0.04, x_scale=0.35, y_scale=0.35,
            duration=30, tween="easeinoutback",
        ),
        "pip slide in",
    )

    wait(2.0, "slide completes")

    send(
        client,
        MIXER_ROTATION(video_channel=1, layer=PIP_LAYER, angle=6.0, duration=20, tween="linear"),
        "rotate +6 deg",
    )
    wait(1.0)
    send(
        client,
        MIXER_ROTATION(video_channel=1, layer=PIP_LAYER, angle=0.0, duration=20, tween="linear"),
        "rotate back",
    )

    wait(1.5)

    # Perspective warp -- simulate the clip displayed on a tilted monitor.
    send(
        client,
        MIXER_PERSPECTIVE(
            video_channel=1, layer=PIP_LAYER,
            top_left_x=0.62,    top_left_y=0.05,
            top_right_x=0.97,   top_right_y=0.02,
            bottom_right_x=0.99, bottom_right_y=0.37,
            bottom_left_x=0.64, bottom_left_y=0.40,
            duration=20, tween="easeinoutcubic",
        ),
        "perspective warp",
    )

    wait(1.5)

    send(client, MIXER_CLEAR(video_channel=1), "reset all mixer")
    send(client, CLEAR(video_channel=1), "clear channel")


# ---------------------------------------------------------------------------
# Scenario 6  -  CG templates: lower-third with data updates
# ---------------------------------------------------------------------------

def _lower_third_data(name: str, title: str) -> str:
    return (
        f'<templateData>'
        f'<componentData id="f0"><data id="text" value="{name}"/></componentData>'
        f'<componentData id="f1"><data id="text" value="{title}"/></componentData>'
        f'</templateData>'
    )


def scenario_cg_templates(client: Client) -> None:
    """
    Load a lower-third template, drive it through its lifecycle:
    add -> play -> update data mid-air -> next -> invoke label -> stop.
    Also demonstrates DATA_STORE / DATA_RETRIEVE for reusable datasets.
    """
    section("Scenario 6  -  CG Templates: Lower-Third")

    TEMPLATE  = "lower_thirds/standard"
    CG_LAYER  = 1
    VID_LAYER = 20

    # Persist a dataset on the server for reuse across sessions.
    dataset_name = "guests/alice"
    send(
        client,
        DATA_STORE(name=dataset_name, data=_lower_third_data("Alice Novak", "Senior Correspondent")),
        "data store",
    )
    resp = send(client, DATA_RETRIEVE(name=dataset_name), "data retrieve")
    if resp and resp.ok and resp.data:
        print(f"  Stored dataset confirmed ({len(resp.data_str)} chars).")

    resp = send(client, DATA_LIST(), "data list")
    if resp and resp.ok and resp.data:
        print(f"  {len(resp.data)} dataset(s) on server.")

    # Add with inline data; play_on_load=0 so we control the timing.
    send(
        client,
        CG_ADD(
            video_channel=1, layer=VID_LAYER, cg_layer=CG_LAYER,
            template=TEMPLATE, play_on_load=0,
            data=_lower_third_data("Alice Novak", "Senior Correspondent"),
        ),
        "cg add",
    )
    send(client, CG_PLAY(video_channel=1, layer=VID_LAYER, cg_layer=CG_LAYER), "cg play")
    wait(2.5, "lower-third animates in")

    # Update data without stopping -- the template handles the transition internally.
    send(
        client,
        CG_UPDATE(
            video_channel=1, layer=VID_LAYER, cg_layer=CG_LAYER,
            data=_lower_third_data("Bob Hartmann", "Field Reporter"),
        ),
        "cg update",
    )
    wait(1.5, "name swap animates")

    send(client, CG_NEXT(video_channel=1, layer=VID_LAYER, cg_layer=CG_LAYER), "cg next")
    wait(1.0)

    send(
        client,
        CG_INVOKE(video_channel=1, layer=VID_LAYER, cg_layer=CG_LAYER, method="outro"),
        "cg invoke:outro",
    )
    wait(1.0)

    send(client, CG_STOP(video_channel=1, layer=VID_LAYER, cg_layer=CG_LAYER), "cg stop")
    send(client, CG_CLEAR(video_channel=1, layer=VID_LAYER), "cg clear")
    send(client, DATA_REMOVE(name=dataset_name), "data remove")
    send(client, CLEAR(video_channel=1, layer=VID_LAYER), "clear layer")


# ---------------------------------------------------------------------------
# Scenario 7  -  Multi-layer composition, SWAP, grid monitor
# ---------------------------------------------------------------------------

def scenario_multilayer(client: Client, clip: str) -> None:
    """
    Build a three-layer stack, swap two layers at runtime, snapshot to disk,
    and display a 2x2 monitoring grid on channel 2.
      Layer 10  -  full-screen background
      Layer 20  -  overlay cropped to left half, placed on right side of screen
      Layer 30  -  small logo positioned in the bottom-left corner
    """
    section("Scenario 7  -  Multi-layer Composition & Swap")

    # Three distinct colours so every layer is unambiguously identifiable on screen.
    L10 = clip if not clip.startswith("#") else "#1b5e20"  # dark green
    L20 = "#b71c1c"   # dark red
    L30 = "#0d47a1"   # dark blue

    send(client, PLAY(video_channel=1, layer=10, clip=L10, loop="LOOP"), "layer 10: bg (green)")

    send(client, PLAY(video_channel=1, layer=20, clip=L20), "layer 20: overlay (red)")
    send(
        client,
        MIXER_CROP(video_channel=1, layer=20, left_edge=0.0, top_edge=0.0,
                   right_edge=0.5, bottom_edge=1.0),
        "crop layer 20 -> left half",
    )
    send(
        client,
        MIXER_FILL(video_channel=1, layer=20, x=0.5, y=0.0, x_scale=0.5, y_scale=1.0),
        "fill layer 20 -> right half of screen",
    )
    send(
        client,
        MIXER_OPACITY(video_channel=1, layer=20, opacity=0.85),
        "layer 20 opacity 85%",
    )

    send(client, PLAY(video_channel=1, layer=30, clip=L30), "layer 30: sting (blue)")
    send(
        client,
        MIXER_FILL(video_channel=1, layer=30, x=0.02, y=0.75, x_scale=0.2, y_scale=0.2),
        "position logo corner",
    )

    wait(2.0, "composition live")

    send(
        client,
        SWAP(channel1=1, layer1=20, channel2=1, layer2=30, transforms="TRANSFORMS"),
        "swap layers 20 <-> 30",
    )
    wait(1.5)

    send(client, PRINT(video_channel=1), "snapshot to disk")

    # 2x2 monitoring grid requires a second channel configured in casparcg.config.
    send(client, MIXER_GRID(video_channel=2, resolution=2, duration=20, tween="linear"), "grid 2x2 on ch2")
    wait(1.5)

    send(client, MIXER_CLEAR(video_channel=1), "reset mixer ch1")
    send(client, CLEAR(video_channel=1), "clear ch1")


# ---------------------------------------------------------------------------
# Scenario 8  -  Blend modes: layer compositing with MIXER_BLEND
# ---------------------------------------------------------------------------

def scenario_blend_modes(client: Client) -> None:
    """
    Stack three solid-colour layers and cycle through MIXER_BLEND modes
    to demonstrate how CasparCG composites layers together.  Uses built-in
    colour producers so no media files are required.

    Blend modes in order: normal -> screen -> add -> multiply -> overlay -> normal.
    """
    section("Scenario 8  -  Blend Modes & Layer Compositing")

    # Primary layer: deep navy fills the whole screen.
    send(client, PLAY(video_channel=1, layer=10, clip="#0d2b6b"), "layer 10: navy bg")

    # Second layer: bright red, covering the right two-thirds.
    send(client, PLAY(video_channel=1, layer=20, clip="#c62828"), "layer 20: red")
    send(
        client,
        MIXER_FILL(video_channel=1, layer=20, x=0.25, y=0.0, x_scale=0.75, y_scale=1.0),
        "fill l20 right 3/4",
    )
    send(client, MIXER_OPACITY(video_channel=1, layer=20, opacity=0.8), "l20 opacity 80%")

    # Third layer: golden yellow, a centered square.
    send(client, PLAY(video_channel=1, layer=30, clip="#f9a825"), "layer 30: gold")
    send(
        client,
        MIXER_FILL(video_channel=1, layer=30, x=0.2, y=0.15, x_scale=0.6, y_scale=0.7),
        "fill l30 center",
    )
    send(client, MIXER_OPACITY(video_channel=1, layer=30, opacity=0.75), "l30 opacity 75%")

    wait(1.5, "base composition")

    # Cycle through blend modes on the gold layer.
    for mode in ("screen", "add", "multiply", "overlay", "normal"):
        send(
            client,
            MIXER_BLEND(video_channel=1, layer=30, blend=mode),
            f"blend: {mode}",
        )
        wait(1.2, f"showing {mode}")

    # Cross-fade: fade the red layer out while expanding the gold to fill.
    send(
        client,
        MIXER_OPACITY(video_channel=1, layer=20, opacity=0.0, duration=30, tween="linear"),
        "fade out red (30 frames)",
    )
    send(
        client,
        MIXER_FILL(
            video_channel=1, layer=30,
            x=0.0, y=0.0, x_scale=1.0, y_scale=1.0,
            duration=30, tween="easeinoutcubic",
        ),
        "expand gold to full",
    )

    wait(2.0)

    send(client, MIXER_CLEAR(video_channel=1), "reset mixer")
    send(client, CLEAR(video_channel=1), "clear channel")


# ---------------------------------------------------------------------------
# Scenario 9  -  Async client: concurrent multi-channel queries
# ---------------------------------------------------------------------------

async def scenario_async(host: str = "127.0.0.1", port: int = 5250) -> None:
    section("Scenario 9  -  Async Client: Concurrent Queries")

    client = ClientAsync()
    try:
        await client.connect(host=host, port=port)
    except Exception as exc:
        print(f"  Connection failed: {exc}")
        return

    async def query(label: str, command):
        print(f"  [{label}] >> {str(command).strip()}")
        try:
            resp = await client.send(command)
            print(f"  [{label}] << {resp.code} {resp.code_description}")
            return resp
        except AMCPResponseError as exc:
            print(f"  [{label}] !! {exc.response.code}")
            return exc.response
        except Exception as exc:
            print(f"  [{label}] !! {type(exc).__name__}: {exc}")
            return None

    # Fire three queries concurrently -- ClientAsync serialises them safely
    # with an asyncio.Lock so they don't interleave on the single connection.
    results = await asyncio.gather(
        query("version",  VERSION()),
        query("info",     INFO(video_channel=1)),
        query("cg-info",  CG_INFO(video_channel=1)),
        return_exceptions=True,
    )

    ok = sum(1 for r in results if isinstance(r, ResponseBase) and r.ok)
    print(f"  {ok}/{len(results)} queries succeeded.")

    # ClientAsync has no disconnect() -- the connection closes when the object
    # goes out of scope at the end of the coroutine.


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    host, port = "127.0.0.1", 5250

    print("amcp-pylib demo   -   CasparCG AMCP scenarios")
    print(f"Target server: {host}:{port}")

    client = Client()
    try:
        # timeout=10 prevents infinite recv() hangs on unexpected server responses.
        client.connect(host=host, port=port, timeout=10.0)
        print("Connected.\n")
    except Exception as exc:
        print(f"\nCould not connect to CasparCG ({exc}).")
        print("Running in offline mode  -  commands are serialised and printed but not sent.\n")
        _run_offline_preview()
        return

    clip = scenario_server_discovery(client)

    scenarios = [
        lambda: scenario_simple_playback(client, clip),
        lambda: scenario_transitions(client, clip),
        lambda: scenario_mixer_color(client, clip),
        lambda: scenario_mixer_spatial(client, clip),
        lambda: scenario_cg_templates(client),
        lambda: scenario_multilayer(client, clip),
        lambda: scenario_blend_modes(client),
    ]

    for fn in scenarios:
        try:
            fn()
        except KeyboardInterrupt:
            print("\nInterrupted.")
            break
        except Exception as exc:
            print(f"  [!] Scenario failed: {exc}")

    # Async scenario uses queries only, no media needed.
    try:
        asyncio.run(scenario_async(host=host, port=port))
    except Exception as exc:
        print(f"  [!] Async scenario failed: {exc}")

    print(f"\n{SEPARATOR}")
    print("  Demo complete.")
    print(SEPARATOR)


# ---------------------------------------------------------------------------
# Offline preview  -  show serialised AMCP strings without a live server
# ---------------------------------------------------------------------------

def _run_offline_preview() -> None:
    """Print the AMCP wire format for a selection of commands."""
    section("Offline preview  -  serialised AMCP commands")

    samples = [
        PING(token="hello"),
        LOADBG(channel=1, clip="commercials/spot_30s", loop="LOOP", transition="MIX",
               duration=25, tween="easeinoutcubic"),
        PLAY(video_channel=1),
        MIXER_FILL(video_channel=1, layer=20, x=0.5, y=0.0, x_scale=0.5, y_scale=1.0,
                   duration=30, tween="easeinback"),
        MIXER_OPACITY(video_channel=1, layer=20, opacity=0.0),
        MIXER_OPACITY(video_channel=1, layer=20, opacity=1.0, duration=50, tween="easeinoutcubic"),
        MIXER_COMMIT(video_channel=1),
        MIXER_PERSPECTIVE(
            video_channel=1, layer=20,
            top_left_x=0.1,    top_left_y=0.1,
            top_right_x=0.9,   top_right_y=0.05,
            bottom_right_x=0.92, bottom_right_y=0.88,
            bottom_left_x=0.08, bottom_left_y=0.92,
            duration=25, tween="linear",
        ),
        CG_ADD(video_channel=1, layer=20, cg_layer=1, template="lower_thirds/standard",
               play_on_load=1,
               data='<templateData><componentData id="f0"><data id="text" value="Jane Doe"/></componentData></templateData>'),
        CG_UPDATE(video_channel=1, layer=20, cg_layer=1,
                  data='<templateData><componentData id="f0"><data id="text" value="John Smith"/></componentData></templateData>'),
        CG_INVOKE(video_channel=1, layer=20, cg_layer=1, method="outro"),
        DATA_STORE(name="guests/presenter", data="<templateData/>"),
        MIXER_BLEND(video_channel=1, layer=20, blend="screen"),
        PLAY(video_channel=1, layer=10, clip="#0d2b6b"),
        PLAY(video_channel=1, layer=20, clip="#c62828"),
        SWAP(channel1=1, layer1=10, channel2=1, layer2=20),
        CLEAR(video_channel=1),
    ]

    for cmd in samples:
        print(f"  {str(cmd).strip()}")

    section("Request-ID tagging (for multi-client / async workflows)")
    for i, clip in enumerate(["news/intro", "commercials/spot_30s", "outro/sign_off"]):
        cmd = PLAY(video_channel=1, clip=clip).with_request_id(f"req-{i:03d}")
        print(f"  {str(cmd).strip()}")


if __name__ == "__main__":
    main()
