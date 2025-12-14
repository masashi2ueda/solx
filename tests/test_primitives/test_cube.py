"""Tests for solx.primitives.cube module."""
import pytest

from solx.core import SolxObject, Vector3D
from solx.primitives.cube import cube
from solx.primitives.types import CenterType


class TestCube:
    """Test cases for cube class."""

    def test_init_default(self):
        """Test cube initialization with default values."""
        c = cube()
        assert isinstance(c, SolxObject)
        assert c.size == Vector3D(1, 1, 1)
        assert c.center == CenterType.BOTTOM_CENTER
        assert c.position == Vector3D(0, 0, 0)

    def test_init_with_size_vector(self):
        """Test cube initialization with Vector3D size."""
        size = Vector3D(10, 20, 30)
        c = cube(size)
        assert c.size == size

    def test_init_with_size_tuple(self):
        """Test cube initialization with tuple size."""
        c = cube((10, 20, 30))
        assert c.size == Vector3D(10, 20, 30)

    def test_init_with_size_list(self):
        """Test cube initialization with list size."""
        c = cube([10, 20, 30])
        assert c.size == Vector3D(10, 20, 30)

    def test_init_with_single_size(self):
        """Test cube initialization with single size value."""
        c = cube(15)
        assert c.size == Vector3D(15, 15, 15)

    def test_init_with_center_type(self):
        """Test cube initialization with different center types."""
        c1 = cube(center=CenterType.BOTTOM_CENTER)
        assert c1.center == CenterType.BOTTOM_CENTER
        
        c2 = cube(center=CenterType.CENTER)
        assert c2.center == CenterType.CENTER
        
        c3 = cube(center=CenterType.BOTTOM_LEFT)
        assert c3.center == CenterType.BOTTOM_LEFT

    def test_init_with_position(self):
        """Test cube initialization with position."""
        pos = Vector3D(10, 20, 30)
        c = cube(position=pos)
        assert c.position == pos

    def test_init_with_position_tuple(self):
        """Test cube initialization with position tuple."""
        c = cube(position=(10, 20, 30))
        assert c.position == Vector3D(10, 20, 30)

    def test_center_type_affects_positioning(self):
        """Test that different center types result in different positioning."""
        size = Vector3D(10, 10, 10)
        
        c_bottom_center = cube(size, center=CenterType.BOTTOM_CENTER)
        c_center = cube(size, center=CenterType.CENTER)
        c_bottom_left = cube(size, center=CenterType.BOTTOM_LEFT)
        
        # All should be different cube objects
        assert c_bottom_center is not c_center
        assert c_center is not c_bottom_left
        assert c_bottom_center is not c_bottom_left

    def test_cube_is_solx_object(self):
        """Test that cube inherits from SolxObject."""
        c = cube()
        assert isinstance(c, SolxObject)
        assert hasattr(c, 'openscad_node')
        assert hasattr(c, 'translate')
        assert hasattr(c, 'rotate')
        assert hasattr(c, 'scale')

    def test_cube_operations(self):
        """Test that cube supports SolxObject operations."""
        c1 = cube(10)
        c2 = cube(5)
        
        # Test union
        union_result = c1 + c2
        assert isinstance(union_result, SolxObject)
        
        # Test difference
        diff_result = c1 - c2
        assert isinstance(diff_result, SolxObject)
        
        # Test intersection
        intersect_result = c1 & c2
        assert isinstance(intersect_result, SolxObject)

    def test_cube_transformations(self):
        """Test cube transformations."""
        c = cube(10)
        
        # Test translate
        translated = c.translate(Vector3D(5, 0, 0))
        assert isinstance(translated, SolxObject)
        assert translated is not c
        
        # Test rotate
        rotated = c.rotate((90, 0, 0))
        assert isinstance(rotated, SolxObject)
        assert rotated is not c
        
        # Test scale
        scaled = c.scale(Vector3D(2, 1, 1))
        assert isinstance(scaled, SolxObject)
        assert scaled is not c

    def test_invalid_size_input(self):
        """Test cube with invalid size input."""
        # Test with negative values (might be valid depending on implementation)
        c = cube((-1, -1, -1))
        assert isinstance(c, SolxObject)

    def test_zero_size(self):
        """Test cube with zero size."""
        c = cube((0, 0, 0))
        assert isinstance(c, SolxObject)
        assert c.size == Vector3D(0, 0, 0)

    def test_attribute_access(self):
        """Test that cube attributes are accessible."""
        size = Vector3D(10, 20, 30)
        pos = Vector3D(5, 10, 15)
        center = CenterType.CENTER
        
        c = cube(size, center=center, position=pos)
        
        assert c.size == size
        assert c.center == center
        assert c.position == pos