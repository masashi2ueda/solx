# %%
from solx.core import SolxObject, Vector3D
from solx.primitives.cube import Cube
from solx.primitives.types import CenterType


class HollowCube(SolxObject):

    def  __init__(
        self,
        size: Vector3D | None = None,
        wall_thickness: float | None = None,
        *,
        width: float | None = None,
        depth: float | None = None,
        height: float | None = None,
        center: CenterType = CenterType.BOTTOM_CENTER,
        d_px: float| None = None,
        d_mx: float| None = None,
        d_py: float| None = None,
        d_my: float| None = None,
        d_pz: float| None = None,
        d_mz: float| None = None,
    ):
        cube = Cube(
            size=size,
            width=width,
            depth=depth,
            height=height,
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
        subt_width = cube.width - d_px - d_mx
        subt_depth = cube.depth - d_py - d_my
        subt_height = cube.height - d_pz - d_mz
        subt_cube = Cube(
            size=(subt_width, subt_depth, subt_height),
            center=CenterType.BOTTOM_LEFT
        ).translate((d_mx, d_my, d_mz))
        hollow_cube = cube - subt_cube

        if center == CenterType.BOTTOM_CENTER:
            hollow_cube = hollow_cube.translate(
                (-cube.width / 2, -cube.depth / 2, 0))
        elif center == CenterType.CENTER:
            hollow_cube = hollow_cube.translate(
                (-cube.width / 2, -cube.depth / 2, -cube.height / 2)
            )
        
        self.width = cube.width
        self.depth = cube.depth
        self.height = cube.height
        self.d_px = d_px
        self.d_mx = d_mx
        self.d_py = d_py
        self.d_my = d_my
        self.d_pz = d_pz
        self.d_mz = d_mz
        super().__init__(hollow_cube.node)


if __name__ == "__main__":
    hc = HollowCube(
        size=(10, 15, 20),
        wall_thickness=1.0,
        d_px=0
    )
    hc.render()
# %%
