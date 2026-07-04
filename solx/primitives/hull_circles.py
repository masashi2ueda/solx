# %%
from __future__ import annotations

import copy

from solid import circle, hull, linear_extrude, translate

from solx.core import Point3D, SolxObject, Vec3, param_apply


# -----------------------
# パラメータ
# -----------------------
class HullCircles(SolxObject):
    def __init__(
        self,
        circle_positions: list[tuple[float, float]],
        circle_radiuses: list[float],
        height: float,
    ):
        circles = []
        for (xy, r) in zip(circle_positions, circle_radiuses):
            x, y = xy
            circles.append(translate([x, y])(circle(r=r)))

        shape2d = hull()(*circles)
        solid = linear_extrude(height=height)(shape2d)

        super().__init__(openscad_node=solid)
        self.circle_positions = [Point3D(x, y, 0) for x, y in circle_positions]
        self.circle_radiuses = circle_radiuses


    def param_apply(self, func_name: str, params: Vec3) -> HullCircles:
        dst = copy.deepcopy(self)
        dst.node = param_apply(func_name, params, self.node)
        dst.circle_positions = [param_apply(func_name, params, pt) for pt in self.circle_positions]
        dst.circle_radiuses = self.circle_radiuses
        return dst



if __name__ == "__main__":
    height = 20
    xys = [(0, 0), (10, 10), (-10, -10), (20, -20), (-20, 20)]
    rs = [1, 2, 3, 4, 5]

    hull_circles = HullCircles(circle_positions=xys, circle_radiuses=rs, height=height)
    hull_circles = hull_circles.translate((10, 20, 30))
    print(hull_circles.circle_positions)
    hull_circles.render()

# %%
