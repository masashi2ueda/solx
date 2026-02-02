# %%
from __future__ import annotations

import copy
from typing import TypeVar

from solx.core import SolxObject, Vec3, param_apply
from solx.primitives import Cube, Cylinder, PolygonExtrude

T = TypeVar("T", bound=SolxObject)

# %%
class SlottedBearing(SolxObject):
    """Cylindrical bearing with slot cutouts"""
    def __init__(
        self,
        outer_radius: float = 7.0,
        inner_radius: float = 3.0,
        height: float = 10.0,
        slot_width_narrow: float = 3.0,
        slot_width_wide: float = 5.0,
        slot_depth_wide: float = 2.0,
        clearance_margin: float = 0.3,
        wide_ty_rate: float = 1/3,
    ):
        """
        Args:
            outer_radius: Radius of outer cylinder
            inner_radius: Radius of inner hole
            height: Total height
            slot_width_narrow: Width of narrow slot (outer)
            slot_width_wide: Width of wide slot (inner)
            slot_depth_wide: Depth of wide slot
            clearance_margin: Clearance margin for inset
        """
        # Outer and inner cylinders
        cyl1 = Cylinder(radius=outer_radius, height=height, segments=64)
        cyl2 = Cylinder(radius=inner_radius, height=height, segments=64)
        cyl = cyl1 - cyl2

        # Narrow outer slot
        narrow_slot = Cube(size=(slot_width_narrow, outer_radius, height))
        narrow_slot_ty = -outer_radius / 2
        narrow_slot = narrow_slot.translate((0, narrow_slot_ty, 0))
        cyl -= narrow_slot

        # Wide inner slot
        wide_slot = Cube(size=(slot_width_wide, slot_depth_wide, height))
        wide_slot_ty = -inner_radius - (outer_radius - inner_radius) * wide_ty_rate
        wide_slot = wide_slot.translate((0, wide_slot_ty, 0))
        cyl -= wide_slot

        # Inset parts (with clearance)
        inset_narrow = Cube(size=(slot_width_narrow - clearance_margin, outer_radius - clearance_margin, height))
        inset_narrow = inset_narrow.translate((0, narrow_slot_ty, 0))
        inset_wide = Cube(size=(slot_width_wide - clearance_margin, slot_depth_wide - clearance_margin, height))
        inset_wide = inset_wide.translate((0, wide_slot_ty, 0))
        inset = inset_narrow + inset_wide - cyl2
    
        super().__init__(openscad_node=cyl.node)
        self.inset = inset

    def param_apply(self, func_name: str, params: Vec3) -> SlottedBearing:
        dst = copy.deepcopy(self)
        dst.node = param_apply(func_name, params, self.node)
        dst.inset = self.inset.param_apply(func_name, params)
        return dst

class ArmRestPlate(SolxObject):
    def __init__(
        self,
        plate_w = 110.0,
        plate_d = 130.0,
        plate_h = 2.0,
        plate_w2_ratio = 0.9,
    ):
        plate_w2 = plate_w * plate_w2_ratio
        plate_d_m = plate_d - plate_w2 / 2

        plate = PolygonExtrude(
            points=[
                (plate_w / 2, 0),
                (plate_w2 / 2, plate_d_m),
                (0, plate_d),
                (-plate_w2 / 2, plate_d_m),
                (-plate_w / 2, 0),
            ],
            height=plate_h,
        )
        cyl = Cylinder(radius=plate_w2 / 2, height=plate_h, segments=64)
        cyl = cyl.translate((0, plate_d_m, 0))
        dst = plate + cyl
        super().__init__(openscad_node=dst.node)

class ArmRest(SolxObject):
    def __init__(
        self,
        # plate
        plate_w = 110.0,
        plate_d = 130.0,
        plate_h = 2.0,
        plate_w2_ratio = 0.9,
        # slot cube
        cube_w = 10.0,
        cube_d = 5.0,
        cube_h = 5.0,
        cube_dx = 5.0,

        # slot ling
        bearing_outer_radius=7.0,
        bearing_inner_radius=3.0,
        bearing_height=10.0,
        bearing_slot_width_narrow=3.0,
        bearing_slot_width_wide=5.0,
        bearing_slot_depth_wide=2.0,
        bearing_clearance_margin=0.3,
        bearing_wide_ty_rate: float = 1/3,
    ):
        # plate
        arm_rest_plate = ArmRestPlate(
            plate_w=plate_w,
            plate_d=plate_d,
            plate_h=plate_h,
            plate_w2_ratio=plate_w2_ratio,
        )
        dst = arm_rest_plate

        c_cube = Cube(size=(cube_w, cube_d, cube_h))
        cube_dy = cube_d / 2
        cube_dz = plate_h
        c_cube = c_cube.translate((0, cube_dy, cube_dz))
        c_cube_tx_r = -cube_w / 2 + plate_w / 2 - cube_dx
        c_cube_tx_l = -1 * c_cube_tx_r
        dst += c_cube.translate((c_cube_tx_r, 0, 0))
        dst += c_cube.translate((c_cube_tx_l, 0, 0))

        slotted_bearing = SlottedBearing(
            outer_radius=bearing_outer_radius,
            inner_radius=bearing_inner_radius,
            height=bearing_height,
            slot_width_narrow=bearing_slot_width_narrow,
            slot_width_wide=bearing_slot_width_wide,
            slot_depth_wide=bearing_slot_depth_wide,
            clearance_margin=bearing_clearance_margin,
            wide_ty_rate=bearing_wide_ty_rate,
        )
        slotted_bearing = slotted_bearing.rotate((90, 0, 0))
        slotted_bearing = slotted_bearing.rotate((0, 0, 90))
        slotted_bearing = slotted_bearing.rotate((180, 0, 0))
        slot_dz = cube_h + cube_dz + bearing_outer_radius - 1
        slotted_bearing = slotted_bearing.translate((-bearing_height/2, cube_dy, slot_dz))
        dst += slotted_bearing.translate((c_cube_tx_r, 0, 0))
        dst += slotted_bearing.translate((c_cube_tx_l, 0, 0))
        super().__init__(openscad_node=dst.node)

        self.slotted_bearing = slotted_bearing
# %%
if __name__ == "__main__":
    # plate
    plate_w = 110.0
    plate_d = 130.0
    plate_h = 2.0
    plate_w2_ratio = 0.9

    # slot cube
    cube_w = 10.0
    cube_d = 5.0
    cube_h = 5.0
    cube_dx = 5.0

    # slot ling
    bearing_outer_radius=7.0
    bearing_inner_radius=3.0
    bearing_height=10.0
    bearing_slot_width_narrow=3.0
    bearing_slot_width_wide=5.0
    bearing_slot_depth_wide=2.0
    bearing_clearance_margin=0.3

    arm_rest = ArmRest(
        plate_w=plate_w,
        plate_d=plate_d,
        plate_h=plate_h,
        plate_w2_ratio=plate_w2_ratio,
        cube_w=cube_w,
        cube_d=cube_d,
        cube_h=cube_h,
        cube_dx=cube_dx,
        bearing_outer_radius=bearing_outer_radius,
        bearing_inner_radius=bearing_inner_radius,
        bearing_height=bearing_height,
        bearing_slot_width_narrow=bearing_slot_width_narrow,
        bearing_slot_width_wide=bearing_slot_width_wide,
        bearing_slot_depth_wide=bearing_slot_depth_wide,
        bearing_clearance_margin=bearing_clearance_margin
    )
    arm_rest.render()
# %%
