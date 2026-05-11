"""Common types for primitive objects.

This module provides type definitions that are commonly used across
different primitive objects in the solx library.
"""

from enum import Enum, auto


class CenterType(Enum):
    """Enumeration of center types for positioning primitive objects.

    This enum defines standard anchor points that can be used to position
    primitive objects consistently across different shapes.

    Attributes:
        BOTTOM_CENTER: Origin at the bottom center of the object.
        CENTER: Origin at the geometric center of the object.
        BOTTOM_LEFT: Origin at the bottom left corner of the object.
    """

    BOTTOM_CENTER = auto()
    CENTER = auto()
    BOTTOM_LEFT = auto()


DefautltCenterType = CenterType.BOTTOM_CENTER
