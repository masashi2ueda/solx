
"""Keycap creation module for mechanical keyboards.

This module provides functionality to create keycaps with stems for mechanical keyboards,
specifically designed for Choc V2 switches. It combines keycap tops with stems to create
complete keycap assemblies.
"""
# %%
import numpy as np

from solx.components.keyboard.keycap_top import create_keycap_top
from solx.components.keyboard.stem_chocv2 import ChocV2Stem
from solx.core.base import SolxObject
from solx.primitives.cylinder import Cylinder


def create_keycap_with_stem(
    keycap_top,
    top_offset_x,
    top_offset_y,
    top_offset_z,
    inverted = False,
    stem_radius = 2.765,
) -> SolxObject:
    stem_core = ChocV2Stem(stem_radius=stem_radius)
    stem_cylinder = Cylinder(radius=stem_core.stem_radius,height=top_offset_z)
    keycap_top = keycap_top.translate((top_offset_x, top_offset_y, top_offset_z))
    keycap = keycap_top + stem_cylinder
    keycap -= stem_core.cross_slot
    if inverted:
        keycap = keycap.rotate_x(180)
    return keycap
# %%
LR = 'R'

K_MGN_Y = 17.0
BASE_KEY_SIZE = BASE_W = BASE_D = 15.5
BOTTOM_W = BASE_KEY_SIZE
BOTTOM_D = BASE_KEY_SIZE
TOP_W = BASE_KEY_SIZE
TOP_D = BASE_KEY_SIZE
K_BLANK_Y = K_MGN_Y - BASE_KEY_SIZE

def create_keycap(
    d_keytop_size_d=0.0,
    d_top_offset_y=0.0,
    key_cap_dh=0.0,
    top_rx_deg=0.0,
):
    d_keytop_size_d = d_keytop_size_d
    d_top_offset_y = - d_top_offset_y
    key_cap_top = create_keycap_top(
        bottom_w=BOTTOM_W,
        bottom_d=BOTTOM_D + d_keytop_size_d,
        top_w=TOP_W,
        top_d=TOP_D + d_keytop_size_d,
        height=5.0 + key_cap_dh,
        bottom_radius=3,
        top_radius=3,
        top_dx=0.0,
        top_dy=0.0,
        top_rx_deg=top_rx_deg,
        top_ry_deg=0.0,
        top_rz_deg=0.0,
        is_dimple=True,
        dimple_radius=40.0,
        dimple_size=3.0,
        dimple_segments=1000,
        is_sohw_dimple=False,
        segments=64,
    )
    dst = create_keycap_with_stem(
        keycap_top=key_cap_top,
        top_offset_x=0.0,
        top_offset_y=d_top_offset_y,
        top_offset_z=5.0,
        inverted=False,
        stem_radius=2.755,
    )
    return dst

dy1 = 5.0

d_keytop_d = - dy1 / 3
hd1 = 5.0
hd2 = 2.0
rdx1 = np.atan2(hd1-hd2, TOP_D) * 180 / np.pi
rdx2 = np.atan2(hd2, TOP_D) * 180 / np.pi + 5
k1_org = create_keycap(
    d_top_offset_y=dy1,
    key_cap_dh=hd1,
    top_rx_deg=rdx1,)
k2_org = create_keycap(
    d_top_offset_y=-2.5 * d_keytop_d,
    d_keytop_size_d=d_keytop_d,
    key_cap_dh=hd2,
    top_rx_deg=rdx2,)
k3_org = create_keycap(
    d_top_offset_y=-1.5 * d_keytop_d,
    d_keytop_size_d=d_keytop_d)
k4_org = create_keycap(
    d_top_offset_y=-0.5 * d_keytop_d,
    d_keytop_size_d=d_keytop_d)

def mytranslate(obj, x, y):
    return obj.translate((x , -y, 0))
k1 = mytranslate(k1_org, -23.0, -K_MGN_Y)
k2 = mytranslate(k2_org, -23.0, 0.0)
k3 = mytranslate(k3_org, -23.0, K_MGN_Y)
k4 = mytranslate(k4_org, -23.0, 2 * K_MGN_Y)

if LR == "L":
    k1 = k1.mirror((1,0,0))
    k2 = k2.mirror((1,0,0))
    k3 = k3.mirror((1,0,0))
    k4 = k4.mirror((1,0,0))

dst = k1 + k2 + k3 + k4
if True:
    dst += dst.translate((17, 0, 0.0))
dst.render()
# %%
from solx.config import EnvConfig

# k1.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_{rz}_k1_{int(stem_radius*1000)}.stl")
k1.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_k1.stl")
k2.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_k2.stl")
k3.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_k3.stl")
k4.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_k4.stl")



# %%
LR = "R"
# LR = "L"
# offset_x = 200
# offset_y = 100
offset_x = 0
offset_y = 0

base_z = 5.0
rz = 0

# stem_radius = 2.770
stem_radius = 2.755

w = 14.5
d = 14.5
if rz == 45:
    w = d = 12.0
def mytranslate(obj, x, y):
    return obj.translate((x , -y, 0))


k1_d_mgn = 0.0
k1_org = create_keycap_with_stem(
    top_offset_z = base_z + 4.0,
    top_offset_y = -4.0,
    dimple=0.2,
    top_rx_deg=8,
    top_rz_deg=rz,
    bottom_w = w,
    bottom_d = d-k1_d_mgn,
    top_w = w,
    top_d = d-k1_d_mgn,
    stem_radius = stem_radius,
)

k2_org = create_keycap_with_stem(
    top_offset_z = base_z,
    top_offset_y = -2.5,
    dimple=0.2,
    top_rx_deg=-3,
    top_rz_deg=rz,
    bottom_w = w,
    bottom_d = d,
    top_w = w,
    top_d = d,
    stem_radius = stem_radius,
)

k3_org = create_keycap_with_stem(
    top_offset_z = base_z,
    top_offset_y = -1.5,
    dimple=0.2,
    top_rx_deg=-3,
    top_rz_deg=rz,
    bottom_w = w,
    bottom_d = d,
    top_w = w,
    top_d = d,
    stem_radius = stem_radius,
)

k4_org = create_keycap_with_stem(
    top_offset_z = base_z,
    top_offset_y = 0.0,
    dimple=0.2,
    top_rx_deg=-3,
    top_rz_deg=rz,
    bottom_w = w,
    bottom_d = d,
    top_w = w,
    top_d = d,
    stem_radius = stem_radius,
)

k1 = mytranslate(k1_org, -23.0, -17.0)
k2 = mytranslate(k2_org, -23.0, 0.0)
k3 = mytranslate(k3_org, -23.0, 17.0)
k4 = mytranslate(k4_org, -23.0, 34.0)

if LR == "L":
    k1 = k1.mirror((1,0,0))
    k2 = k2.mirror((1,0,0))
    k3 = k3.mirror((1,0,0))
    k4 = k4.mirror((1,0,0))

dst = k1 + k2 + k3 + k4
if True:
    dst += dst.translate((17, 0, 0.0))
dst.render()
# %%
from solx.config import EnvConfig

# k1.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_{rz}_k1_{int(stem_radius*1000)}.stl")
k1.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_{rz}_k1.stl")
k2.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_{rz}_k2.stl")
k3.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_{rz}_k3.stl")
k4.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_{rz}_k4.stl")

# %%
o_height = 4.0
o_dimple = 0.1
o_base_z = 4.5
o1_org = create_keycap_with_stem(
    top_offset_z = o_base_z,
    top_offset_y = -3.0,
    dimple=o_dimple,
    top_rx_deg=5,
    top_rz_deg=20,
    bottom_w = w,
    bottom_d = d,
    top_w = w,
    top_d = 20.0,
    stem_radius = stem_radius,
    height=o_height,
)

o2_org = create_keycap_with_stem(
    top_offset_z = base_z,
    top_offset_y = -3.0,
    dimple=0.2,
    top_rx_deg=5,
    top_rz_deg=0,
    bottom_w = w,
    bottom_d = d,
    top_w = w,
    top_d = 16.0,
    stem_radius = stem_radius,
)

o3_org = create_keycap_with_stem(
    top_offset_z = base_z,
    top_offset_y = -0.0,
    dimple=0.2,
    top_rx_deg=5,
    top_rz_deg=-40,
    bottom_w = w,
    bottom_d = d,
    top_w = w,
    top_d = 14.0,
    stem_radius = stem_radius,
)
off_x = 100
o1 = mytranslate(o1_org, -109.0+off_x, 40.0)
o2 = mytranslate(o2_org, -92.0+off_x, 34.0)
o3 = mytranslate(o3_org, -75.0+off_x, 34.0)


if LR == "L":
    o1 = o1.mirror((1,0,0))
    o2 = o2.mirror((1,0,0))
    o3 = o3.mirror((1,0,0))


dst = o1 + o2 + o3
dst.render()
# set_swith_diode(71, -109.0 + offset_x, 40.0 + offset_y)
# set_swith_diode(81, -92.0 + offset_x, 34.0 + offset_y)
# if LR == "L":
#     set_swith_diode(91, -75.0 + offset_x, 34.0 + offset_y)

# %%
from solx.config import EnvConfig

o1.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_o1.stl")
o2.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_o2.stl")
o3.save_stl(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/{LR}_o3.stl")
# %%
# set_swith_diode(21, -40.0 + offset_x, -32.0 + offset_y)
# set_swith_diode(22, -40.0 + offset_x, -15.0 + offset_y)
# set_swith_diode(23, -40.0 + offset_x, 2.0 + offset_y)
# if LR == "L":
#     set_swith_diode(24, -40.0 + offset_x, 19.0 + offset_y)

# set_swith_diode(31, -57.0 + offset_x, -35.0 + offset_y)
# set_swith_diode(32, -57.0 + offset_x, -18.0 + offset_y)
# set_swith_diode(33, -57.0 + offset_x, -1.0 + offset_y)
# if LR == "L":
#     set_swith_diode(34, -57.0 + offset_x, 16.0 + offset_y)

# set_swith_diode(41, -74.0 + offset_x, -23.0 + offset_y)
# set_swith_diode(42, -74.0 + offset_x, -6.0 + offset_y)
# set_swith_diode(43, -74.0 + offset_x, 11.0 + offset_y)

# set_swith_diode(51, -91.0 + offset_x, -17.0 + offset_y)
# set_swith_diode(52, -91.0 + offset_x, 0.0 + offset_y)
# set_swith_diode(53, -91.0 + offset_x, 17.0 + offset_y)

# set_swith_diode(61, -108.0 + offset_x, 3.0 + offset_y)
# set_swith_diode(62, -108.0 + offset_x, 20.0 + offset_y)

# set_swith_diode(71, -109.0 + offset_x, 40.0 + offset_y)
# set_swith_diode(81, -92.0 + offset_x, 34.0 + offset_y)
# if LR == "L":
#     set_swith_diode(91, -75.0 + offset_x, 34.0 + offset_y)
# if LR == "L":
#     dst = dst.mirror((1,0,0))

dst.render()
# dst.save_scad(f"{EnvConfig.OUTPUT_STL_DIR_PATH}/test.scad")
# %%
