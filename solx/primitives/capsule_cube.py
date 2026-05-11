"""Capsule cube primitive for 3D modeling.

This module provides the CapsuleCube class, which creates a cube with rounded edges
by combining a central rectangular cube with cylindrical caps on opposite sides.
The capsule cube can be configured with different sizes, positioning origins,
and segment counts for smooth edge approximation.
"""

# %%
from __future__ import annotations

import copy

from solid.objects import OpenSCADObject

from solx.core import Point3D, Vec3
from solx.primitives.cube import Cube
from solx.primitives.cylinder import Cylinder
from solx.primitives.types import CenterType, DefautltCenterType


class CapsuleCube(Cube):
    pts: list[Point3D]
    node: OpenSCADObject
    r: float

    def __init__(
        self,
        size: Vec3 = (1, 1, 1),
        center: CenterType = DefautltCenterType,
        segments: int = 32,
    ):
        # create cube
        w = size[0]
        d = size[1]
        h = size[2]

        # create cube
        cube = Cube(size=(w - d, d, h), center=CenterType.BOTTOM_CENTER)

        r = d / 2
        cyl = Cylinder(radius=r, height=h, center=CenterType.BOTTOM_CENTER, segments=segments)
        dx = w / 2 - r
        cube += cyl.translate((-dx, 0, 0))
        cube += cyl.translate((dx, 0, 0))

        pts = Cube.create_pts(size=size)
        pts = [pt.translate((0, 0, h / 2)) for pt in pts]

        trans_vec = (0, 0, 0)
        if center == CenterType.BOTTOM_CENTER:
            pass
        if center == CenterType.CENTER:
            trans_vec = (0, 0, -h / 2)
        if center == CenterType.BOTTOM_LEFT:
            trans_vec = (w / 2, d / 2, 0)
        cube = cube.translate(trans_vec)
        pts = [pt.translate(trans_vec) for pt in pts]

        super()._init(node=cube.node, pts=pts)
        self.r = r

    def param_apply(self, func_name: str, params: Vec3) -> CapsuleCube:
        dst = copy.deepcopy(self)
        dst = dst.cube_param_apply(func_name, params)
        return dst


if __name__ == "__main__":
    taobj = CapsuleCube(size=(30, 5, 30), center=CenterType.BOTTOM_LEFT)
    taobj = taobj.translate((10, 20, 30))
    taobj = taobj.rotate((10, 20, 30))
    taobj = taobj.scale((1.5, 2.0, 2.5))
    c = Cube(size=(2, 2, 2), center=CenterType.BOTTOM_CENTER)
    taobj += c
    c = Cube(size=(1, 1, 1), center=CenterType.BOTTOM_CENTER)
    taobj -= c
    dst = taobj.copy()
    for i, pt in enumerate(taobj.pts):
        pt_cube = Cube(size=(1, 1, 5), center=CenterType.CENTER).translate(pt.to_tuple())
        dst += pt_cube
    dst.render()

# %%
