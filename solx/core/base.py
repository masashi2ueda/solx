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

    def save_scad(self, path: str) -> None:
        """Save the SolxObject as an OpenSCAD (.scad) file.

        Args:
            path(str): The file path to save the .scad file.
        """
        solid.scad_render_to_file(self.node, path)

    def save_stl(self, path: str) -> None:
        """Export the SolxObject as an STL file.

        Args:
            path(str): The file path to save the .stl file.
        """
        _renderer.render(self.node, outfile=path)

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

    def rotate(self, rotation_angles: Vector3D) -> SolxObject:
        """Rotate the SolxObject by given angles around each axis.

        Args:
            rotation_angles: The rotation angles (in degrees) as a tuple, numpy array, float, or list.

        Returns:
            Self for method chaining.
        """
        normalized_angles = normalize_vector3d(rotation_angles)
        return SolxObject(solid.rotate(normalized_angles)(self.node))

    def rotate_x(self, angle: float) -> SolxObject:
        """Rotate the SolxObject around the X-axis.

        Args:
            angle: The rotation angle (in degrees) around the X-axis.

        Returns:
            Self for method chaining.
        """
        return self.rotate((angle, 0.0, 0.0))

    def rotate_y(self, angle: float) -> SolxObject:
        """Rotate the SolxObject around the Y-axis.

        Args:
            angle: The rotation angle (in degrees) around the Y-axis.

        Returns:
            Self for method chaining.
        """
        return self.rotate((0.0, angle, 0.0))

    def rotate_z(self, angle: float) -> SolxObject:
        """Rotate the SolxObject around the Z-axis.

        Args:
            angle: The rotation angle (in degrees) around the Z-axis.

        Returns:
            Self for method chaining.
        """
        return self.rotate((0.0, 0.0, angle))

    def __add__(self, other: SolxObject) -> SolxObject:
        """Union operation using + operator.

        Args:
            other: The SolxObject to union with this object.

        Returns:
            A new SolxObject representing the union of both objects.
        """
        return SolxObject(solid.union()(self.node, other.node))

    def __sub__(self, other: SolxObject) -> SolxObject:
        """Difference operation using - operator.

        Args:
            other: The SolxObject to subtract from this object.

        Returns:
            A new SolxObject representing the difference of both objects.
        """
        return SolxObject(solid.difference()(self.node, other.node))
