
"""Keycap creation module for mechanical keyboards.

This module provides functionality to create keycaps with stems for mechanical keyboards,
specifically designed for Choc V2 switches. It combines keycap tops with stems to create
complete keycap assemblies.
"""
# %%
from solx import CenterType, Cube
from solx.components.keyboard.keycap_top import create_keycap_top
from solx.components.keyboard.stem_chocv2 import create_chocv2_stem
from solx.core.base import SolxObject


def create_keycap_with_stem(
    top_offset_x = 0.0,
    top_offset_y = 0.0,
    top_offset_z = 1.5,
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
    home_bump = False,
    home_bump_radius = 0.8,
    home_bump_height = 0.4,
    home_bump_length = 2.5,
    home_bump_offset_x = 0.0,
    home_bump_offset_y = 0.0,
    home_bump_offset_y_ratio = -0.8,
    segments = 64,
    offset_wd = 1,
    offset_h_ratio = 0.5,
    inverted = False
) -> SolxObject:
    """Create a keycap with a Choc V2 stem attached.

    Args:
        top_offset_x (float): X offset of the keycap top from the stem.
        top_offset_y (float): Y offset of the keycap top from the stem.
        top_offset_z (float): Z offset of the keycap top from the stem.
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
        home_bump (bool): If True, add a small bump for home position.
        home_bump_radius (float): Radius of the home position bump.
        home_bump_height (float): Height of the home position bump.
        home_bump_length (float): Length of the home position bump.
        home_bump_offset_x (float): X offset of the bump on the top face.
        home_bump_offset_y (float): Y offset of the bump on the top face.
        home_bump_offset_y_ratio (float|None): If set, overrides Y offset using a ratio
            of half the top depth (-1.0: front edge, 0: center, 1.0: back edge).
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
        home_bump = home_bump,
        home_bump_radius = home_bump_radius,
        home_bump_height = home_bump_height,
        home_bump_length = home_bump_length,
        home_bump_offset_x = home_bump_offset_x,
        home_bump_offset_y = home_bump_offset_y,
        home_bump_offset_y_ratio = home_bump_offset_y_ratio,
        segments = segments,
        offset_wd = offset_wd,
        offset_h_ratio = offset_h_ratio)
    stem = create_chocv2_stem(inverted=False)
    clip_z = top_offset_z
    stem_clipper = Cube(size=(200, 200, 200), center=CenterType.BOTTOM_CENTER).translate(
        (0, 0, clip_z)
    )
    stem = stem - stem_clipper
    keycap_top = keycap_top.translate((top_offset_x, top_offset_y, top_offset_z))
    keycap = keycap_top + stem
    if inverted:
        keycap = keycap.rotate_x(180)
    return keycap


if __name__ == "__main__":
    keycap = create_keycap_with_stem()
    # keycap.render()
    from solx.config import EnvConfig
    keycap.save_scad(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/test.scad")
    # dst_dir_path = "/home/uedam/dev/solx/examples/output_stl"
    # keycap.save_stl(f"{dst_dir_path}/keycap_chocv2.stl")
# %%
# キーキャップの高さ
top_offset_z = 3.5
# キーキャップの前への出具合
top_offset_y = -5.0
# ディンプルの深さ
dimple = 0.2
# キーキャップの傾き
top_rx_deg = 10
keycap = create_keycap_with_stem(
    top_offset_z = top_offset_z,
    top_offset_y = top_offset_y,
    dimple=dimple,
    top_rx_deg=top_rx_deg,
)
from solx.config import EnvConfig
keycap.save_scad(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/test.scad")
# %%
from solx.primitives import Cube
LR = "L"
dst = Cube(size=(10, 10, 10))
# key switch space
def set_swith_diode(index: int, x: float, y: float):
    # global top_case, cx, cy
    global dst
    mgn = 0.3
    key_h = 15.0 + mgn
    key_w = 15.0 + mgn
    # inner_cube = Cube(size=(key_h, key_w, 100))
    base_z = 1.0
    # キーキャップの高さ
    top_offset_z = base_z + 0.0
    # キーキャップの前への出具合
    top_offset_y = 0.0
    # ディンプルの深さ
    dimple = 0.2
    # キーキャップの傾き
    top_rx_deg = 10
    ci = int(index/10)
    ri = index%10
    if ri == 1:
        top_offset_y = -1.0
        top_offset_z = base_z + 3.5
        top_rx_deg = 5
    if ri == 2:
        top_offset_y = 0.0
        top_offset_z = base_z + 2.0
        top_rx_deg = 2

    keycap = create_keycap_with_stem(
        top_offset_z = top_offset_z,
        top_offset_y = top_offset_y,
        dimple=dimple,
        top_rx_deg=top_rx_deg,
        home_bump=True
    )

    inner_cube = keycap.translate((x, -y, 0))
    dst = dst + inner_cube

offset_x = 200
offset_y = 100
set_swith_diode(11, -23.0 + offset_x, -17.0 + offset_y)
set_swith_diode(12, -23.0 + offset_x, 0.0 + offset_y)
set_swith_diode(13, -23.0 + offset_x, 17.0 + offset_y)
set_swith_diode(14, -23.0 + offset_x, 34.0 + offset_y)

set_swith_diode(21, -40.0 + offset_x, -32.0 + offset_y)
set_swith_diode(22, -40.0 + offset_x, -15.0 + offset_y)
set_swith_diode(23, -40.0 + offset_x, 2.0 + offset_y)
if LR == "L":
    set_swith_diode(24, -40.0 + offset_x, 19.0 + offset_y)

set_swith_diode(31, -57.0 + offset_x, -35.0 + offset_y)
set_swith_diode(32, -57.0 + offset_x, -18.0 + offset_y)
set_swith_diode(33, -57.0 + offset_x, -1.0 + offset_y)
if LR == "L":
    set_swith_diode(34, -57.0 + offset_x, 16.0 + offset_y)

set_swith_diode(41, -74.0 + offset_x, -23.0 + offset_y)
set_swith_diode(42, -74.0 + offset_x, -6.0 + offset_y)
set_swith_diode(43, -74.0 + offset_x, 11.0 + offset_y)

set_swith_diode(51, -91.0 + offset_x, -17.0 + offset_y)
set_swith_diode(52, -91.0 + offset_x, 0.0 + offset_y)
set_swith_diode(53, -91.0 + offset_x, 17.0 + offset_y)

set_swith_diode(61, -108.0 + offset_x, 3.0 + offset_y)
set_swith_diode(62, -108.0 + offset_x, 20.0 + offset_y)

set_swith_diode(71, -109.0 + offset_x, 40.0 + offset_y)
set_swith_diode(81, -92.0 + offset_x, 34.0 + offset_y)
if LR == "L":
    set_swith_diode(91, -75.0 + offset_x, 34.0 + offset_y)

if LR == "L":
    dst = dst.mirror((1,0,0))


dst.save_scad(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/test.scad")
# %%
