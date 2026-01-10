"""Magnet hole creation utilities for 3D printing.

This module provides functionality to create cylindrical magnet holes
that can be subtracted from other 3D objects for embedding magnets.
"""

# %%
from solx import Cube, Cylinder
from solx.core.base import SolxObject
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

class MagnetHoleCube(SolxObject):
    def __init__(self, mgn: float = 2):
        mag_cyl = create_magnet_hole()
        mag_cyl = mag_cyl.translate((0, 0, mgn))
        cube_wd = r * 2 + mgn
        cube_h = h + mgn
        cube = Cube(size=(cube_wd, cube_wd, cube_h), center=CenterType.BOTTOM_CENTER)
        hole_cube = cube - mag_cyl

        self.cube = cube
        self.mag_cyl = mag_cyl
        self.hole_cube = hole_cube
        self.cube_wd = cube_wd
        self.cube_h = cube_h
    
        super().__init__(
            openscad_node=hole_cube.node,
            sub_nodes=[cube.node, mag_cyl.node])


if __name__ == "__main__":
    mhc = MagnetHoleCube()

    outer_cube = Cube(size=(10, 10, 3), center=CenterType.BOTTOM_CENTER)
    outer_cube -= mhc.cube
    outer_cube += mhc

    outer_cube.render()
    dst_dir_path = "/home/uedam/dev/solx/examples/output_stl"
    outer_cube.save_stl(f"{dst_dir_path}/mag.stl")

# %%
mhc = MagnetHoleCube()
mhc = mhc.translate((10, 0, 0))
(mhc + mhc.cube).render()

# %%
class A:
    def __init__(self, val: float, sub_vals: list[float]|None = None):
        self.val = val
        self.sub_vals = sub_vals

    def add(self, add_val: float):
        return self.__class__.from_val(self.val + add_val, self.sub_vals)

    @classmethod
    def from_val(cls, val: float, sub_vals: list[float]|None = None):
        return cls(val, sub_vals)

class B(A):
    def __init__(self,val1: float,val2: float,
        val=None, sub_vals=None):
        if val is not None:
            super().__init__(val, sub_vals)
            self.val1 = sub_vals[0]
            self.val2 = sub_vals[1]
            self.val3 = val
            return
        self.val1 = val1
        self.val2 = val2
        self.val3 = val1 + val2
        sub_vals = [val1, val2]
        super().__init__(self.val3, sub_vals=[val1, val2])
    
    @classmethod
    def from_val(cls, val: float, sub_vals: list[float]|None = None):
        # どう分解するかは設計次第
        return cls(None, None, val, sub_vals)
    def __repr__(self):
        return f"B(val1={self.val1}, val2={self.val2}, val3={self.val3})"

b = B(2, 3)
c = b.add(5)
c

# %%
