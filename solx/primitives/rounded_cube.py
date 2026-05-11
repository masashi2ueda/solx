# %%
from __future__ import annotations

from solx.core import Vec3
from solx.primitives.cube import Cube
from solx.primitives.cylinder import Cylinder
from solx.primitives.types import CenterType, DefautltCenterType


class RoundedCube(Cube):
    def __init__(
        self,
        size: Vec3 = (5, 5, 5),
        radius: float = 1.0,
        segments: int = 32,
        center: CenterType = DefautltCenterType,
    ):
        r2 = radius * 2
        w, d, h = size
        base_cube1 = Cube(size=(w - r2, d, h), center=CenterType.BOTTOM_CENTER)
        base_cube2 = Cube(size=(w, d - r2, h), center=CenterType.BOTTOM_CENTER)
        base_cube = base_cube1 + base_cube2
        outer_cube = Cube(size=size, center=CenterType.BOTTOM_CENTER)

        corner_cylinder = Cylinder(radius=radius, segments=segments, height=h, center=CenterType.BOTTOM_CENTER)
        dw = w / 2 - radius
        dh = d / 2 - radius
        base_cube += corner_cylinder.translate((dw, dh, 0))
        base_cube += corner_cylinder.translate((-dw, dh, 0))
        base_cube += corner_cylinder.translate((-dw, -dh, 0))
        base_cube += corner_cylinder.translate((dw, -dh, 0))

        tranc_vec = (0, 0, 0)
        if center == CenterType.CENTER:
            tranc_vec = (0, 0, -size[2] / 2)
        elif center == CenterType.BOTTOM_LEFT:
            tranc_vec = (size[0] / 2, size[1] / 2, 0)
        base_cube = base_cube.translate(tranc_vec)
        outer_cube = outer_cube.translate(tranc_vec)

        super()._init(node=base_cube.node, pts=outer_cube.pts)
        self.radius = radius

    def param_apply(self, func_name: str, params: Vec3) -> RoundedCube:
        return self.cube_param_apply(func_name, params)


if __name__ == "__main__":
    taobj = RoundedCube(size=(30, 20, 10), radius=3, center=CenterType.BOTTOM_CENTER)
    taobj = taobj.translate((10, 20, 30))
    taobj = taobj.rotate((10, 0, 0))
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
