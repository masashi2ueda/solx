"""Utility functions for primitive shapes."""
from typing import Tuple

from solx.core import Vector3D, normalize_vector3d


def normalize_size_params(
    size: Vector3D | None = None,
    width: float | None = None,
    depth: float | None = None,
    height: float | None = None,
) -> Tuple[float, float, float]:
    """Normalize size parameters into a consistent size tuple.

    Args:
        size (Vector3D | None): Size of the shape along each axis.
        width (float | None): Width (X-axis) of the shape.
        depth (float | None): Depth (Y-axis) of the shape.
        height (float | None): Height (Z-axis) of the shape.

    Returns:
        Tuple[float, float, float]: Normalized size tuple (width, depth, height).

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

    return size_tuple
