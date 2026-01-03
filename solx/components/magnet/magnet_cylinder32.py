"""Magnet hole creation utilities for 3D printing.

This module provides functionality to create cylindrical magnet holes
that can be subtracted from other 3D objects for embedding magnets.
"""

# %%
from solx import Cube, Cylinder
from solx.primitives.types import CenterType

r = 1.6
h = 2.1


def create_magnet_hole()->Cylinder:
    """Create a cylindrical magnet hole.

    Returns:
        Cylinder: A cylinder representing the magnet hole.
    """
    mag_cyl = Cylinder(radius=r, height=h)
    return mag_cyl


if __name__ == "__main__":
    mgn_h = 0.5
    outer_cube = Cube(size=(4, 4, h + mgn_h), center=CenterType.BOTTOM_CENTER)
    mag_cyl = create_magnet_hole()
    mag_cyl = mag_cyl.translate((0, 0, mgn_h))

    dst = outer_cube - mag_cyl
    dst.render()
    dst_dir_path = "/home/uedam/dev/solx/examples/output_stl"
    dst.save_stl(f"{dst_dir_path}/mag.stl")
