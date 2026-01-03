
"""Solx - A 3D solid modeling library.

This package provides classes and utilities for creating and manipulating
3D geometric objects including cubes, cylinders, and other primitives.
"""

from .config import EnvConfig
from .core import SolxObject, Vector3D, normalize_vector3d
from .primitives import (
    CapsuleCube,
    CenterType,
    Cube,
    Cylinder,
    HollowCube,
    PolygonExtrude,
    RoundedCube,
)

__all__ = [
    "SolxObject",
    "Vector3D",
    "normalize_vector3d",
    "Cube",
    "Cylinder",
    "CenterType",
    "RoundedCube",
    "PolygonExtrude",
    "CapsuleCube",
    "EnvConfig",
    "HollowCube",
]
