"""Base classes and core functionality for Solx.

This module provides the fundamental SolxObject wrapper class that unifies
SolidPython/OpenSCAD nodes with additional utility methods and transforms.
"""
from __future__ import annotations

import solid
from solid.objects import OpenSCADObject
from viewscad import Renderer

from solx.config.openscad import get_openscad_path
from solx.core.vector import Vector3D, normalize_vector3d

# Initialize renderer with configured OpenSCAD path
_renderer = Renderer(openscad_path=get_openscad_path())


class SolxObject:
    """Wrapper class for SolidPython/OpenSCAD nodes.

    This class provides a unified interface for Solx objects, allowing
    additional utility methods, transforms, and metadata.
    """

    def __init__(self, openscad_node: OpenSCADObject) -> None:
        """Initialize SolxObject with a SolidPython node.

        Args:
            openscad_node: The SolidPython/OpenSCAD node to wrap.
        """
        self.node = openscad_node

    def render(self) -> None:
        """Render the SolxObject using ViewSCAD Renderer.

        This method uses the configured OpenSCAD executable to render the object.
        """
        _renderer.render(self.node)

    def translate(self, translation_vector: Vector3D) -> SolxObject:
        """Translate the SolxObject by a given vector.

        Args:
            translation_vector: The translation vector as a tuple, numpy array, float, or list.

        Returns:
            Self for method chaining.
        """
        normalized_vector = normalize_vector3d(translation_vector)
        return SolxObject(solid.translate(normalized_vector)(self.node))

    def translate_x(self, distance: float) -> SolxObject:
        """Translate the SolxObject along the X-axis.

        Args:
            distance: The distance to translate along the X-axis.

        Returns:
            Self for method chaining.
        """
        return self.translate((distance, 0.0, 0.0))

    def translate_y(self, distance: float) -> SolxObject:
        """Translate the SolxObject along the Y-axis.

        Args:
            distance: The distance to translate along the Y-axis.

        Returns:
            Self for method chaining.
        """
        return self.translate((0.0, distance, 0.0))

    def translate_z(self, distance: float) -> SolxObject:
        """Translate the SolxObject along the Z-axis.

        Args:
            distance: The distance to translate along the Z-axis.

        Returns:
            Self for method chaining.
        """
        return self.translate((0.0, 0.0, distance))
