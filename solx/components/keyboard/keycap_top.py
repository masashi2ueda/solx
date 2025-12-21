# %%
import solid

from solx import SolxObject
from solx.primitives import Cylinder, RoundedCube
from solx.primitives.types import CenterType

SMALL_VAL = 1e-5


# def create_keycap_top(
#     height = 2.0,
#     bottom_w = 3.0,
#     bottom_d = 3.0,
#     bottom_radius = 0.5,
#     top_w = 2.0,
#     top_d = 2.0,
#     top_radius = 0.3,
#     top_dx = 0.0,
#     top_dy = 0.1,
#     top_rx_deg = 5.0,
#     top_ry_deg = 0.0,
#     top_rz_deg = 0.0,
#     dimple = 0.1,
#     segments = 64,
#     subt_scale = 0.98,
# )-> SolxObject:

def create_keycap_base(
    bottom_w = 15.0,
    bottom_d = 15.0,
    top_w = 15.0,
    top_d = 15.0,
    height = 2.0,

    bottom_radius = 3,
    top_radius = 3,

    top_dx = 0.0,
    top_dy = 0.0,
    top_rx_deg = 0.0,
    top_ry_deg = 0.0,
    top_rz_deg = 0.0,
    dimple = 0.1,
    segments = 64)-> SolxObject:
    bottom_cube = RoundedCube(
        size=[bottom_w, bottom_d, SMALL_VAL],
        radius=bottom_radius,
        center=CenterType.BOTTOM_CENTER,
        segments=segments
    )

    top_cube = RoundedCube(
        size=[top_w, top_d, SMALL_VAL],
        radius=top_radius,
        center=CenterType.BOTTOM_CENTER,
        segments=segments
    )

    top_cube = top_cube.translate((top_dx, top_dy, height))
    top_cube = top_cube.rotate_x(top_rx_deg)
    top_cube = top_cube.rotate_y(top_ry_deg)
    top_cube = top_cube.rotate_z(top_rz_deg)
    key_cap_node = solid.hull()(
        bottom_cube.node, top_cube.node
    )
    key_cap = SolxObject(key_cap_node)

    cyl_h = max(bottom_d, bottom_w) * 2

    dip_radius = top_w / 2
    cyl = Cylinder(
        radius=dip_radius,
        height=cyl_h,
        center=CenterType.CENTER)
    cyl = cyl.rotate_x(90)
    cyl = cyl.scale([1.0, 1.0, dimple])
    cyl = cyl.translate((top_dx, top_dy, height))
    cyl = cyl.rotate_x(top_rx_deg)
    cyl = cyl.rotate_y(top_ry_deg)
    cyl = cyl.rotate_z(top_rz_deg)

    dst = key_cap - cyl
    return dst


# %%
def create_keycap_top(
    bottom_w = 15.0,
    bottom_d = 15.0,
    top_w = 15.0,
    top_d = 15.0,
    height = 2.0,
    bottom_radius = 3,
    top_radius = 3,
    top_dx = 0.0,
    top_dy = 0.0,
    top_rx_deg = 0.0,
    top_ry_deg = 0.0,
    top_rz_deg = 0.0,
    dimple = 0.1,
    segments = 64,
    offset_wd = 3,
    offset_h_ratio = 0.5,
    ) -> SolxObject:
    keycap_outer = create_keycap_base(
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
    )

    offset_h = height * offset_h_ratio
    keycap_innter = create_keycap_base(
        bottom_w = bottom_w - offset_wd,
        bottom_d = bottom_d - offset_wd,
        top_w = top_w - offset_wd,
        top_d = top_d - offset_wd,
        height = height - offset_h,
        bottom_radius = bottom_radius,
        top_radius = top_radius,
        top_dx = top_dx,
        top_dy = top_dy,
        top_rx_deg = top_rx_deg,
        top_ry_deg = top_ry_deg,
        top_rz_deg = top_rz_deg,
        dimple = dimple,
        segments = segments,
    )

    key_cap = keycap_outer - keycap_innter
    key_cap.render()
    return key_cap
# %%
