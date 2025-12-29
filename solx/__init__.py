
"""Solx - A 3D solid modeling library.

This package provides classes and utilities for creating and manipulating
3D geometric objects including cubes, cylinders, and other primitives.
"""

# pkg_resources deprecation warning を抑制
import warnings

warnings.filterwarnings("ignore",
                       message="pkg_resources is deprecated",
                       category=UserWarning)

from .core import SolxObject, Vector3D, normalize_vector3d
from .primitives.cube import Cube
from .primitives.cylinder import Cylinder
from .primitives.polygon_extlude import PolygonExtrude
from .primitives.rounded_cube import RoundedCube
from .primitives.types import CenterType

__all__ = [
    "SolxObject",
    "Vector3D",
    "normalize_vector3d",
    "Cube",
    "Cylinder",
    "CenterType",
    "RoundedCube",
    "PolygonExtrude",
]
