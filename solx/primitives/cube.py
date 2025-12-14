"""Cube primitive for 3D modeling.

This module provides a cube primitive with configurable positioning origins.
"""
# %%
from typing import Optional

import solid

from solx.core import SolxObject, Vector3D, normalize_vector3d
from solx.primitives.types import CenterType


class cube(SolxObject):
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
        position: Optional[Vector3D] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        z: Optional[float] = None,
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
            position (Vector3D, optional): Position of the cube. Can be float, tuple,
                list, or ndarray.
            x (float, optional): X position of the cube. Used if position is not
                provided.
            y (float, optional): Y position of the cube. Used if position is not
                provided.
            z (float, optional): Z position of the cube. Used if position is not
                provided.
            center (CenterType): Center type for positioning the cube.

        Raises:
            ValueError: If conflicting parameters are given.
        """
        # Handle size parameters
        if size is not None:
            if any(dim is not None for dim in [width, depth, height]):
                raise ValueError(
                    "Cannot specify both 'size' and individual dimensions "
                    "(width, depth, height)"
                )
            size_tuple = normalize_vector3d(size)
        elif any(dim is not None for dim in [width, depth, height]):
            if any(dim is None for dim in [width, depth, height]):
                raise ValueError(
                    "If using individual dimensions, all of "
                    "width, depth, and height must be specified"
                )
            size_tuple = (float(width), float(depth), float(height))
        else:
            # Default to unit cube
            size_tuple = (1.0, 1.0, 1.0)

        # Handle position parameters
        if position is not None:
            if any(pos is not None for pos in [x, y, z]):
                raise ValueError("Cannot specify both 'position' and individual coordinates (x, y, z)")
            position_tuple = normalize_vector3d(position)
        elif any(pos is not None for pos in [x, y, z]):
            # Use provided coordinates, default missing ones to 0
            position_tuple = (
                float(x) if x is not None else 0.0,
                float(y) if y is not None else 0.0,
                float(z) if z is not None else 0.0
            )
        else:
            # Default to origin
            position_tuple = (0.0, 0.0, 0.0)

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
        total_translation = (
            center_translation[0] + position_tuple[0],
            center_translation[1] + position_tuple[1],
            center_translation[2] + position_tuple[2]
        )

        cube = cube.translate(total_translation)

        super().__init__(cube.node)

