# %%
# https://www.amazon.co.jp/dp/B0756QMKBH?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_2&th=1
# ラディウス radius HP-DME ディープマウントイヤーピース : 高いフィット感 重低音の迫力増強 高遮音性 イヤーピース イヤーチップ (ブラック/XS (SS) サイズ ・3セット) HP-DME04K

from __future__ import annotations

from typing import TypeVar

from solx.core import SolxObject
from solx.primitives import CenterType, Cube, Cylinder

T = TypeVar("T", bound=SolxObject)


class RubberFoot(SolxObject):
    def __init__(
        self,
        cube_size: tuple[float, float, float] = (10.0, 10.0, 40.0),
        cylinder_r1: float = 4.5,
        cylinder_r2: float = 3.5,
        cylinder_r3: float = 2.5,
        screw_r: float = 3.0,
        hole_z_frm_top: float = 7.0,
        center: CenterType = CenterType.BOTTOM_CENTER,
    ):
        cube_w, cube_d, cube_h = cube_size
        cube = Cube(size=cube_size, center=center)
        screw_cylinder = Cylinder(radius=screw_r, height=cube_d, center=CenterType.BOTTOM_CENTER)
        screw_cylinder = screw_cylinder.rotate((90, 0, 0))
        screw_cylinder = screw_cylinder.translate((0, cube_d/2, 0))
        screw_cylinder = screw_cylinder.translate((0, 0, cube_h - hole_z_frm_top))
        cube = cube - screw_cylinder
        cube = cube.translate((0, 0, cylinder_r1))

        cylinder1 = Cylinder(radius=cylinder_r1, height=cylinder_r1*2, center=CenterType.BOTTOM_CENTER)
        cylinder2 = Cylinder(radius=cylinder_r2, height=cylinder_r2*2, center=CenterType.BOTTOM_CENTER)
        cylinder3 = Cylinder(radius=cylinder_r3, height=cylinder_r3*2, center=CenterType.BOTTOM_CENTER)

        dst = cube + cylinder1 - cylinder2 + cylinder3

        super().__init__(openscad_node=dst.node)  # Dummy initialization

if __name__ == "__main__":
    rubber_foot = RubberFoot()
    rubber_foot.render()
# %%


