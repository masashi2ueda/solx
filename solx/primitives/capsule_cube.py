"""Capsule cube primitive for 3D modeling.

This module provides the CapsuleCube class, which creates a cube with rounded edges
by combining a central rectangular cube with cylindrical caps on opposite sides.
The capsule cube can be configured with different sizes, positioning origins,
and segment counts for smooth edge approximation.
"""

# %%
from solx.core import Vector3D
from solx.core.base import SolxObject
from solx.primitives.cube import Cube
from solx.primitives.cylinder import Cylinder
from solx.primitives.types import CenterType
from solx.primitives.utils import normalize_size_params


# %%
class CapsuleCube(SolxObject):
    """A capsule cube primitive for 3D modeling.

    This class creates a cube with rounded edges, configurable size, edge radius,
    and positioning origin. The cube can be positioned with different origin types such as
    bottom center, geometric center, or bottom left corner.

    Attributes:
        size (Vector3D): Size of the cube along each axis.
        radius (float): Radius of the rounded edges.
        center (CenterType): Center type for positioning the cube.
    """

    def __init__(self,
        size: Vector3D | None = None,
        *,
        width: float | None = None,
        depth: float | None = None,
        height: float | None = None,
        segments: int = 32,
        center: CenterType = CenterType.BOTTOM_CENTER
    ):
        """Create a capsule cube primitive.

        Args:
            size (Vector3D | None): Size of the cube along each axis.
            radius (float, optional): Radius of the rounded edges. Defaults to 1.0.
            width (float | None, optional): Width (X-axis) of the cube. Used if size is not
                provided.
            depth (float | None, optional): Depth (Y-axis) of the cube. Used if size is not
                provided.
            height (float | None, optional): Height (Z-axis) of the cube. Used if size is not
                provided.
            segments (int, optional): Number of segments to approximate the rounded edges.
                Defaults to 32.
            center (CenterType, optional): Center type for positioning the cube.
                Defaults to CenterType.BOTTOM_CENTER.

        Raises:
            ValueError: If conflicting parameters are given.
        """
        size_tuple = normalize_size_params(
            size=size,
            width=width,
            depth=depth,
            height=height
        )
        w = size_tuple[0]
        d = size_tuple[1]
        h = size_tuple[2]

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
