"""Vector utilities for 3D operations.

This module provides:
- Vector3D: type alias for 3D vector inputs
- normalize_vector3d: function to convert various input types to 3D tuples
"""

from typing import TypeAlias, Union

import numpy as np

# Type alias for 3D point/vector inputs
Vector3D: TypeAlias = Union[tuple[float, float, float], list[float], np.ndarray, float]


def normalize_vector3d(vector_input: Vector3D) -> tuple[float, float, float]:
    """Convert various input types to a 3-element float tuple.

    Args:
        vector_input: Input value to convert. Can be a float, tuple, list,
            or numpy array.

    Returns:
        A 3-element tuple of floats.

    Raises:
        ValueError: If the input has incorrect dimensions or length.
        TypeError: If the input type is not supported.
    """
    if isinstance(vector_input, float):
        return (vector_input, vector_input, vector_input)

    if isinstance(vector_input, np.ndarray):
        if vector_input.ndim != 1 or vector_input.shape[0] != 3:
            raise ValueError(
                "NumPy array must be one-dimensional with exactly three elements"
            )
        return tuple(vector_input.astype(float))

    if isinstance(vector_input, (tuple, list)):
        if len(vector_input) != 3:
            raise ValueError(
                f"{type(vector_input).__name__} must have exactly three elements"
            )
        return tuple(float(x) for x in vector_input)

    raise TypeError(f"Unsupported type for vector conversion: {type(vector_input)}")
