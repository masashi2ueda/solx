# %%
"""Choc v2 low-profile mechanical keyboard switch cutout and plate primitives.

This module provides builders for PCB/plate cutouts compatible with the
Kailh Choc v2 low-profile switch footprint, including support for both
pin-style and socket-style mounting holes.
"""
from typing import Literal

from solx.primitives import Cube, Cylinder

HoleType = Literal["pin", "socket"]

KEY_PITCH_MM = 17.0
CENTER_HOLE_RADIUS_MM = 5.0 / 2
PIN_SLOT_WIDTH_MM = 1.5
PIN_SLOT_DEPTH_MM = 1.0
SOCKET_HOLE_RADIUS_MM = 1.7
SOCKET1_OFFSET = (0.0, -5.90, 0.0)
SOCKET2_OFFSET = (-5.00, -3.80, 0.0)
CUTOUT_EXTRA_HEIGHT_MM = 1.0


def build_choc_v2_switch_cutout(thickness: float, hole_type: HoleType) -> Cube:
    """Build a Choc v2 switch cutout geometry for a plate of the given thickness.

    Creates a central circular cutout for the switch stem, plus either a pair of
    rectangular pin slots (for direct PCB mounting) or a pair of circular socket
    holes (for hot-swap socket mounting).

    Args:
        thickness: Plate thickness in millimetres. The cutout height is extended
            by ``CUTOUT_EXTRA_HEIGHT_MM`` to ensure a clean through-hole.
        hole_type: ``"pin"`` for rectangular pin slots, ``"socket"`` for circular
            hot-swap socket holes.

    Returns:
        A solid geometry object representing the combined switch cutout.

    Raises:
        ValueError: If *hole_type* is not ``"pin"`` or ``"socket"``.
    """
    cutout_height = thickness + CUTOUT_EXTRA_HEIGHT_MM
    cutout = Cylinder(radius=CENTER_HOLE_RADIUS_MM, height=cutout_height)

    if hole_type == "pin":
        pin_slot = Cube(size=(PIN_SLOT_WIDTH_MM, PIN_SLOT_DEPTH_MM, cutout_height))
        cutout += pin_slot.translate(SOCKET1_OFFSET)
        cutout += pin_slot.translate(SOCKET2_OFFSET)
    elif hole_type == "socket":
        socket_hole = Cylinder(radius=SOCKET_HOLE_RADIUS_MM, height=cutout_height)
        cutout += socket_hole.translate(SOCKET1_OFFSET)
        cutout += socket_hole.translate(SOCKET2_OFFSET)
    else:
        raise ValueError(f"Invalid hole_type: {hole_type}. Use 'pin' or 'socket'.")

    return cutout


def build_choc_v2_key_plate(thickness: float, hole_type: HoleType) -> Cube:
    """Build a single Choc v2 key plate tile with the switch cutout subtracted.

    The tile is a square with side length ``KEY_PITCH_MM`` (17 mm standard Choc
    pitch) and the specified *thickness*.  The switch cutout returned by
    :func:`build_choc_v2_switch_cutout` is boolean-subtracted from the tile.

    Args:
        thickness: Plate thickness in millimetres.
        hole_type: ``"pin"`` or ``"socket"`` — passed through to
            :func:`build_choc_v2_switch_cutout`.

    Returns:
        A solid geometry object representing one key plate unit.
    """
    key_plate = Cube(size=(KEY_PITCH_MM, KEY_PITCH_MM, thickness))
    key_plate -= build_choc_v2_switch_cutout(thickness=thickness, hole_type=hole_type)
    return key_plate


def render_preview_models(thickness: float = 1.0) -> None:
    """Render all Choc v2 preview models for visual inspection.

    Renders the switch cutout and key plate geometries for both ``"pin"`` and
    ``"socket"`` hole types using the OpenSCAD backend.

    Args:
        thickness: Plate thickness in millimetres used for all preview models.
            Defaults to ``1.0``.
    """
    build_choc_v2_switch_cutout(thickness, "pin").render()
    build_choc_v2_switch_cutout(thickness, "socket").render()
    build_choc_v2_key_plate(thickness, "pin").render()
    build_choc_v2_key_plate(thickness, "socket").render()


if __name__ == "__main__":
    render_preview_models()

# %%
