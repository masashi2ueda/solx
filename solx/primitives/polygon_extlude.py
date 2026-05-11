"""Polygon extrusion primitive for 3D modeling.

This module provides the PolygonExtrude class for creating 3D objects by extruding
2D polygon shapes along the Z-axis using the SolidPython library.
"""

# %%
from __future__ import annotations

import copy

import solid

from solx.core import Point3D, SolxObject, Vec3, param_apply


class PolygonExtrude(SolxObject):
    """A polygon extrude primitive for 3D modeling.

    This class creates a 3D object by extruding a 2D polygon shape along the Z-axis.
    The extrusion can be configured with height and positioning origin.

    Attributes:
        points (list[tuple[float, float]]): List of 2D points defining the polygon shape.
        height (float): Height of the extrusion along the Z-axis.
        center (bool): Whether to center the extrusion along the Z-axis.
    """

    def __init__(
        self,
        points: list[tuple[float, float]],
        height: float = 1.0,
    ):
        """Create a polygon extrude primitive.

        Args:
            points (list[tuple[float, float]]): List of 2D points defining the polygon shape.
            height (float, optional): Height of the extrusion along the Z-axis. Defaults to 1.0.

        Returns:
            SolxObject: A polygon extrude object positioned according to the specified parameters.
        """
        node_extrude = solid.linear_extrude(height=height)(solid.polygon(points=points))
        super().__init__(node_extrude)
        self.h = height
        self.top_pts = [Point3D(x, y, height) for x, y in points]
        self.bottom_pts = [Point3D(x, y, 0) for x, y in points]

    def param_apply(self, func_name: str, params: Vec3) -> PolygonExtrude:
        dst = copy.deepcopy(self)
        dst.node = param_apply(func_name, params, self.node)
        dst.top_pts = [param_apply(func_name, params, pt) for pt in self.top_pts]
        dst.bottom_pts = [param_apply(func_name, params, pt) for pt in self.bottom_pts]
        return dst


if __name__ == "__main__":
    from solx.primitives.cube import Cube
    from solx.primitives.types import CenterType

    taobj = PolygonExtrude(points=[(0, 0), (10, 0), (10, 20), (5, 20), (3, 8)], height=10)
    taobj = taobj.translate((10, 20, 30))
    taobj = taobj.rotate((10, 20, 30))
    taobj = taobj.scale((1.5, 2.0, 2.5))
    c = Cube(size=(2, 2, 2), center=CenterType.BOTTOM_CENTER)
    taobj += c
    c = Cube(size=(1, 1, 1), center=CenterType.BOTTOM_CENTER)
    taobj -= c
    dst = taobj.copy()
    pts = taobj.bottom_pts + taobj.top_pts
    for i, pt in enumerate(pts):
        pt_cube = Cube(size=(1, 1, 5), center=CenterType.CENTER).translate(pt.to_tuple())
        dst += pt_cube
    dst.render()
# %%
