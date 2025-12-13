"""Cube primitive for 3D modeling.

This module provides a cube primitive with configurable positioning origins.
"""
# %%
from enum import Enum, auto

import solid

from solx.core import SolxObject, Vector3D, normalize_vector3d


# %%
class OriginType(Enum):
    """Enumeration of origin types for positioning cube primitives.

    Attributes:
        BOTTOM_CENTER: Origin at the bottom center of the cube.
        CENTER: Origin at the geometric center of the cube.
        BOTTOM_LEFT: Origin at the bottom left corner of the cube.
    """
    BOTTOM_CENTER = auto()
    CENTER = auto()
    BOTTOM_LEFT = auto()


class cube(SolxObject):
    """A cube primitive for 3D modeling.

    This class creates a cube with configurable size and positioning origin.
    The cube can be positioned with different origin types such as bottom center,
    geometric center, or bottom left corner.

    Attributes:
        size (Vector3D): Size of the cube along each axis.
        center (OriginType): Origin type for positioning the cube.
    """

    def __init__(
        self,
        size: Vector3D = 1.0,
        center: OriginType = OriginType.BOTTOM_CENTER
    ):
        """Create a cube primitive.

        Args:
            size (Vector3D, optional): Size of the cube along each axis. Defaults to 1.0.
            center (OriginType, optional): Origin type for positioning the cube. Defaults to OriginType.BOTTOM_CENTER.

        Returns:
            SolxObject: A cube object positioned according to the specified origin type.
        """
        size_tuple = normalize_vector3d(size)
        node_cube = solid.cube(size=size_tuple, center=True)
        cube = SolxObject(node_cube)

        if center == OriginType.BOTTOM_CENTER:
            translation = (0, 0, size_tuple[2] / 2)
        elif center == OriginType.CENTER:
            translation = (0, 0, 0)
        elif center == OriginType.BOTTOM_LEFT:
            translation = (size_tuple[0] / 2, size_tuple[1] / 2, size_tuple[2] / 2)
        else:
            raise ValueError("Invalid OriginType")

        cube = cube.translate(translation)

        super().__init__(cube.node)

