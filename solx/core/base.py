"""Base classes and core functionality for Solx.

This module provides the fundamental SolxObject wrapper class that unifies
SolidPython/OpenSCAD nodes with additional utility methods and transforms.
"""
from __future__ import annotations

import copy
from typing import Self

import numpy as np
import solid
from solid.objects import OpenSCADObject
from viewscad import Renderer

from solx.config.openscad import get_openscad_path

# Initialize renderer with configured OpenSCAD path
_renderer = Renderer(openscad_path=get_openscad_path())

Vec3 = tuple[float, float, float]

def param_apply(func_name: str, params: Vec3, target: OpenSCADObject|Point3D) -> OpenSCADObject|Point3D:
    if isinstance(target, OpenSCADObject):
        if func_name == 'translate':
            return solid.translate(params)(target)
        elif func_name == 'rotate':
            return solid.rotate(params)(target)
        elif func_name == 'scale':
            return solid.scale(params)(target)
        elif func_name == 'mirror':
            return solid.mirror(params)(target)
        else:
            raise ValueError(f"Unknown function name: {func_name}")
    elif isinstance(target, Point3D):
        return target._param_apply(func_name, params)
    else:
        raise ValueError("Target must be OpenSCADObject or Point3D")


class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def to_tuple(self) -> Vec3:
        return (self.x, self.y, self.z)

    def translate(self, translation_vector: Vec3) -> Point3D:
        dx, dy, dz = translation_vector
        return Point3D(self.x + dx, self.y + dy, self.z + dz)

    def rotate(self, rotation_angles: Vec3) -> Point3D:
        rx, ry, rz = np.radians(rotation_angles)
        # Rotation matrices around each axis
        Rx = np.array([[1, 0, 0],
                       [0, np.cos(rx), -np.sin(rx)],
                       [0, np.sin(rx), np.cos(rx)]])
        Ry = np.array([[np.cos(ry), 0, np.sin(ry)],
                       [0, 1, 0],
                       [-np.sin(ry), 0, np.cos(ry)]])
        Rz = np.array([[np.cos(rz), -np.sin(rz), 0],
                       [np.sin(rz), np.cos(rz), 0],
                       [0, 0, 1]])
        # Combined rotation matrix
        R = Rz @ Ry @ Rx
        # Original point as vector
        p = np.array([self.x, self.y, self.z])
        # Rotated point
        p_rotated = R @ p
        return Point3D(p_rotated[0], p_rotated[1], p_rotated[2])
    
    def scale(self, scale_factors: Vec3) -> Point3D:
        sx, sy, sz = scale_factors
        return Point3D(self.x * sx, self.y * sy, self.z * sz)
    
    def mirror(self, axis: Vec3) -> Point3D:
        mx, my, mz = axis
        return Point3D(
            -self.x if mx else self.x,
            -self.y if my else self.y,
            -self.z if mz else self.z
        )
    
    def _param_apply(self, func_name: str, params: Vec3) -> Point3D:
        if func_name == 'translate':
            return self.translate(params)
        elif func_name == 'rotate':
            return self.rotate(params)
        elif func_name == 'scale':
            return self.scale(params)
        elif func_name == 'mirror':
            return self.mirror(params)
        else:
            raise ValueError(f"Unknown function name: {func_name}")

    def distance_to(self, other: Point3D) -> float:
        return np.sqrt((self.x - other.x) ** 2 +
                       (self.y - other.y) ** 2 +
                       (self.z - other.z) ** 2)

class SolxObject:
    """Wrapper class for SolidPython/OpenSCAD nodes.

    This class provides a unified interface for Solx objects, allowing
    additional utility methods, transforms, and metadata.
    """

    def __init__(
        self,
        openscad_node: OpenSCADObject=None,
        ) -> None:
        """Initialize SolxObject with a SolidPython node.

        Args:
            openscad_node: The SolidPython/OpenSCAD node to wrap.
        """
        self.node = openscad_node

    @property
    def all_params(self) -> list[OpenSCADObject]:
        return [self.node]

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

    def _param_apply(self, func_name: str, params: Vec3) -> SolxObject:
        if func_name == 'translate':
            return SolxObject(openscad_node=solid.translate(params)(self.node))
        elif func_name == 'rotate':
            return SolxObject(openscad_node=solid.rotate(params)(self.node))
        elif func_name == 'scale':
            return SolxObject(openscad_node=solid.scale(params)(self.node))
        elif func_name == 'mirror':
            return SolxObject(openscad_node=solid.mirror(params)(self.node))
        else:
            raise ValueError(f"Unknown function name: {func_name}")

    def param_apply(self, func_name: str, params: Vec3) -> SolxObject:
        node = param_apply(func_name, params, self.node)
        return SolxObject(openscad_node=node)

    def translate(self, translation_vector: Vec3) -> Self:
        return self.param_apply('translate', translation_vector)
    def rotate(self, rotation_angles: Vec3) -> Self:
        return self.param_apply('rotate', rotation_angles)
    def scale(self, scale_factors: Vec3) -> Self:
        return self.param_apply('scale', scale_factors)
    def mirror(self, axis: Vec3) -> Self:
        return self.param_apply('mirror', axis)

    def copy(self) -> Self:
        return copy.deepcopy(self)
    
    def other_param_apply(self, func_name: str, other: SolxObject) -> Self:
        dst = self.copy()
        src_node = self.node
        other_node = other.node
        dst_node = None
        if func_name == 'union':
            dst_node = solid.union()(src_node, other_node)
        elif func_name == 'difference':
            dst_node = solid.difference()(src_node, other_node)
        else:
            raise ValueError(f"Unknown function name: {func_name}")
        dst.node = dst_node
        return dst

    def __add__(self, other: SolxObject) -> Self:
        return self.other_param_apply('union', other)

    def __sub__(self, other: SolxObject) -> Self:
        return self.other_param_apply('difference', other)
