# %%
import solid

from solx import SolxObject
from solx.primitives import Cylinder, RoundedCube
from solx.primitives.types import CenterType

SMALL_VAL = 1e-5

class KeyCap:
    def __init__(
        self,
        height = 2.0,
        bottom_w = 3.0,
        bottom_d = 3.0,
        bottom_radius = 0.5,
        top_w = 2.0,
        top_d = 2.0,
        top_radius = 0.3,
        top_dx = 0.0,
        top_dy = 0.1,
        top_rx_deg = 5.0,
        top_ry_deg = 0.0,
        top_rz_deg = 0.0,
        dimple = 0.1,
        segments = 64,
        subt_scale = 0.98,
    )-> SolxObject:
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

        key_cap = key_cap - cyl

        key_cap_sub = key_cap.scale(subt_scale)
        key_cap = key_cap - key_cap_sub
        return key_cap
key_cap.render()
# %%
