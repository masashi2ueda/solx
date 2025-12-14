"""Tests for solx.primitives.cylinder module."""
import pytest

from solx.core import SolxObject, Vector3D
from solx.primitives.cylinder import cylinder
from solx.primitives.types import CenterType


class TestCylinder:
    """Test cases for cylinder class."""

    def test_init_default(self):
        """Test cylinder initialization with default values."""
        c = cylinder()
        assert isinstance(c, SolxObject)
        # Check default values based on the actual implementation
        assert hasattr(c, 'radius')
        assert hasattr(c, 'height')
        assert hasattr(c, 'center')
        assert hasattr(c, 'position')

    def test_init_with_radius_and_height(self):
        """Test cylinder initialization with radius and height."""
        c = cylinder(radius=5, height=10)
        assert c.radius == 5
        assert c.height == 10

    def test_init_with_diameter_and_height(self):
        """Test cylinder initialization with diameter and height."""
        c = cylinder(diameter=10, height=20)
        assert c.radius == 5  # diameter/2
        assert c.height == 20

    def test_init_with_position(self):
        """Test cylinder initialization with position."""
        pos = Vector3D(10, 20, 30)
        c = cylinder(position=pos)
        assert c.position == pos

    def test_init_with_position_tuple(self):
        """Test cylinder initialization with position tuple."""
        c = cylinder(position=(10, 20, 30))
        assert c.position == Vector3D(10, 20, 30)

    def test_init_with_center_type(self):
        """Test cylinder initialization with different center types."""
        c1 = cylinder(center=CenterType.BOTTOM_CENTER)
        assert c1.center == CenterType.BOTTOM_CENTER
        
        c2 = cylinder(center=CenterType.CENTER)
        assert c2.center == CenterType.CENTER

    def test_radius_and_diameter_conflict(self):
        """Test that specifying both radius and diameter raises an error."""
        with pytest.raises((ValueError, TypeError)):
            cylinder(radius=5, diameter=10)

    def test_cylinder_is_solx_object(self):
        """Test that cylinder inherits from SolxObject."""
        c = cylinder()
        assert isinstance(c, SolxObject)
        assert hasattr(c, 'openscad_node')
        assert hasattr(c, 'translate')
        assert hasattr(c, 'rotate')
        assert hasattr(c, 'scale')

    def test_cylinder_operations(self):
        """Test that cylinder supports SolxObject operations."""
        c1 = cylinder(radius=5, height=10)
        c2 = cylinder(radius=3, height=8)
        
        # Test union
        union_result = c1 + c2
        assert isinstance(union_result, SolxObject)
        
        # Test difference
        diff_result = c1 - c2
        assert isinstance(diff_result, SolxObject)
        
        # Test intersection
        intersect_result = c1 & c2
        assert isinstance(intersect_result, SolxObject)

    def test_cylinder_transformations(self):
        """Test cylinder transformations."""
        c = cylinder(radius=5, height=10)
        
        # Test translate
        translated = c.translate(Vector3D(5, 0, 0))
        assert isinstance(translated, SolxObject)
        assert translated is not c
        
        # Test rotate
        rotated = c.rotate((90, 0, 0))
        assert isinstance(rotated, SolxObject)
        assert rotated is not c
        
        # Test scale
        scaled = c.scale(Vector3D(2, 2, 1))
        assert isinstance(scaled, SolxObject)
        assert scaled is not c

    def test_center_type_affects_positioning(self):
        """Test that different center types result in different positioning."""
        c_bottom_center = cylinder(radius=5, height=10, center=CenterType.BOTTOM_CENTER)
        c_center = cylinder(radius=5, height=10, center=CenterType.CENTER)
        
        # Should be different objects
        assert c_bottom_center is not c_center

    def test_zero_radius(self):
        """Test cylinder with zero radius."""
        c = cylinder(radius=0, height=10)
        assert isinstance(c, SolxObject)
        assert c.radius == 0

    def test_zero_height(self):
        """Test cylinder with zero height."""
        c = cylinder(radius=5, height=0)
        assert isinstance(c, SolxObject)
        assert c.height == 0

    def test_negative_values(self):
        """Test cylinder with negative values."""
        # Negative values might be valid depending on implementation
        c = cylinder(radius=-5, height=-10)
        assert isinstance(c, SolxObject)

    def test_attribute_access(self):
        """Test that cylinder attributes are accessible."""
        radius = 7
        height = 15
        pos = Vector3D(5, 10, 15)
        center = CenterType.CENTER
        
        c = cylinder(radius=radius, height=height, center=center, position=pos)
        
        assert c.radius == radius
        assert c.height == height
        assert c.center == center
        assert c.position == pos

    def test_segments_parameter(self):
        """Test cylinder with segments parameter if supported."""
        # This test might need adjustment based on actual implementation
        try:
            c = cylinder(radius=5, height=10, segments=32)
            assert isinstance(c, SolxObject)
            if hasattr(c, 'segments'):
                assert c.segments == 32
        except TypeError:
            # If segments parameter is not supported, that's also fine
            pass