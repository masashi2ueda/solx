# %%
from solid import screw_thread

from solx.core import SolxObject
from solx.primitives import CenterType, Cube, Cylinder


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


class ScrewThread(SolxObject):
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


screw_height = 15
screw_radius = 2
tooth_height = 0.5
tooth_width = 0.2
rotation_cnt = 5
handle_height = 3
handle_width = 30
handle_depth = 3
thread = ScrewThread(
    tooth_height=tooth_height,
    tooth_width=tooth_width,
    screw_height=screw_height,
    screw_radius=screw_radius,
    rotation_cnt=rotation_cnt,
    handle_height=handle_height,
    handle_width=handle_width,
    handle_depth=handle_depth,
    flat_ratio=0.3,
)
thread.render()
# %%
nat_offset_xy = 0.1
nat_offset_z = 0
nat_width = (screw_radius + tooth_height) * 2 + nat_offset_xy
nat_depth = nat_width
nat_height = 10
nat_cube = Cube(size=(nat_width, nat_depth, nat_height), center=CenterType.BOTTOM_CENTER)
nat_cube -= thread.translate((0, 0, nat_offset_z))
nat_cube.render()
# %%
