# %%
from solx import config
from solx.primitives import CenterType, Cube, Cylinder

nut_cube_h = 11.0
nut_cube_wd = 8.125

nut_r = 3.0
nut_r_clr = 0.2
nut_h = 3.0

cube = Cube((nut_cube_wd, nut_cube_wd, nut_cube_h), center=CenterType.BOTTOM_CENTER)
cube.render()

r = nut_r + nut_r_clr
cylinder = Cylinder(radius=r, height=nut_h, segments=6,center=CenterType.BOTTOM_CENTER)
cylinder.render()

tz = nut_cube_h - nut_h
cylinder = cylinder.translate((0, 0, tz))

cube -= cylinder
cube.render()

dst_path = config.EnvConfig.OUTPUT_STL_DIR_PATH + "/mat_nut_cube.stl"
cube.save_stl(dst_path)

# %%
from __future__ import annotations

import copy
from typing import TypeVar

from solid import screw_thread

from solx.core import SolxObject, Vec3, param_apply
from solx.primitives import CenterType, Cube, Cylinder

T = TypeVar("T", bound=SolxObject)

# %%
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
        inverse_thread_dicrection: bool = False,
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
            length=screw_height + handle_height,
            segments_per_rot=31,
            neck_in_degrees=30,
            neck_out_degrees=30,
        )
        thread = SolxObject(thread)
        if inverse_thread_dicrection:
            thread = thread.mirror((0, 0, 1))
            thread = thread.translate((0, 0, screw_height))
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
        inverse_thread_dicrection: bool = False,
        nat_hole_d: float = 0.1
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
            inverse_thread_dicrection=inverse_thread_dicrection,
        )
        nat_width = (screw_radius + tooth_height) * 2 + nat_offset_xy
        nat_depth = nat_width
        nat_cube = Cube(size=(nat_width, nat_depth, nat_h), center=CenterType.BOTTOM_CENTER)
        nat_hole_cube = Cube(size=(nat_width+nat_hole_d, nat_depth + nat_hole_d, nat_h), center=CenterType.BOTTOM_CENTER)
        thread_for_nat = thread_for_nat.translate((0, 0, z_mgn))
        nat_cube -= thread_for_nat
        super().__init__(openscad_node=nat_cube.node)
        self.thread = copy.deepcopy(thread_for_nat)
        self.w = nat_width
        self.d = nat_depth
        self.h = nat_h
        self.nat_hole_cube = nat_hole_cube


    def param_apply(self, func_name: str, params: Vec3) -> Nut:
        dst = copy.deepcopy(self)
        dst.node = param_apply(func_name, params, dst.node)
        dst.thread = self.thread.param_apply(func_name, params)
        dst.nat_hole_cube = self.nat_hole_cube.param_apply(func_name, params)
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
    nut = Nut(
        tooth_height=tooth_height,
        tooth_width=tooth_width,
        screw_height=screw_height,
        screw_radius=screw_radius,
        rotation_cnt=rotation_cnt,
        nat_h=nat_h,)
    (thread+ nut).render()
    nut = nut.translate((0, 0, screw_height + 5))
    nut = nut.rotate((0, 0, 15))
# %%
from solx import config

# %%
# rubber_foot
rubeer_foot_cube_h = 40.0
rubeer_foot_cube_d = 8.0
rubeer_foot_cylinder_h = 10.0
rubeer_foot_screw_r_c = 0.25
rubeer_foot_screw_wd_mgn = 2.0

# screw
is_inverse = False
tooth_height = 0.7
tooth_width = 1.0
rotation_cnt = 7.5
screw_handle_height = 4.0
screw_handle_width = 30.0
flat_ratio = 0.3
rubeer_foot_cube_w_mgn = 3.0
screw_height_minus_mgn = 3.0

# nut cube
nut_h = 11.0
nut_h_mgn = 1.0
nut_wd = 8.125
nut_wd_mgn = 0.8
screw_r_c = 0.35
screw_tooth_height_c = 0.35
screw_tooth_width_c = 0.35

screw_height = nut_h + rubeer_foot_cube_d - nut_h_mgn - screw_height_minus_mgn

# nut calc
nut_out_r = nut_wd / 2
nut_in_r = nut_out_r - nut_wd_mgn
nut_screw_r = nut_in_r - tooth_height
nut_screw_tooth_height = tooth_height + screw_tooth_height_c
nut_screw_tooth_width = tooth_width + screw_tooth_width_c

# screw calc
screw_r = nut_screw_r - screw_r_c
screw_handle_depth = (screw_r + tooth_height) * 2

# foot calc
rubeer_foot_screw_r = screw_r + tooth_height + rubeer_foot_screw_r_c
rubeer_foot_cube_w = rubeer_foot_screw_r * 2 + rubeer_foot_cube_w_mgn

inverse_thread_dicrection = False
screw = Screw(
    tooth_height=tooth_height,
    tooth_width=tooth_width,
    screw_height=screw_height,
    screw_radius=screw_r,
    rotation_cnt=rotation_cnt,
    handle_height=screw_handle_height,
    handle_width=screw_handle_width,
    handle_depth=screw_handle_depth,
    flat_ratio=flat_ratio,
    inverse_thread_dicrection=is_inverse,
)
# screw.render()
dst_path = f"{config.EnvConfig.OUTPUT_STL_DIR_PATH}/screw.stl"
if is_inverse:
    dst_path = dst_path.replace("screw.stl", "screw_inverse.stl")
screw.save_stl(dst_path)
# %%
thread_for_nut = Screw(
    tooth_height=nut_screw_tooth_height,
    tooth_width=nut_screw_tooth_width,
    screw_height=screw_height,
    screw_radius=nut_screw_r,
    rotation_cnt=rotation_cnt,
    handle_height=1,
    handle_width=1,
    handle_depth=1,
    flat_ratio=flat_ratio,
    inverse_thread_dicrection=is_inverse,
)
nut_cube = Cube(size=(nut_wd, nut_wd, nut_h), center=CenterType.BOTTOM_CENTER)
thread_for_nut = thread_for_nut.translate((0, 0, nut_h_mgn))
nut_cube -= thread_for_nut
# nut_cube.render()
dst_path = f"{config.EnvConfig.OUTPUT_STL_DIR_PATH}/nut_cube.stl"
if is_inverse:
    dst_path = dst_path.replace("nut_cube.stl", "nut_cube_inverse.stl")
nut_cube.save_stl(dst_path)
# thread_for_nut.render()
# %%
nut_screw_tooth_height
# %%
print("screw_height:", screw_height)
print("screw_r:", screw_r)
print("nut_screw_r:", nut_screw_r)
print("tooth_height:", tooth_height)
print("tooth_width:", tooth_width)
print("nut_screw_tooth_height:", nut_screw_tooth_height)
print("nut_screw_tooth_width:", nut_screw_tooth_width)

# %%
# # %%
from solx.components.keyboard.rubber_foot import RubberFoot

rf = RubberFoot(
    cube_size=(
        rubeer_foot_cube_w,
        rubeer_foot_cube_d,
        rubeer_foot_cube_h
    ),
    screw_r=rubeer_foot_screw_r,
    cylinder_h=rubeer_foot_cylinder_h
)
rf = RubberFoot(
    cube_size=(
        rubeer_foot_cube_w,
        rubeer_foot_cube_d,
        rubeer_foot_cube_h
    ),
    screw_r=rubeer_foot_screw_r,
    cylinder_h=rubeer_foot_cylinder_h
)
# c = Cube((20,20,35))
# rf -= c
# rf.render()
rf.save_stl(f"{config.EnvConfig.OUTPUT_STL_DIR_PATH}/rubber_foot.stl")

# %%
