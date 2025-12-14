"""Cylinder primitive for 3D modeling.

This module provides a cylinder primitive with configurable positioning origins.
"""
# %%
import solid

from solx.core import SolxObject
from solx.primitives.types import CenterType


class cylinder(SolxObject):
    """A cylinder primitive for 3D modeling.

    This class creates a cylinder with configurable radius, height, and positioning origin.
    The cylinder can be positioned with different origin types such as bottom center,
    geometric center, or bottom left corner.

    Attributes:
        radius (float): Radius of the cylinder.
        height (float): Height of the cylinder.
        center (CenterType): Center type for positioning the cylinder.
    """

    def __init__(
        self,
        radius: float = 1.0,
        height: float = 1.0,
        center: CenterType = CenterType.BOTTOM_CENTER,
        segments: int = 32
    ):
        """Create a cylinder primitive.

        Args:
            radius (float, optional): Radius of the cylinder. Defaults to 1.0.
            height (float, optional): Height of the cylinder. Defaults to 1.0.
            center (CenterType, optional): Center type for positioning the cylinder. Defaults to CenterType.BOTTOM_CENTER.
            segments (int, optional): Number of segments to approximate the cylinder. Defaults to 32.

        Returns:
            SolxObject: A cylinder object positioned according to the specified origin type.
        """
        node_cylinder = solid.cylinder(
            r=radius,
            h=height,
            center=True,
            segments=segments)
        cyl = SolxObject(node_cylinder)

        if center == CenterType.BOTTOM_CENTER:
            translation = (0, 0, height / 2)
        elif center == CenterType.CENTER:
            translation = (0, 0, 0)
        elif center == CenterType.BOTTOM_LEFT:
            translation = (radius, radius, height / 2)
        else:
            raise ValueError("Invalid CenterType")

        cyl = cyl.translate(translation)

        super().__init__(cyl.node)
