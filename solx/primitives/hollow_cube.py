# %%
from __future__ import annotations

import copy

from solx.core import Vec3
from solx.primitives.cube import Cube
from solx.primitives.types import CenterType, DefautltCenterType


class HollowCube(Cube):
    def  __init__(
        self,
        size: Vec3 = (5, 5, 5),
        wall_thickness: float = 1.0,
        center: CenterType = DefautltCenterType,
        d_px: float| None = None,
        d_mx: float| None = None,
        d_py: float| None = None,
        d_my: float| None = None,
        d_pz: float| None = None,
        d_mz: float| None = None,
    ):
        cube = Cube(
            size=size,
            center=CenterType.BOTTOM_LEFT
        )

        def trans_d_func(d_val, wall_thickness):
            return d_val if d_val is not None else wall_thickness if wall_thickness is not None else 1.0

        d_px = trans_d_func(d_px, wall_thickness)
        d_mx = trans_d_func(d_mx, wall_thickness)
        d_py = trans_d_func(d_py, wall_thickness)
        d_my = trans_d_func(d_my, wall_thickness)
        d_pz = trans_d_func(d_pz, wall_thickness)
        d_mz = trans_d_func(d_mz, wall_thickness)
        subt_width = cube.w - d_px - d_mx
        subt_depth = cube.d - d_py - d_my
        subt_height = cube.h - d_pz - d_mz
        subt_cube = Cube(
            size=(subt_width, subt_depth, subt_height),
            center=CenterType.BOTTOM_LEFT
        ).translate((d_mx, d_my, d_mz))
        hollow_cube = cube - subt_cube

        trans_vec = (0, 0, 0)
        if center == CenterType.BOTTOM_CENTER:
            trans_vec = (-cube.w / 2, -cube.d / 2, 0)
        elif center == CenterType.CENTER:
            trans_vec = (-cube.w / 2, -cube.d / 2, -cube.h / 2)
        
        hollow_cube = hollow_cube.translate(trans_vec)
        subt_cube = subt_cube.translate(trans_vec)

        self.d_px = d_px
        self.d_mx = d_mx
        self.d_py = d_py
        self.d_my = d_my
        self.d_pz = d_pz
        self.d_mz = d_mz
        self.subt_cube = subt_cube
        super()._init(node=hollow_cube.node, pts=hollow_cube.pts)

    def param_apply(self, func_name: str, params: Vec3) -> HollowCube:
        dst = copy.deepcopy(self)
        dst = dst.cube_param_apply(func_name, params)
        dst.subt_cube = self.subt_cube.param_apply(func_name, params)
        return dst


if __name__ == "__main__":
    taobj = HollowCube(size=(30, 5, 30),wall_thickness=1,d_px=0, center=CenterType.BOTTOM_CENTER)
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
    subt_cube = taobj.subt_cube.translate((0,5,0))
    dst += subt_cube
    for i, pt in enumerate(subt_cube.pts):
        pt_cube = Cube(size=(1, 1, 5), center=CenterType.CENTER).translate(pt.to_tuple())
        dst += pt_cube

    dst.render()

# %%
