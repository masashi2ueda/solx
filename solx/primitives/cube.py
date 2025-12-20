"""Cube primitive for 3D modeling.

This module provides a cube primitive with configurable positioning origins.
"""
# %%
from typing import Optional

import solid

from solx.core import SolxObject, Vector3D
from solx.primitives.types import CenterType
from solx.primitives.utils import normalize_size_params


class Cube(SolxObject):
    """A cube primitive for 3D modeling.

    This class creates a cube with configurable size and positioning origin.
    The cube can be positioned with different origin types such as bottom center,
    geometric center, or bottom left corner.

    Attributes:
        size (Vector3D): Size of the cube along each axis.
        center (CenterType): Center type for positioning the cube.
        position (Vector3D): Position of the cube.
    """

    def __init__(
        self,
        size: Optional[Vector3D] = None,
        *,
        width: Optional[float] = None,
        depth: Optional[float] = None,
        height: Optional[float] = None,
        center: CenterType = CenterType.BOTTOM_CENTER
    ):
        """Create a cube primitive.

        Args:
            size (Vector3D, optional): Size of the cube along each axis
                (width, depth, height order). Can be float, tuple, list, or ndarray.
            width (float, optional): Width (X-axis) of the cube. Used if size is not
                provided.
            depth (float, optional): Depth (Y-axis) of the cube. Used if size is not
                provided.
            height (float, optional): Height (Z-axis) of the cube. Used if size is not
                provided.
            center (CenterType): Center type for positioning the cube.

        Raises:
            ValueError: If conflicting parameters are given.
        """
        size_tuple = normalize_size_params(
            size=size,
            width=width,
            depth=depth,
            height=height
        )
        node_cube = solid.cube(size=size_tuple, center=True)
        cube = SolxObject(node_cube)

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

        # Apply center translation and position translation
        cube = cube.translate(center_translation)

        self.size_tuple = size_tuple
        super().__init__(cube.node)

