"""Cube primitive for 3D modeling.

This module provides a cube primitive with configurable positioning origins.
"""

# %%
from __future__ import annotations

import copy
from typing import Self

import solid

from solx.core import Point3D, SolxObject, Vec3, param_apply
from solx.primitives.types import CenterType, DefautltCenterType


class Cube(SolxObject):
    def __init__(
        self,
        size: Vec3 = (1, 1, 1),
        center: CenterType = DefautltCenterType,
    ):
        """Create a cube primitive.
        Args:
            size (Vec3): Size of the cube along each axis.
            center (CenterType, optional): Center type for positioning the cube.
                Defaults to CenterType.BOTTOM_CENTER.
        Note:
            Cube vertex labeling:
             p7---p6
             /   /
            p4---p5

             p3---p2
             /   /
            p0---p1
        """
        w, d, h = size
        base_cube = SolxObject(openscad_node=solid.cube(size=size, center=True))
        pts = self.create_pts(size=size)
        if center == CenterType.BOTTOM_CENTER:
            center_translation = (0, 0, h / 2)
        elif center == CenterType.CENTER:
            center_translation = (0, 0, 0)
        elif center == CenterType.BOTTOM_LEFT:
            center_translation = (w / 2, d / 2, h / 2)
        base_cube = base_cube.translate(center_translation)
        pts = [pt.translate(center_translation) for pt in pts]

        super().__init__(openscad_node=base_cube.node)
        self.pts = pts

    @staticmethod
    def create_pts(size: Vec3) -> list[Point3D]:
        w, d, h = size
        pts = [
            Point3D(-w / 2, -d / 2, -h / 2),  # p0
            Point3D(w / 2, -d / 2, -h / 2),  # p1
            Point3D(w / 2, d / 2, -h / 2),  # p2
            Point3D(-w / 2, d / 2, -h / 2),  # p3
            Point3D(-w / 2, -d / 2, h / 2),  # p4
            Point3D(w / 2, -d / 2, h / 2),  # p5
            Point3D(w / 2, d / 2, h / 2),  # p6
            Point3D(-w / 2, d / 2, h / 2),  # p7
        ]
        return pts

    @property
    def w(self) -> float:
        return self.pts[1].distance_to(self.pts[0])

    @property
    def d(self) -> float:
        return self.pts[3].distance_to(self.pts[0])

    @property
    def h(self) -> float:
        return self.pts[4].distance_to(self.pts[0])

    @property
    def size(self) -> Vec3:
        return (self.w, self.d, self.h)

    @property
    def center(self) -> Point3D:
        cx = (self.pts[0].x + self.pts[1].x) / 2
        cy = (self.pts[0].y + self.pts[3].y) / 2
        cz = (self.pts[0].z + self.pts[4].z) / 2
        return Point3D(cx, cy, cz)

    def _init(self, node: solid.OpenSCADObject, pts: list[Point3D]) -> None:
        self.node = node
        self.pts = pts

    @classmethod
    def create(cls, node: solid.OpenSCADObject, pts: list[Point3D]) -> Cube:
        dst = Cube.__new__(Cube)
        dst._init(node=node, pts=pts)
        return dst

    def cube_param_apply(self, func_name: str, params: Vec3) -> Self:
        dst = copy.deepcopy(self)
        dst.node = param_apply(func_name, params, self.node)
        dst.pts = [param_apply(func_name, params, pt) for pt in self.pts]
        return dst

    def param_apply(self, func_name: str, params: Vec3) -> Cube:
        return self.cube_param_apply(func_name, params)


if __name__ == "__main__":
    taobj = Cube(size=(10, 20, 30), center=CenterType.BOTTOM_LEFT)
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
