"""Cylinder primitive for 3D modeling.

This module provides a cylinder primitive with configurable positioning origins.
"""
# %%
from __future__ import annotations

import copy

import solid

from solx.core import Point3D, SolxObject, Vec3, param_apply
from solx.primitives.types import CenterType


class Cylinder(SolxObject):
    def __init__(
        self,
        radius: float = 1.0,
        height: float = 1.0,
        center: CenterType = CenterType.BOTTOM_CENTER,
        segments: int = 32,
    ):
        node_cylinder = solid.cylinder(
            r=radius,
            h=height,
            center=True,
            segments=segments)
        cyl = SolxObject(node_cylinder)
        pts = [
            Point3D(0, 0, -height / 2),  # Bottom center
            Point3D(0, 0, height / 2),   # Top center
        ]

        if center == CenterType.BOTTOM_CENTER:
            translation = (0, 0, height / 2)
        elif center == CenterType.CENTER:
            translation = (0, 0, 0)
        elif center == CenterType.BOTTOM_LEFT:
            translation = (radius, radius, height / 2)
        else:
            raise ValueError("Invalid CenterType")

        cyl = cyl.translate(translation)
        pts = [pt.translate(translation) for pt in pts]

        super().__init__(cyl.node)
        self.pts = pts
        self.r = radius
        self.h = height

    def _init(self, node: solid.OpenSCADObject, pts: list[Point3D]) -> None:
        self.node = node
        self.pts = pts

    @property
    def bottom_center(self) -> Point3D:
        return self.pts[0]
    @property
    def top_center(self) -> Point3D:
        return self.pts[1]
    
    def param_apply(self, func_name: str, params: Vec3) -> Cylinder:
        dst = copy.deepcopy(self)
        dst.node = param_apply(func_name, params, self.node)
        dst.pts = [param_apply(func_name, params, pt) for pt in self.pts]
        return dst


if __name__ == "__main__":
    from solx.primitives.cube import Cube
    taobj = Cylinder(radius=10, height=20, center=CenterType.BOTTOM_LEFT)
    taobj = taobj.translate((10, 20, 30))
    taobj = taobj.rotate((10, 20, 30))
    taobj = taobj.scale((1.5, 2.0, 2.5))

    dst = taobj.copy()
    for i, pt in enumerate(taobj.pts):
        pt_cube = Cube(size=(1, 1, 5), center=CenterType.CENTER).translate(pt.to_tuple())
        dst += pt_cube
    dst.render()
# %%
