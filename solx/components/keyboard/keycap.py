
"""Keycap creation module for mechanical keyboards.

This module provides functionality to create keycaps with stems for mechanical keyboards,
specifically designed for Choc V2 switches. It combines keycap tops with stems to create
complete keycap assemblies.
"""

# %%
from solx.components.keyboard.keycap_top import create_keycap_top
from solx.components.keyboard.stem_chocv2 import create_chocv2_stem
from solx.core.base import SolxObject


def create_keycap_with_stem(
    top_offset_h = 1.5,
    bottom_w = 16.0,
    bottom_d = 16.0,
    top_w = 16.0,
    top_d = 16.0,
    height = 5.0,
    bottom_radius = 3,
    top_radius = 3,
    top_dx = 0.0,
    top_dy = 0.0,
    top_rx_deg = 0.0,
    top_ry_deg = 0.0,
    top_rz_deg = 0.0,
    dimple = 0.0,
    segments = 64,
    offset_wd = 1,
    offset_h_ratio = 0.5,
    inverted = False
) -> SolxObject:
    """Create a keycap with a Choc V2 stem attached.

    Args:
        top_offset_h (float): Height offset to position the keycap top above the stem.
        bottom_w (float): Width of the bottom face of the keycap top.
        bottom_d (float): Depth of the bottom face of the keycap top.
        top_w (float): Width of the top face of the keycap top.
        top_d (float): Depth of the top face of the keycap top.
        height (float): Height of the keycap top.
        bottom_radius (float): Radius of the bottom face corners of the keycap top.
        top_radius (float): Radius of the top face corners of the keycap top.
        top_dx (float): X offset of the top face of the keycap top.
        top_dy (float): Y offset of the top face of the keycap top.
        top_rx_deg (float): Rotation around X axis of the top face in degrees.
        top_ry_deg (float): Rotation around Y axis of the top face in degrees.
        top_rz_deg (float): Rotation around Z axis of the top face in degrees.
        dimple (float): Depth of the dimple on the top face of the keycap top.
        segments (int): Number of segments for rounded corners of the keycap top.
        offset_wd (float): Wall thickness of the keycap top.
        offset_h_ratio (float): Ratio of height to offset the inner hollow part.
        inverted (bool): If True, creates an inverted keycap (upside down).

    Returns:
        SolxObject: The keycap with Choc V2 stem attached.
    """
    keycap_top = create_keycap_top(
        bottom_w = bottom_w,
        bottom_d = bottom_d,
        top_w = top_w,
        top_d = top_d,
        height = height,
        bottom_radius = bottom_radius,
        top_radius = top_radius,
        top_dx = top_dx,
        top_dy = top_dy,
        top_rx_deg = top_rx_deg,
        top_ry_deg = top_ry_deg,
        top_rz_deg = top_rz_deg,
        dimple = dimple,
        segments = segments,
        offset_wd = offset_wd,
        offset_h_ratio = offset_h_ratio)
    stem = create_chocv2_stem(inverted=False)
    keycap_top = keycap_top.translate((0, 0, top_offset_h))
    keycap = keycap_top + stem
    if inverted:
        keycap = keycap.rotate_x(180)
    return keycap


# %%
if __name__ == "__main__":
    keycap = create_keycap_with_stem()
    keycap.render()
    # dst_dir_path = "/home/uedam/dev/solx/examples/output_stl"
    # keycap.save_stl(f"{dst_dir_path}/keycap_chocv2.stl")
# %%
