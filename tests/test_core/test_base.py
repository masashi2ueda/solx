"""Tests for solx.core.base module."""
import pytest
import solid
from solid.objects import OpenSCADObject

from solx.core.base import SolxObject
from solx.core.vector import Vector3D


class TestSolxObject:
    """Test cases for SolxObject class."""

    def test_init_with_openscad_object(self):
        """Test SolxObject initialization with OpenSCAD object."""
        # Create a simple OpenSCAD cube
        scad_cube = solid.cube([10, 10, 10])
        solx_obj = SolxObject(scad_cube)
        
        assert solx_obj.openscad_node is scad_cube
        assert isinstance(solx_obj.openscad_node, OpenSCADObject)

    def test_translate_method(self):
        """Test translate method."""
        scad_cube = solid.cube([10, 10, 10])
        solx_obj = SolxObject(scad_cube)
        
        # Test translation with Vector3D
        translated = solx_obj.translate(Vector3D(5, 0, 0))
        assert isinstance(translated, SolxObject)
        assert translated is not solx_obj  # Should return new object

    def test_translate_with_tuple(self):
        """Test translate method with tuple input."""
        scad_cube = solid.cube([10, 10, 10])
        solx_obj = SolxObject(scad_cube)
        
        # Test translation with tuple
        translated = solx_obj.translate((5, 0, 0))
        assert isinstance(translated, SolxObject)

    def test_translate_with_list(self):
        """Test translate method with list input."""
        scad_cube = solid.cube([10, 10, 10])
        solx_obj = SolxObject(scad_cube)
        
        # Test translation with list
        translated = solx_obj.translate([5, 0, 0])
        assert isinstance(translated, SolxObject)

    def test_rotate_method(self):
        """Test rotate method."""
        scad_cube = solid.cube([10, 10, 10])
        solx_obj = SolxObject(scad_cube)
        
        # Test rotation
        rotated = solx_obj.rotate((90, 0, 0))
        assert isinstance(rotated, SolxObject)
        assert rotated is not solx_obj  # Should return new object

    def test_scale_method(self):
        """Test scale method."""
        scad_cube = solid.cube([10, 10, 10])
        solx_obj = SolxObject(scad_cube)
        
        # Test scaling
        scaled = solx_obj.scale(Vector3D(2, 1, 1))
        assert isinstance(scaled, SolxObject)
        assert scaled is not solx_obj  # Should return new object

    def test_union_operator(self):
        """Test union operation using + operator."""
        scad_cube1 = solid.cube([10, 10, 10])
        scad_cube2 = solid.cube([10, 10, 10])
        solx_obj1 = SolxObject(scad_cube1)
        solx_obj2 = SolxObject(scad_cube2)
        
        # Test union
        union_obj = solx_obj1 + solx_obj2
        assert isinstance(union_obj, SolxObject)

    def test_difference_operator(self):
        """Test difference operation using - operator."""
        scad_cube1 = solid.cube([10, 10, 10])
        scad_cube2 = solid.cube([5, 5, 5])
        solx_obj1 = SolxObject(scad_cube1)
        solx_obj2 = SolxObject(scad_cube2)
        
        # Test difference
        diff_obj = solx_obj1 - solx_obj2
        assert isinstance(diff_obj, SolxObject)

    def test_intersection_operator(self):
        """Test intersection operation using & operator."""
        scad_cube1 = solid.cube([10, 10, 10])
        scad_cube2 = solid.cube([5, 5, 5])
        solx_obj1 = SolxObject(scad_cube1)
        solx_obj2 = SolxObject(scad_cube2)
        
        # Test intersection
        intersect_obj = solx_obj1 & solx_obj2
        assert isinstance(intersect_obj, SolxObject)

    def test_render_method_exists(self):
        """Test that render method exists and is callable."""
        scad_cube = solid.cube([10, 10, 10])
        solx_obj = SolxObject(scad_cube)
        
        # Check that render method exists
        assert hasattr(solx_obj, 'render')
        assert callable(getattr(solx_obj, 'render'))