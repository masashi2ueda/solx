# %%
from __future__ import annotations

import copy
from typing import TypeVar

from solx.core import SolxObject, Vec3
from solx.primitives import Cube, Cylinder, PolygonExtrude

T = TypeVar("T", bound=SolxObject)


# %%

c_w = 10.0
c_d = 5.0
c_h = 5.0
c_dx = 5.0

plate_w = 110.0
plate_d = 130.0

plat_radius = 50.0
plate_h = 2.0

# plate_w = plate_w - plat_radius * 2
# plate_d = plate_d - plat_radius * 2

plate_w2 = plate_w * 0.9
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

c_cube = Cube(size=(c_w, c_d, c_h)).translate((0, c_d / 2, plate_h))
c_cube_tx = -c_w / 2 + plate_w / 2 - c_dx
c_cube = c_cube.translate((c_cube_tx, 0, 0))
dst += c_cube

dst.render()

# %%
class InsetBearing(SolxObject):
    def __init__(
        self,
        c_c_cube_w1 = 3.0,
        c_c_cube_w2 = 5.0,
        c_c_cube_d2 = 2.0,
        c_c_r1 = 7,
        c_c_r2 = 3,
        c_c_h = 10.0,
        c_mgn = 0.3,
    ):
        cyl1 = Cylinder(radius=c_c_r1, height=c_c_h, segments=64)
        cyl2 = Cylinder(radius=c_c_r2, height=c_c_h, segments=64)
        cyl = cyl1 - cyl2

        c1_w = c_c_cube_w1
        c1_d = c_c_r1
        c1_h = c_c_h
        c1 = Cube(size=(c1_w, c1_d, c1_h))
        c1_ty = -c1_d / 2
        c1 = c1.translate((0, c1_ty, 0))
        cyl -= c1

        c2_w = c_c_cube_w2
        c2_d = c_c_cube_d2
        c2_h = c_c_h
        c2 = Cube(size=(c2_w, c2_d, c2_h))
        c2_ty = - c_c_r2 - (c_c_r1 - c_c_r2) / 2
        c2 = c2.translate((0, c2_ty, 0))
        cyl -= c2

        inset1 = Cube(size=(c1_w - c_mgn, c1_d  - c_mgn , c1_h))
        inset1 = inset1.translate((0, c1_ty, 0))
        inset2 = Cube(size=(c2_w - c_mgn, c2_d - c_mgn, c2_h))
        inset2 = inset2.translate((0, c2_ty, 0))
        inset = inset1 + inset2 - cyl2
    
        super().__init__(openscad_node=cyl.node)
        self.inset = inset

    def param_apply(self, func_name: str, params: Vec3) -> InsetBearing:
        dst = copy.deepcopy(self)
        dst = dst.param_apply(func_name, params)
        dst.inset = self.inset.param_apply(func_name, params)
        return dst


c_c_cube_w1 = 3.0
c_c_cube_w2 = 5.0
c_c_cube_d2 = 2.0

c_c_r1 = 7
c_c_r2 = 3
c_c_h = 10.0

c_mgn = 0.3

inset_bearing = InsetBearing(
    c_c_cube_w1=c_c_cube_w1,
    c_c_cube_w2=c_c_cube_w2,
    c_c_cube_d2=c_c_cube_d2,
    c_c_r1=c_c_r1,
    c_c_r2=c_c_r2,
    c_c_h=c_c_h,
    c_mgn=c_mgn,
)

(inset_bearing + inset_bearing.inset).render()
# inset.render()


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
        wide_slot_ty = -inner_radius - (outer_radius - inner_radius) / 2
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
        dst = dst.param_apply(func_name, params)
        dst.inset = self.inset.param_apply(func_name, params)
        return dst


slotted_bearing = SlottedBearing(
    outer_radius=7.0,
    inner_radius=3.0,
    height=10.0,
    slot_width_narrow=3.0,
    slot_width_wide=5.0,
    slot_depth_wide=2.0,
    clearance_margin=0.3,
)

if __name__ == "__main__":
    (slotted_bearing + slotted_bearing.inset).render()

# %%
