"""Capsule cube primitive for 3D modeling.

This module provides the CapsuleCube class, which creates a cube with rounded edges
by combining a central rectangular cube with cylindrical caps on opposite sides.
The capsule cube can be configured with different sizes, positioning origins,
and segment counts for smooth edge approximation.
"""

# %%
from solx.core.base import SolxObject, Vec3
from solx.primitives.cube import Cube
from solx.primitives.cylinder import Cylinder
from solx.primitives.types import CenterType


# %%
class CapsuleCube(SolxObject):
    def __init__(self,
        size: Vec3,
        segments: int = 32,
        center: CenterType = CenterType.BOTTOM_CENTER
    ):
        w = size[0]
        d = size[1]
        h = size[2]

        cyl = Cylinder(radius=d / 2, height=h, center=CenterType.BOTTOM_CENTER, segments=segments)
        cube = Cube(size=(w - d * 2, d, h), center=CenterType.BOTTOM_CENTER)
        dx = (w - 2 * d) / 2
        capsule_cube = cube + cyl.translate((-dx, 0, 0)) + cyl.translate((dx, 0, 0))
        if center == CenterType.BOTTOM_CENTER:
            pass
        if center == CenterType.CENTER:
            capsule_cube = capsule_cube.translate((0, 0, -h / 2))
        if center == CenterType.BOTTOM_LEFT:
            capsule_cube = capsule_cube.translate((w / 2, d / 2, 0))

        super().__init__(capsule_cube.node)

if __name__ == "__main__":
    # Example usage
    capsule_cube = CapsuleCube(size=(100, 20, 40))
    capsule_cube.render()

# %%
