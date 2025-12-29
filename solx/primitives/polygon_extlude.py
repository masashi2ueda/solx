
"""Polygon extrusion primitive for 3D modeling.

This module provides the PolygonExtrude class for creating 3D objects by extruding
2D polygon shapes along the Z-axis using the SolidPython library.
"""

import solid

from solx.core import SolxObject


class PolygonExtrude(SolxObject):
    """A polygon extrude primitive for 3D modeling.

    This class creates a 3D object by extruding a 2D polygon shape along the Z-axis.
    The extrusion can be configured with height and positioning origin.

    Attributes:
        points (list[tuple[float, float]]): List of 2D points defining the polygon shape.
        height (float): Height of the extrusion along the Z-axis.
        center (bool): Whether to center the extrusion along the Z-axis.
    """

    def __init__(
        self,
        points: list[tuple[float, float]],
        height: float = 1.0,
    ):
        """Create a polygon extrude primitive.

        Args:
            points (list[tuple[float, float]]): List of 2D points defining the polygon shape.
            height (float, optional): Height of the extrusion along the Z-axis. Defaults to 1.0.

        Returns:
            SolxObject: A polygon extrude object positioned according to the specified parameters.
        """
        node_extrude = solid.linear_extrude(height=height)(
            solid.polygon(points=points)
        )
        super().__init__(node_extrude)
