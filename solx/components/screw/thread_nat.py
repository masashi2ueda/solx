# %%
from __future__ import annotations

import copy
from typing import TypeVar

from solid import screw_thread

from solx.core import SolxObject, Vec3
from solx.primitives import CenterType, Cube, Cylinder

T = TypeVar("T", bound=SolxObject)


def create_trapezoid_thread(
    tooth_height: float,
    tooth_width: float,
    flat_ratio: float = 0.3):
    """
    台形のネジ山（ISO規格に近い形状）
    
    :param tooth_width: 歯の幅
    :param tooth_height: 歯の高さ
    :param flat_ratio: 上下の平坦部の割合（0.0-1.0）
    """
    flat_h = tooth_width * flat_ratio
    pts = [
        (0, -tooth_width / 2, 0),           # 底辺下
        (tooth_height, -flat_h / 2, 0),       # 外側下
        (tooth_height, flat_h / 2, 0),        # 外側上
        (0, tooth_width / 2, 0),            # 底辺上
    ]
    return pts


class Screw(SolxObject):
    def __init__(
        self,
        tooth_height: float,
        tooth_width: float,
        screw_height: float,
        screw_radius: float,
        rotation_cnt: int,
        handle_height: float,
        handle_width: float,
        handle_depth: float,
        flat_ratio: float = 0.3,
    ):
        pts = create_trapezoid_thread(
            tooth_height=tooth_height,
            tooth_width=tooth_width,
            flat_ratio=flat_ratio
        )

        pitch = screw_height / rotation_cnt


        thread = screw_thread.thread(
            pts,
            inner_rad=screw_radius,
            pitch=pitch,
            length=screw_height,
            segments_per_rot=31,
            neck_in_degrees=30,
            neck_out_degrees=30,
        )
        thread = SolxObject(thread)
        cylinder = Cylinder(
            radius=screw_radius + 0.01,
            height=screw_height + handle_height,
            center=CenterType.BOTTOM_CENTER
        )
        handle = Cube(
            size=(handle_width, handle_depth, handle_height),
            center=CenterType.BOTTOM_CENTER)
        handle = handle.translate((0, 0, screw_height))
        dst = thread + cylinder + handle

        
        super().__init__(dst.node)


class Nut(SolxObject):
    def __init__(
        self,
        tooth_height: float,
        tooth_width: float,
        screw_height: float,
        screw_radius: float,
        rotation_cnt: int,
        nat_h: float,
        th_mgn = 0.1,
        tw_mgn = 0.1,
        tr_mgn = 0.1,
        z_mgn = 2,
        nat_offset_xy = 2,
        flat_ratio: float = 0.3,
    ):
        thread_for_nat = Screw(
            tooth_height=tooth_height + th_mgn,
            tooth_width=tooth_width + tw_mgn,
            screw_height=screw_height,
            screw_radius=screw_radius + tr_mgn,
            rotation_cnt=rotation_cnt,
            handle_height=0,
            handle_width=0,
            handle_depth=0,
            flat_ratio=flat_ratio,
        )
        nat_width = (screw_radius + tooth_height) * 2 + nat_offset_xy
        nat_depth = nat_width
        nat_cube = Cube(size=(nat_width, nat_depth, nat_h), center=CenterType.BOTTOM_CENTER)
        nat_cube -= thread_for_nat.translate((0, 0, z_mgn))
        super().__init__(nat_cube.node)
        self.thread = thread_for_nat


    def param_apply(self, func_name: str, params: Vec3) -> Nut:
        dst = copy.deepcopy(self)
        dst = dst.param_apply(func_name, params)
        dst.thread = self.thread.param_apply(func_name, params)
        return dst
    
    def add_to(self, base: T) -> T:
        base += self
        base -= self.thread
        return base


if __name__ == "__main__":
    screw_height = 15
    screw_radius = 2
    tooth_height = 0.5
    tooth_width = 0.2
    rotation_cnt = 5
    handle_height = 3
    handle_width = 30
    handle_depth = 3
    flat_ratio = 0.3
    nat_h = 10
    thread = Screw(
        tooth_height=tooth_height,
        tooth_width=tooth_width,
        screw_height=screw_height,
        screw_radius=screw_radius,
        rotation_cnt=rotation_cnt,
        handle_height=handle_height,
        handle_width=handle_width,
        handle_depth=handle_depth,
        flat_ratio=flat_ratio,
    )
    nat = Nut(
        tooth_height=tooth_height,
        tooth_width=tooth_width,
        screw_height=screw_height,
        screw_radius=screw_radius,
        rotation_cnt=rotation_cnt,
        nat_h=nat_h,)
    (thread+ nat).render()
