"""Magnet hole creation utilities for 3D printing.

This module provides functionality to create cylindrical magnet holes
that can be subtracted from other 3D objects for embedding magnets.
"""

# %%
from __future__ import annotations

import copy

from solx.core import Point3D, SolxObject, Vec3, param_apply
from solx.primitives import CenterType, Cube, Cylinder, DefautltCenterType


class MagnetCylinder32(Cylinder):
    def __init__(
        self,
        radius: float = 1.6,
        height: float = 2.1,
        center: CenterType = DefautltCenterType,
        segments: int = 32,
    ):
        super().__init__(radius=radius, height=height, center=center, segments=segments)
    


class MagnetCube32(Cube):
    def __init__(
        self,
        mgn_wd: float = 2,
        mgn_h: float = 2,
        center: CenterType = DefautltCenterType,
    ):
        mag_cyl = MagnetCylinder32(center=center)
        mag_cyl = mag_cyl.translate((0, 0, mgn_h))
        cube_wd = mag_cyl.r * 2 + mgn_wd
        cube_h = mag_cyl.h + mgn_h
        cube = Cube(size=(cube_wd, cube_wd, cube_h), center=center)
        hole_cube = cube - mag_cyl

        super()._init(node=hole_cube.node, pts=hole_cube.pts)
        self.mag_cyl_r = mag_cyl.r
        self.mag_cyl_h = mag_cyl.h
        self.mag_cyl_pts = mag_cyl.pts
        self.cube = cube
        self.cylinder = mag_cyl
    
    @property
    def mag_bottom_center(self) -> Point3D:
        return self.mag_cyl_pts[0]
    @property
    def mag_top_center(self) -> Point3D:
        return self.mag_cyl_pts[1]

    def param_apply(self, func_name: str, params: Vec3) -> MagnetCube32:
        dst = copy.deepcopy(self)
        # base_cube
        dst.node = param_apply(func_name, params, self.node)
        dst.pts = [param_apply(func_name, params, pt) for pt in self.pts]
        
        dst.mag_cyl_pts = [param_apply(func_name, params, pt) for pt in self.mag_cyl_pts]
        dst.cube = self.cube.param_apply(func_name, params)
        dst.cylinder = self.cylinder.param_apply(func_name, params)
        return dst

    def add_with_subt(self, other: SolxObject) -> MagnetCube32:
        dst = copy.deepcopy(self)
        dst += other
        dst -= self.cylinder
        return dst


if __name__ == "__main__":
    taobj = MagnetCube32(center=CenterType.BOTTOM_CENTER)
    base_cube = Cube(size=(2, 2, 10), center=CenterType.CENTER).translate((2, 0, 0))
    taobj = taobj.add_with_subt(base_cube)
    taobj = taobj.translate((10, 20, 30))
    taobj = taobj.rotate((10, 20, 30))
    taobj = taobj.scale((1.5, 2.0, 2.5))

    dst = taobj.copy()
    for i, pt in enumerate(taobj.pts):
        pt_cube = Cube(size=(0.3, 0.3, 2), center=CenterType.CENTER).translate(pt.to_tuple())
        dst += pt_cube
    for i, pt in enumerate(taobj.mag_cyl_pts):
        pt_cube = Cube(size=(0.3, 0.3, 2), center=CenterType.CENTER).translate(pt.to_tuple())
        dst += pt_cube

    dst.render()

