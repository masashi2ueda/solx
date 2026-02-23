# %%
"""Docstring for solx.components.keyboard.keycap_top."""
import solid

from solx import SolxObject
from solx.primitives import Cylinder, RoundedCube
from solx.primitives.types import CenterType

SMALL_VAL = 1e-5
EPS = 1e-3


def create_keycap_base(
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
    dimple,
    segments) -> SolxObject:
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

    top_cube = top_cube.translate((top_dx, top_dy, height))
    top_cube = top_cube.rotate_x(top_rx_deg)
    top_cube = top_cube.rotate_y(top_ry_deg)
    top_cube = top_cube.rotate_z(top_rz_deg)
    key_cap_node = solid.hull()(
        bottom_cube.node, top_cube.node
    )
    key_cap = SolxObject(key_cap_node)

    if dimple > 0:
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
    return key_cap


# %%
def create_keycap_top(
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
    offset_h_ratio = 0.5
) -> SolxObject:
    """Create a keycap top with hollow inside.

    Args:
        bottom_w (float): Width of the bottom face.
        bottom_d (float): Depth of the bottom face.
        top_w (float): Width of the top face.
        top_d (float): Depth of the top face.
        height (float): Height of the keycap.
        bottom_radius (float): Radius of the bottom face corners.
        top_radius (float): Radius of the top face corners.
        top_dx (float): X offset of the top face.
        top_dy (float): Y offset of the top face.
        top_rx_deg (float): Rotation around X axis of the top face in degrees.
        top_ry_deg (float): Rotation around Y axis of the top face in degrees.
        top_rz_deg (float): Rotation around Z axis of the top face in degrees.
        dimple (float): Depth of the dimple on the top face.
        home_bump (bool): If True, add a small bump for home position.
        home_bump_radius (float): Radius of the home position bump.
        home_bump_height (float): Height of the home position bump.
        home_bump_length (float): Length of the home position bump.
        home_bump_offset_x (float): X offset of the bump on the top face.
        home_bump_offset_y (float): Y offset of the bump on the top face.
        home_bump_offset_y_ratio (float|None): If set, overrides Y offset using a ratio
            of half the top depth (-1.0: front edge, 0: center, 1.0: back edge).
        segments (int): Number of segments for rounded corners.
        offset_wd (float): Wall thickness of the keycap.
        offset_h_ratio (float): Ratio of height to offset the inner hollow part.

    Returns:
        SolxObject: The hollow keycap top object.
    """
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

    keycap_innter = keycap_innter.translate((0.0, 0.0, -EPS))
    key_cap = keycap_outer - keycap_innter

    if home_bump:
        bump_offset_y = home_bump_offset_y
        if home_bump_offset_y_ratio is not None:
            bump_offset_y = (top_d / 2) * home_bump_offset_y_ratio
        bump = Cylinder(
            radius=home_bump_radius,
            height=home_bump_length,
            center=CenterType.CENTER,
            segments=segments
        )
        bump = bump.rotate_y(90)
        if home_bump_radius > 0:
            bump = bump.scale([1.0, 1.0, home_bump_height / (2 * home_bump_radius)])
        bump = bump.translate(
            (
                top_dx + home_bump_offset_x,
                top_dy + bump_offset_y,
                height + (home_bump_height / 2)
            )
        )
        bump = bump.rotate_x(top_rx_deg)
        bump = bump.rotate_y(top_ry_deg)
        bump = bump.rotate_z(top_rz_deg)
        key_cap = key_cap + bump
    return key_cap
# %%
