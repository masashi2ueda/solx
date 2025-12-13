"""Base classes and core functionality for Solx.

This module provides the fundamental SolxObject wrapper class that unifies
SolidPython/OpenSCAD nodes with additional utility methods and transforms.
"""

from solid.objects import OpenSCADObject
from viewscad import Renderer

from solx.config.openscad import get_openscad_path

_renderer = Renderer(openscad_path=get_openscad_path())


class SolxObject:
    """Wrapper class for SolidPython/OpenSCAD nodes.

    This class provides a unified interface for Solx objects, allowing
    additional utility methods, transforms, and metadata.
    """

    def __init__(self, node: OpenSCADObject):
        """Initialize SolxObject with a SolidPython node.

        Args:
            node (OpenSCADObject): The SolidPython/OpenSCAD node to wrap.
        """
        self.node = node

    def render(self)-> None:
        """Render the SolxObject using ViewSCAD Renderer.

        This method uses the configured OpenSCAD executable to render
        the object.

        Returns:
            None
        """
        _renderer.render(self.node)
