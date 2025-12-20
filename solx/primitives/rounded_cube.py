# %%
"""Rounded cube primitive implementation."""
import solid

from solx.core import SolxObject, Vector3D
from solx.primitives.types import CenterType
from solx.primitives.utils import normalize_size_params

SMALL_VALUE = 1e-6

class RoundedCube(SolxObject):
    """A rounded cube primitive for 3D modeling.

    This class creates a cube with rounded corners, configurable size, corner radius,
    and positioning origin. The cube can be positioned with different origin types such as
    bottom center, geometric center, or bottom left corner.

    Attributes:
        size (Vector3D): Size of the cube along each axis.
        radius (float): Radius of the rounded corners.
        center (CenterType): Center type for positioning the cube.
    """

    def __init__(self,
        size: Vector3D | None = None,
        radius: float = 1.0,
        *,
        width: float | None = None,
        depth: float | None = None,
        height: float | None = None,
        segments: int = 32,
        center: CenterType = CenterType.BOTTOM_CENTER

    ):
        """Create a rounded cube primitive.

        Args:
            size (Vector3D | None): Size of the cube along each axis.
            radius (float, optional): Radius of the rounded corners. Defaults to 1.0.
            width (float | None, optional): Width (X-axis) of the cube. Used if size is not
                provided.
            depth (float | None, optional): Depth (Y-axis) of the cube. Used if size is not
                provided.
            height (float | None, optional): Height (Z-axis) of the cube. Used if size is not
                provided.
            segments (int, optional): Number of segments to approximate the rounded corners.
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
        cube_size_tuple = (
            size_tuple[0] - 2 * radius,
            size_tuple[1] - 2 * radius,
            size_tuple[2] - 2 * SMALL_VALUE,
        )

        base_cube = solid.cube(
            size=cube_size_tuple,
            center=True
        )
        corner_cylinder = solid.cylinder(
            r=radius,
            segments=segments,
            h = SMALL_VALUE,
            center=True
        )

        rounded_cube_node = solid.minkowski()(base_cube, corner_cylinder)
        rounded_cube = SolxObject(rounded_cube_node)

        if center == CenterType.BOTTOM_CENTER:
            center_translation = (0, 0, size_tuple[2] / 2)
        elif center == CenterType.CENTER:
            center_translation = (0, 0, 0)
        elif center == CenterType.BOTTOM_LEFT:
            center_translation = (
                size_tuple[0] / 2, size_tuple[1] / 2, size_tuple[2] / 2
            )
        else:
            raise ValueError("Invalid CenterType")

        rounded_cube = rounded_cube.translate(center_translation)

        super().__init__(rounded_cube.node)

