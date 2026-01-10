"""Cube primitive for 3D modeling.

This module provides a cube primitive with configurable positioning origins.
"""
# %%
from __future__ import annotations

import solid
from solid.objects import OpenSCADObject

from solx.core import Point3D, SolxObject, Vec3
from solx.primitives.types import CenterType


class Cube(SolxObject):
    def __init__(
        self,
        size: Vec3 = (1, 1, 1),
        center: CenterType = CenterType.BOTTOM_CENTER,
    ):
        """Create a cube primitive.
        Args:
            size (Vec3): Size of the cube along each axis.
            center (CenterType, optional): Center type for positioning the cube.
                Defaults to CenterType.BOTTOM_CENTER.
        Note:
            Cube vertex labeling:
             p4---p5
             /   /
            p7---p6

             p0---p1
             /   /
            p3---p2
        """
        w, d, h = size
        base_cube = SolxObject(openscad_node=solid.cube(size=size, center=True))
        pts = [
            Point3D(-w / 2, -d / 2, -h / 2),  # p0
            Point3D( w / 2, -d / 2, -h / 2),  # p1
            Point3D( w / 2,  d / 2, -h / 2),  # p2
            Point3D(-w / 2,  d / 2, -h / 2),  # p3
            Point3D(-w / 2, -d / 2,  h / 2),  # p4
            Point3D( w / 2, -d / 2,  h / 2),  # p5
            Point3D( w / 2,  d / 2,  h / 2),  # p6
            Point3D(-w / 2,  d / 2,  h / 2),  # p7
        ]
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

    @classmethod
    def _from_params(cls, openscad_node: OpenSCADObject, pts: list[Point3D]) -> Cube:
        cube = cls.__new__(cls)
        super(Cube, cube).__init__(openscad_node=openscad_node)
        cube.pts = pts
        return cube
    
    def _param_apply(self, func_name, params) -> Cube:
        pts = [pt._param_apply(func_name, params) for pt in self.pts]
        cube = super()._param_apply(func_name, params)
        dst_cube = Cube._from_params(openscad_node=cube.node, pts=pts)
        return dst_cube

    def translate(self, translation_vector: Vec3) -> Cube:
        return self._param_apply('translate', translation_vector)
    def rotate(self, rotation_angles: Vec3) -> Cube:
        return self._param_apply('rotate', rotation_angles)
    def scale(self, scale_factors: Vec3) -> Cube:
        return self._param_apply('scale', scale_factors)


if __name__ == "__main__":
    cube = Cube(size=(10, 20, 30), center=CenterType.BOTTOM_LEFT)
    cube = cube.translate((5, 5, 0))

    cube.render()

    pts = None
    for i, pt in enumerate(cube.pts):
        pt_cube = Cube(size=(1, 1, 1+i*0.1), center=CenterType.CENTER)
        pt_cube = pt_cube.translate(pt.to_tuple())
        pts = pt_cube if pts is None else pts + pt_cube
    pts.render()

# %%
