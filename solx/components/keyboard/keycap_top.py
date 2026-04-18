# %%
"""Docstring for solx.components.keyboard.keycap_top."""
import solid

from solx import SolxObject
from solx.primitives import Cylinder, RoundedCube
from solx.primitives.types import CenterType

SMALL_VAL = 1e-5
LARGE_VAL = 100
EPS = 1e-3


def create_keycap_top(
    bottom_w,
    bottom_d,
    top_w,
    top_d,
    height,
    bottom_radius,
    top_radius,
    top_dx,
    top_dy,
    top_rx_deg,
    top_ry_deg,
    top_rz_deg,
    is_dimple,
    dimple_radius,
    dimple_size,
    segments,
    dimple_segments,
    is_sohw_dimple = False,
    is_bump = False
    ) -> SolxObject:
    """Create a basic keycap shape using hull between two rounded cubes."""
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

    top_cube = top_cube.rotate_x(top_rx_deg)
    top_cube = top_cube.rotate_y(top_ry_deg)
    top_cube = top_cube.rotate_z(top_rz_deg)
    top_cube = top_cube.translate((top_dx, top_dy, height))

    key_cap_node = solid.hull()(
        bottom_cube.node, top_cube.node
    )
    key_cap = SolxObject(key_cap_node)

    if is_dimple:
        cyl = Cylinder(
            radius=dimple_radius,
            height=LARGE_VAL,
            center=CenterType.CENTER,
            segments=dimple_segments)
        cyl = cyl.rotate_x(90)
        cyl_dh = height + dimple_radius - dimple_size
        cyl = cyl.translate((top_dx, top_dy, cyl_dh))
        cyl = cyl.rotate_x(top_rx_deg)
        cyl = cyl.rotate_y(top_ry_deg)
        cyl = cyl.rotate_z(top_rz_deg)
        if is_sohw_dimple:
            key_cap = key_cap + cyl
        else:
            key_cap = key_cap - cyl

    if is_bump:
        # Create a small horizontal cylinder bump for home position indicator
        bump_radius = 0.4
        bump_length = 3.0
        bump = Cylinder(
            radius=bump_radius,
            height=bump_length,
            center=CenterType.CENTER,
            segments=segments)
        # Rotate to make it horizontal (along Y-axis)
        bump = bump.rotate_x(90)
        # Position at the center of the top surface
        bump = bump.translate((top_dx, top_dy, height))
        # Apply the same rotations as the top surface
        bump = bump.rotate_x(top_rx_deg)
        bump = bump.rotate_y(top_ry_deg)
        bump = bump.rotate_z(top_rz_deg)

        key_cap = key_cap + bump

    return key_cap


# %%
if __name__ == "__main__":
    # Example 1: Keycap with dimple
    key_cap = create_keycap_top(
        bottom_w=16.0,
        bottom_d=16.0,
        top_w=16.0,
        top_d=16.0,
        height=5.0,
        bottom_radius=3,
        top_radius=3,
        top_dx=0.0,
        top_dy=0.0,
        top_rx_deg=5.0,
        top_ry_deg=0.0,
        top_rz_deg=0.0,
        is_dimple=True,
        dimple_radius=40.0,
        dimple_size=3.0,
        dimple_segments=1000,
        is_sohw_dimple=False,
        segments=64,
        # is_bump=True,
    )
    key_cap.render()

    # Example 2: Keycap with bump for home position (F/J keys)
    # key_cap_bump = create_keycap_top(
    #     bottom_w=16.0,
    #     bottom_d=16.0,
    #     top_w=16.0,
    #     top_d=16.0,
    #     height=5.0,
    #     bottom_radius=3,
    #     top_radius=3,
    #     top_dx=0.0,
    #     top_dy=0.0,
    #     top_rx_deg=5.0,
    #     top_ry_deg=0.0,
    #     top_rz_deg=0.0,
    #     dimple=0.0,
    #     segments=64,
    #     is_bump=True,
    # )
    # key_cap_bump.render()
# %%
